import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = path.resolve(import.meta.dirname, '..');
const BASE_URL = process.env.COMFYUI_URL || 'http://192.168.1.2:8188';

function parseArgs(argv) {
    const out = {
        only: '',
        variants: 1,
        prompts: 'prompts/candidates.json',
        project: 'projects/edina-dawn/v1.0.7',
    };
    for (let i = 0; i < argv.length; i += 1) {
        if (argv[i] === '--only') out.only = argv[++i] || '';
        else if (argv[i] === '--variants') out.variants = Math.max(1, Number(argv[++i]) || 1);
        else if (argv[i] === '--prompts') out.prompts = String(argv[++i] || '');
        else if (argv[i] === '--project') out.project = String(argv[++i] || '');
    }
    return out;
}

function replaceDeep(value, replacements) {
    if (Array.isArray(value)) return value.map((item) => replaceDeep(item, replacements));
    if (value && typeof value === 'object') {
        return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, replaceDeep(item, replacements)]));
    }
    if (typeof value !== 'string') return value;
    let result = value;
    for (const [key, replacement] of Object.entries(replacements)) {
        result = result.split(`%${key}%`).join(String(replacement));
    }
    return result;
}

async function api(pathname, options) {
    const response = await fetch(`${BASE_URL}${pathname}`, options);
    if (!response.ok) throw new Error(`${pathname} -> ${response.status} ${await response.text()}`);
    return response;
}

async function waitForResult(promptId, timeoutMs = 240000) {
    const started = Date.now();
    while (Date.now() - started < timeoutMs) {
        const response = await api(`/history/${encodeURIComponent(promptId)}`);
        const history = await response.json();
        const entry = history[promptId];
        if (entry?.status?.completed) return entry;
        if (entry?.status?.status_str === 'error') throw new Error(`ComfyUI error: ${JSON.stringify(entry.status)}`);
        await new Promise((resolve) => setTimeout(resolve, 2000));
    }
    throw new Error(`ComfyUI timeout: ${promptId}`);
}

function collectImages(historyEntry) {
    const images = [];
    for (const output of Object.values(historyEntry.outputs || {})) {
        for (const image of output.images || []) {
            images.push(image);
        }
    }
    return images;
}

async function downloadImage(image, targetFile) {
    const params = new URLSearchParams({
        filename: image.filename,
        subfolder: image.subfolder || '',
        type: image.type || 'output',
    });
    const response = await api(`/view?${params.toString()}`);
    const buffer = Buffer.from(await response.arrayBuffer());
    fs.writeFileSync(targetFile, buffer);
    return {
        sha256: crypto.createHash('sha256').update(buffer).digest('hex'),
        bytes: buffer.length,
    };
}

async function generateOne(character, spec, workflowSnapshot, variant, project, rawDir) {
    const positive = [spec.commonPrefix, character.positive, spec.commonSuffix].join(', ');
    const seed = Number(character.seed) + variant;
    const replacements = {
        prompt: positive,
        negative_prompt: spec.negative,
        MODEL_NAME: workflowSnapshot.model,
        vae: workflowSnapshot.vae,
        width: spec.width,
        height: spec.height,
        seed,
        steps: spec.steps,
        cfg_scale: spec.cfg,
        sampler_name: spec.sampler,
        scheduler: spec.scheduler,
    };
    const prompt = replaceDeep(workflowSnapshot.workflow, replacements);
    const clientId = crypto.randomUUID();
    const response = await api('/prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, client_id: clientId }),
    });
    const body = await response.json();
    const history = await waitForResult(body.prompt_id);
    const images = collectImages(history);
    if (!images.length) throw new Error(`No output image for ${character.id} seed ${seed}`);
    const targetFile = path.join(rawDir, `${character.id}-s${seed}-${variant + 1}.png`);
    const file = await downloadImage(images[0], targetFile);
    return {
        characterId: character.id,
        characterName: character.name,
        seed,
        positive,
        negative: spec.negative,
        workflow: workflowSnapshot.sourcePreset,
        model: workflowSnapshot.model,
        promptId: body.prompt_id,
        image: path.relative(project, targetFile).replaceAll('\\', '/'),
        ...file,
    };
}

async function main() {
    const args = parseArgs(process.argv.slice(2));
    const project = path.resolve(ROOT, args.project);
    if (!project.startsWith(path.join(ROOT, 'projects'))) throw new Error(`Project escapes projects root: ${project}`);
    const workflowFile = path.join(project, 'prompts', 'workflow-anima.json');
    const rawDir = path.join(project, 'portraits', 'raw');
    const recordFile = path.join(project, 'prompts', 'generation-records.json');
    const promptsFile = path.resolve(project, args.prompts);
    if (!promptsFile.startsWith(project)) throw new Error(`Prompt file escapes project: ${promptsFile}`);
    const spec = JSON.parse(fs.readFileSync(promptsFile, 'utf8'));
    const workflowSnapshot = JSON.parse(fs.readFileSync(workflowFile, 'utf8'));
    fs.mkdirSync(rawDir, { recursive: true });

    const selected = spec.characters.filter((character) => !args.only || character.id === args.only);
    if (!selected.length) throw new Error(`Unknown character id: ${args.only}`);

    const records = fs.existsSync(recordFile)
        ? JSON.parse(fs.readFileSync(recordFile, 'utf8'))
        : { schemaVersion: 1, runs: [] };

    for (const character of selected) {
        for (let variant = 0; variant < args.variants; variant += 1) {
            const record = await generateOne(character, spec, workflowSnapshot, variant, project, rawDir);
            records.runs.push(record);
            fs.writeFileSync(recordFile, `${JSON.stringify(records, null, 2)}\n`, 'utf8');
            console.log(JSON.stringify(record));
        }
    }
}

main().catch((error) => {
    console.error(error);
    process.exit(1);
});
