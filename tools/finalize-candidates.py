from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "edina-dawn" / "v1.0.7"
RAW_DIR = PROJECT / "portraits" / "raw"
OUT_DIR = PROJECT / "portraits"
MANIFEST_FILE = PROJECT / "manifest.json"

SELECTIONS = {
    "victoria": "victoria-s740003-3.png",
    "clara": "clara-s741002-2.png",
    "lumina": "lumina-s742002-2.png",
    "merl": "merl-s743002-2.png",
    "cecilia": "cecilia-s744002-2.png",
    "beatrix": "beatrix-s745002-2.png",
    "yulia": "yulia-s746001-1.png",
    "sylvana": "sylvana-s747001-1.png",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in manifest["characters"]}

    for character_id, raw_name in SELECTIONS.items():
        raw_file = RAW_DIR / raw_name
        output_file = OUT_DIR / f"{character_id}.webp"
        if not raw_file.exists():
            raise FileNotFoundError(raw_file)

        with Image.open(raw_file) as image:
            rgb = image.convert("RGB")
            rgb.save(output_file, "WEBP", quality=90, method=6)

        item = by_id[character_id]
        item.update(
            {
                "status": "ready",
                "sourceRaw": f"portraits/raw/{raw_name}",
                "image": f"portraits/{character_id}.webp",
                "sha256": sha256_file(output_file),
                "bytes": output_file.stat().st_size,
            }
        )

    manifest["status"] = "ready"
    MANIFEST_FILE.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Finalized {len(SELECTIONS)} portraits.")


if __name__ == "__main__":
    main()
