#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from pi_utils import list_chunk_files_auto


def normalize_pattern(raw):
    if "." in raw:
        raw = raw.split(".", 1)[1]
    digits = "".join(ch for ch in raw if ch.isdigit())
    if not digits:
        raise ValueError("pattern must contain digits")
    return digits


def search_pattern(output_dir, pattern):
    files = list_chunk_files_auto(output_dir)
    if not files:
        raise SystemExit("No pi digit chunks found in input directory")

    carry = ""
    processed = 0

    for path in files:
        data = path.read_text(encoding="utf-8").strip()
        combined = carry + data
        idx = combined.find(pattern)
        if idx != -1:
            position = processed - len(carry) + idx + 1
            return position

        processed += len(data)
        if len(pattern) > 1:
            carry = combined[-(len(pattern) - 1) :]
        else:
            carry = ""

    return None


def parse_args():
    parser = argparse.ArgumentParser(description="Search for a digit sequence in pi")
    parser.add_argument("pattern", help="digit sequence to search for")
    parser.add_argument(
        "--input-dir",
        default="data/pi_digits",
        help="directory containing pi digit chunks",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        pattern = normalize_pattern(args.pattern)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if Path(args.input_dir).is_dir() is False:
        raise SystemExit(f"{args.input_dir} not found")

    position = search_pattern(args.input_dir, pattern)
    if position is None:
        print("Not found")
        sys.exit(1)

    print(position)


if __name__ == "__main__":
    main()
