from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "edina-dawn"
OUT_DIR = PROJECT / "portraits"
RAW_DIR = PROJECT / "archive" / "v1.0.9" / "raw"
RETIRED_DIR = PROJECT / "archive" / "v1.0.9" / "retired"
MANIFEST_FILE = PROJECT / "manifest.json"

D = Path(r"D:\game\ComfyUI-WorkFisher-V2\ComfyUI\output\任务产出\2026-10-18-其他世界书角色文生图")
E = Path(r"E:\games\deepseek\comfyUI\任务\2026-10-18-其他世界书角色文生图")

SELECTIONS = [
    ("elise", D / "爱丽丝" / "候选v2" / "图-1792397005820_00001_.png", "elise-s2026102320-2.png"),
    ("sylph", E / "希尔菲" / "对照" / "图-1792333260215_00001_.png", "sylph-s2026101819-3.png"),
    ("dorothy", D / "桃乐丝" / "候选" / "图-1792396096212_00001_.png", "dorothy-s2026102171-5.png"),
    ("kael", D / "凯尔" / "候选" / "图-1792386629489_00001_.png", "kael-s2026102125-1.png"),
    ("lucius", D / "卢修斯" / "候选" / "图-1792387716082_00001_.png", "lucius-s2026102131-1.png"),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    for d in (OUT_DIR, RAW_DIR, RETIRED_DIR):
        d.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in manifest["characters"]}
    report = []
    for character_id, src, raw_name in SELECTIONS:
        if not src.exists():
            raise FileNotFoundError(src)
        raw_target = RAW_DIR / raw_name
        shutil.copy2(src, raw_target)
        active = OUT_DIR / f"{character_id}.webp"
        if active.exists():
            shutil.move(str(active), str(RETIRED_DIR / f"{character_id}-pre-20261019.webp"))
        with Image.open(src) as image:
            image.convert("RGB").save(active, "WEBP", quality=90, method=6)
        item = by_id[character_id]
        item.update({
            "status": "ready",
            "sourceRaw": f"archive/v1.0.9/raw/{raw_name}",
            "image": f"portraits/{character_id}.webp",
            "sha256": sha256_file(active),
            "bytes": active.stat().st_size,
        })
        report.append({"id": character_id, "raw": raw_name, "bytes": active.stat().st_size, "sha256": item["sha256"]})
    MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()