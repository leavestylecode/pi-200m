#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

from pi_utils import list_chunk_files, load_manifest


def sha256_file(path):
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def write_checksums(input_dir, output_path):
    manifest = load_manifest(input_dir)
    width = manifest["width"]
    files = list_chunk_files(input_dir, width)

    lines = []
    manifest_path = Path(input_dir) / "manifest.json"
    lines.append(f"{sha256_file(manifest_path)}  manifest.json")
    for path in files:
        lines.append(f"{sha256_file(path)}  {path.name}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_checksums(input_dir, checksum_path):
    text = Path(checksum_path).read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("checksum file is empty")

    failures = []
    for line in text.splitlines():
        if "  " not in line:
            continue
        digest, name = line.split("  ", 1)
        path = Path(input_dir) / name
        if not path.exists():
            failures.append(f"missing {name}")
            continue
        actual = sha256_file(path)
        if actual != digest:
            failures.append(f"mismatch {name}")

    return failures


def parse_args():
    parser = argparse.ArgumentParser(description="Create or verify SHA256 checksums")
    parser.add_argument(
        "--input-dir",
        default="data/pi_digits",
        help="directory containing digit chunks",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="output checksum file path (default: <input-dir>/checksums.txt)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="verify existing checksum file instead of creating one",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        raise SystemExit(f"{input_dir} not found")

    output_path = Path(args.output) if args.output else input_dir / "checksums.txt"

    if args.verify:
        failures = verify_checksums(input_dir, output_path)
        if failures:
            raise SystemExit("\n".join(failures))
        print("OK")
        return

    write_checksums(input_dir, output_path)
    print(output_path)


if __name__ == "__main__":
    main()
