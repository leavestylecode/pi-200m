#!/usr/bin/env python3
import argparse
from pathlib import Path

from pi_utils import list_chunk_files, load_manifest


def extract_fractional(text):
    if "3." in text:
        idx = text.find("3.")
        tail = text[idx + 2 :]
    elif "." in text:
        idx = text.find(".")
        tail = text[idx + 1 :]
    else:
        tail = text
    return "".join(ch for ch in tail if ch.isdigit())


def load_generated_digits(input_dir):
    manifest = load_manifest(input_dir)
    width = manifest["width"]
    files = list_chunk_files(input_dir, width)

    for path in files:
        data = path.read_text(encoding="utf-8").strip()
        if data:
            yield data


def compare_digits(source_digits, generated_chunks):
    offset = 0
    idx = 0
    buffer = source_digits

    for chunk in generated_chunks:
        if offset + len(chunk) > len(buffer):
            return False, offset, "", ""
        for i, ch in enumerate(chunk):
            if buffer[offset + i] != ch:
                pos = offset + i
                return False, pos, buffer[pos : pos + 10], chunk[i : i + 10]
        offset += len(chunk)

    if offset != len(buffer):
        return False, offset, buffer[offset : offset + 10], ""
    return True, None, "", ""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare an external pi digit file with generated chunks"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="path to external pi digit file (e.g., one-million.txt)",
    )
    parser.add_argument(
        "--input-dir",
        default="data/pi_digits",
        help="directory containing generated digit chunks",
    )
    parser.add_argument(
        "--normalize-output",
        default=None,
        help="write normalized fractional digits to this path",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    source_path = Path(args.source)
    if not source_path.is_file():
        raise SystemExit(f"{source_path} not found")

    text = source_path.read_text(encoding="utf-8", errors="ignore")
    fractional = extract_fractional(text)
    if not fractional:
        raise SystemExit("No digits found in source")

    if args.normalize_output:
        Path(args.normalize_output).write_text(fractional, encoding="utf-8")

    generated = load_generated_digits(args.input_dir)
    ok, pos, a, b = compare_digits(fractional, generated)
    if ok:
        print("MATCH")
    else:
        print(f"MISMATCH at position {pos + 1}")
        if a or b:
            print(f"source: {a}")
            print(f"generated: {b}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
