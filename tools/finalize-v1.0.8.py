from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "edina-dawn"
VERSION_DIR = PROJECT / "v1.0.8"
PREVIOUS_DIR = PROJECT / "v1.0.7"
RAW_DIR = VERSION_DIR / "portraits" / "raw"
OUT_DIR = VERSION_DIR / "portraits"

CANDIDATE_SELECTIONS = {
    "victoria": "victoria-s740003-3.png",
    "clara": "clara-s741002-2.png",
    "lumina": "lumina-s742002-2.png",
    "merl": "merl-s743002-2.png",
    "cecilia": "cecilia-s744002-2.png",
    "beatrix": "beatrix-s745002-2.png",
    "yulia": "yulia-s746001-1.png",
    "sylvana": "sylvana-s747001-1.png",
}

WORLDBOOK_IDS = [
    "lilith",
    "elise",
    "sariel",
    "sylph",
    "seraphina",
    "tia",
    "mimi",
    "kael",
    "lucius",
    "eludi",
    "freya",
    "celine",
    "livia",
    "dorothy",
    "ophelia",
    "yuffie",
    "natasha",
    "roland",
    "jack",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_characters() -> dict[str, dict]:
    candidates = json.loads((VERSION_DIR / "prompts" / "candidates.json").read_text(encoding="utf-8"))
    worldbook = json.loads((VERSION_DIR / "prompts" / "worldbook-characters.json").read_text(encoding="utf-8"))
    return {
        character["id"]: character
        for character in [*candidates["characters"], *worldbook["characters"]]
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    characters = load_characters()
    manifest_characters = []

    for character_id, raw_name in CANDIDATE_SELECTIONS.items():
        raw_file = RAW_DIR / raw_name
        if not raw_file.exists():
            shutil.copy2(PREVIOUS_DIR / "portraits" / "raw" / raw_name, raw_file)

    for character_id in WORLDBOOK_IDS:
        matches = sorted(RAW_DIR.glob(f"{character_id}-s*-1.png"))
        if len(matches) != 1:
            raise RuntimeError(f"Expected one raw image for {character_id}, found {len(matches)}")

    ordered_ids = [*CANDIDATE_SELECTIONS.keys(), *WORLDBOOK_IDS]
    for character_id in ordered_ids:
        if character_id in CANDIDATE_SELECTIONS:
            raw_file = RAW_DIR / CANDIDATE_SELECTIONS[character_id]
        else:
            raw_file = sorted(RAW_DIR.glob(f"{character_id}-s*-1.png"))[0]

        output_file = OUT_DIR / f"{character_id}.webp"
        with Image.open(raw_file) as image:
            image.convert("RGB").save(output_file, "WEBP", quality=90, method=6)

        character = characters[character_id]
        manifest_characters.append(
            {
                "id": character_id,
                "name": character["name"],
                "image": f"portraits/{character_id}.webp",
                "status": "ready",
                "sourceRaw": f"portraits/raw/{raw_file.name}",
                "sha256": sha256_file(output_file),
                "bytes": output_file.stat().st_size,
            }
        )

    manifest = {
        "schemaVersion": 1,
        "projectId": "edina-dawn",
        "cardVersion": "1.0.8",
        "cardSource": "圣女今天也很努力（大概）！",
        "status": "ready",
        "backend": {
            "plugin": "st-chatu8",
            "mode": "comfyui",
            "url": "http://192.168.1.2:8188",
            "model": "anima\\【轻柔二次元】miaomiaoHarem_anima13.safetensors",
            "workflow": "生图anima专用 (1)",
        },
        "promptFiles": [
            "prompts/candidates.json",
            "prompts/worldbook-characters.json",
        ],
        "characters": manifest_characters,
    }
    (VERSION_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Finalized {len(manifest_characters)} portraits.")


if __name__ == "__main__":
    main()
