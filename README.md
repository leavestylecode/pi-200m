# pi-200m

## Overview (EN)
This project computes and stores the first 200,000,000 digits of pi for fast substring search. It includes a generator that writes digits into fixed-size chunks and a search tool that scans those chunks to find the first occurrence of a digit sequence.

## 使用简介 (中文)
本项目用于计算并保存圆周率小数点后 2 亿位数字，以便进行快速的“pi search”。提供计算脚本（按固定大小分块保存）和搜索脚本（在分块文件中查找首次出现位置）。

## Requirements
- Python 3.10+
- `gmpy2` (GMP/MPIR backend for big integers)

Install:
```bash
python -m pip install -r requirements.txt
```

## Compute Digits
Generate fractional digits and write chunked files:
```bash
python scripts/pi_compute.py --digits 200000000 --chunk-size 1000000 --output-dir data/pi_digits
```
Notes:
- Output contains **fractional digits only** (no leading `3.`).
- Each file is named `pi_digits_<start>_<end>.txt` with 1-based positions.
- `data/pi_digits/manifest.json` describes chunk size and format.

## Search Digits
Search for the first occurrence position (1-based, fractional digits):
```bash
python scripts/pi_search.py 1415926 --input-dir data/pi_digits
```
If the sequence is found, the script prints the position. If not found, it exits with code 1.

## Output Format
- Chunk files: ASCII digits only, no newlines.
- Manifest fields: `digits`, `chunk_size`, `width`, `index_base`, `fractional_only`.

## GitHub Storage
Only commit scripts, configuration, and documentation. Do not commit generated digit files. The `.gitignore` excludes `data/pi_digits/`.
If you want to share results, use Git LFS or GitHub Releases for the chunk files.

## Resource Considerations
Computing 200M digits is CPU/RAM intensive. This implementation uses Chudnovsky binary splitting and may take hours (or longer) depending on hardware. Adjust `--guard` for safer rounding if needed.
