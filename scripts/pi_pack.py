#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from pi_utils import list_chunk_files_auto


def pack_digits(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = list_chunk_files_auto(input_dir)
    if not files:
        raise SystemExit("No pi digit chunks found in input directory")

    binary_path = output_dir / "pi_digits.bin"
    digits = 0
    carry = None

    with binary_path.open("wb") as handle:
        for path in files:
            chunk = path.read_text(encoding="utf-8").strip()
            if not chunk:
                continue
            digits += len(chunk)

            if carry is not None:
                chunk = carry + chunk
                carry = None

            if len(chunk) % 2:
                carry = chunk[-1]
                chunk = chunk[:-1]

            for i in range(0, len(chunk), 2):
                value = int(chunk[i : i + 2])
                handle.write(bytes([value]))

        if carry is not None:
            value = int(carry + "0")
            handle.write(bytes([value]))

    manifest = {
        "format_version": 1,
        "digits": digits,
        "index_base": 1,
        "fractional_only": True,
        "pack_scheme": "two_digits_per_byte",
        "binary_file": binary_path.name,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    return binary_path


def parse_args():
    parser = argparse.ArgumentParser(description="Pack pi digits into binary form")
    parser.add_argument(
        "--input-dir",
        default="data/pi_digits",
        help="directory containing text digit chunks",
    )
    parser.add_argument(
        "--output-dir",
        default="data/pi_packed",
        help="directory to store packed output",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    binary_path = pack_digits(args.input_dir, args.output_dir)
    print(binary_path)


if __name__ == "__main__":
    main()
