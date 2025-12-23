#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DIGIT_TABLE = [
    (str(i // 10), str(i % 10)) for i in range(100)
]


def normalize_pattern(raw):
    if "." in raw:
        raw = raw.split(".", 1)[1]
    digits = "".join(ch for ch in raw if ch.isdigit())
    if not digits:
        raise ValueError("pattern must contain digits")
    return digits


def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search_stream(pattern, byte_iter, total_digits):
    lps = build_lps(pattern)
    j = 0
    pos = 0

    for value in byte_iter:
        tens, ones = DIGIT_TABLE[value]
        for digit in (tens, ones):
            if pos >= total_digits:
                return None
            while j and digit != pattern[j]:
                j = lps[j - 1]
            if digit == pattern[j]:
                j += 1
                if j == len(pattern):
                    return pos - len(pattern) + 2
            pos += 1

    return None


def iter_bytes(path, block_size=4 * 1024 * 1024):
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(block_size)
            if not chunk:
                break
            for value in chunk:
                yield value


def parse_args():
    parser = argparse.ArgumentParser(
        description="Search pi digits in packed binary format"
    )
    parser.add_argument("pattern", help="digit sequence to search for")
    parser.add_argument(
        "--input-dir",
        default="data/pi_packed",
        help="directory containing packed pi digits",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        pattern = normalize_pattern(args.pattern)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    input_dir = Path(args.input_dir)
    manifest_path = input_dir / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"{manifest_path} not found")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("pack_scheme") != "two_digits_per_byte":
        raise SystemExit("Unsupported pack scheme")

    total_digits = manifest["digits"]
    binary_path = input_dir / manifest["binary_file"]
    if not binary_path.is_file():
        raise SystemExit(f"{binary_path} not found")

    position = kmp_search_stream(pattern, iter_bytes(binary_path), total_digits)
    if position is None:
        print("Not found")
        raise SystemExit(1)

    print(position)


if __name__ == "__main__":
    main()
