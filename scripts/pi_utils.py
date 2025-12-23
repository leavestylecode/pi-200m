import json
import re
from pathlib import Path

MANIFEST_NAME = "manifest.json"
CHUNK_RE = re.compile(r"^pi_digits_(\d+)_(\d+)\.txt$")


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


def list_chunk_files_auto(output_dir):
    path = Path(output_dir)
    items = []
    for entry in path.iterdir():
        if not entry.is_file():
            continue
        match = CHUNK_RE.match(entry.name)
        if not match:
            continue
        start = int(match.group(1))
        end = int(match.group(2))
        items.append((start, end, entry))
    best_by_start = {}
    for start, end, entry in items:
        current = best_by_start.get(start)
        if current is None or end > current[0]:
            best_by_start[start] = (end, entry)

    ordered = []
    last_end = 0
    for start in sorted(best_by_start):
        end, entry = best_by_start[start]
        if last_end:
            if start <= last_end:
                raise SystemExit(
                    f"Overlapping chunks detected at start {start}. "
                    "Remove extra files or regenerate digits."
                )
            if start != last_end + 1:
                raise SystemExit(
                    f"Non-contiguous chunks: expected start {last_end + 1} got {start}. "
                    "Remove extra files or regenerate digits."
                )
        ordered.append(entry)
        last_end = end
    return ordered
