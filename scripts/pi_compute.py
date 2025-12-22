#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

try:
    import gmpy2
except ImportError as exc:
    raise SystemExit(
        "gmpy2 is required. Install with: python -m pip install -r requirements.txt"
    ) from exc

from pi_utils import chunk_filename, write_manifest

DIGITS_PER_TERM = 14.181647462725477
C3_OVER_24 = 640320**3 // 24


def bs(a, b):
    if b - a == 1:
        if a == 0:
            p = gmpy2.mpz(1)
            q = gmpy2.mpz(1)
        else:
            p = gmpy2.mpz((6 * a - 5) * (2 * a - 1) * (6 * a - 1))
            q = gmpy2.mpz(a) * a * a * C3_OVER_24
        t = p * (13591409 + 545140134 * a)
        if a % 2:
            t = -t
        return p, q, t

    m = (a + b) // 2
    p1, q1, t1 = bs(a, m)
    p2, q2, t2 = bs(m, b)
    p = p1 * p2
    q = q1 * q2
    t = t1 * q2 + p1 * t2
    return p, q, t


def compute_pi_fractional_digits(digits, guard):
    if digits <= 0:
        raise ValueError("digits must be positive")

    terms = int(digits / DIGITS_PER_TERM) + 1
    p, q, t = bs(0, terms)

    scale = gmpy2.mpz(10) ** (digits + guard)
    sqrt_c = gmpy2.isqrt(gmpy2.mpz(10005) * scale * scale)
    pi_scaled = (gmpy2.mpz(426880) * sqrt_c * q) // t

    s = str(pi_scaled)
    if guard:
        s = s[:-guard]

    needed_len = digits + 1
    if len(s) < needed_len:
        s = "0" * (needed_len - len(s)) + s

    s = s[:needed_len]
    integer = s[0]
    fractional = s[1:]
    return integer, fractional


def write_chunks(fractional, output_dir, chunk_size):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    digits = len(fractional)
    width = len(str(digits))
    for idx in range(0, digits, chunk_size):
        start = idx + 1
        end = min(idx + chunk_size, digits)
        chunk = fractional[idx:end]
        filename = chunk_filename(start, end, width)
        (output_dir / filename).write_text(chunk, encoding="utf-8")

    manifest = {
        "format_version": 1,
        "digits": digits,
        "chunk_size": chunk_size,
        "index_base": 1,
        "fractional_only": True,
        "width": width,
        "file_template": "pi_digits_{start}_{end}.txt",
    }
    write_manifest(output_dir, manifest)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute pi digits with Chudnovsky binary splitting",
    )
    parser.add_argument(
        "--digits",
        type=int,
        required=True,
        help="number of digits after the decimal point",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1_000_000,
        help="digits per output file",
    )
    parser.add_argument(
        "--output-dir",
        default="data/pi_digits",
        help="directory to store digit chunks",
    )
    parser.add_argument(
        "--guard",
        type=int,
        default=10,
        help="extra guard digits for rounding safety",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="allow overwriting an existing output directory",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)

    if output_dir.exists() and any(output_dir.iterdir()) and not args.overwrite:
        raise SystemExit(
            f"{output_dir} is not empty. Use --overwrite to proceed."
        )

    print(f"Computing {args.digits} digits of pi...")
    integer, fractional = compute_pi_fractional_digits(args.digits, args.guard)
    if integer != "3":
        print(
            "Warning: unexpected integer part. Guard digits may be too small.",
            file=sys.stderr,
        )

    print("Writing chunks...")
    write_chunks(fractional, output_dir, args.chunk_size)
    print(f"Done. Output in {output_dir}")


if __name__ == "__main__":
    main()
