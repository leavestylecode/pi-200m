import json
from pathlib import Path

MANIFEST_NAME = "manifest.json"


def chunk_filename(start, end, width):
    return f"pi_digits_{start:0{width}d}_{end:0{width}d}.txt"


def write_manifest(output_dir, manifest):
    path = Path(output_dir) / MANIFEST_NAME
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def load_manifest(output_dir):
    path = Path(output_dir) / MANIFEST_NAME
    return json.loads(path.read_text(encoding="utf-8"))


def list_chunk_files(output_dir, width):
    path = Path(output_dir)
    files = sorted(path.glob(f"pi_digits_{'?' * width}_{'?' * width}.txt"))
    return files
