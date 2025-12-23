# pi-200m

# English

## Overview
This project computes and stores the first 200,000,000 digits of pi for fast substring search. It includes a generator that writes digits into fixed-size chunks and a search tool that scans those chunks to find the first occurrence of a digit sequence.

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

## Packed Format (Space Saving)
Pack digits into a binary file using two digits per byte (00–99), about 50% size reduction:
```bash
python scripts/pi_pack.py --input-dir data/pi_digits --output-dir data/pi_packed
```
Search the packed output:
```bash
python scripts/pi_search_packed.py 1415926 --input-dir data/pi_packed
```
On typical desktop hardware, a full scan against 200M digits is usually a few seconds.

## Checksums
Create a checksum list:
```bash
python scripts/pi_hash.py --input-dir data/pi_digits
```
Verify later:
```bash
python scripts/pi_hash.py --input-dir data/pi_digits --verify
```

## GitHub Storage
Only commit scripts, configuration, and documentation. Do not commit generated digit files. The `.gitignore` excludes `data/pi_digits/`.
If you want to share results, use Git LFS or GitHub Releases for the chunk files.

### Sharing Results (EN)
Option A: Git LFS
```bash
git lfs install
git lfs track "data/pi_digits/*.txt" "data/pi_digits/manifest.json" "data/pi_digits/checksums.txt"
git add .gitattributes data/pi_digits/manifest.json data/pi_digits/checksums.txt
```
Option B: GitHub Releases
```bash
python scripts/pi_hash.py --input-dir data/pi_digits
tar -czf pi_digits.tar.gz data/pi_digits
```
Upload the archive to a GitHub Release and keep scripts in git.

## Resource Considerations
Computing 200M digits is CPU/RAM intensive. This implementation uses Chudnovsky binary splitting and may take hours (or longer) depending on hardware. Adjust `--guard` for safer rounding if needed.

## External Validation
Compare against a known source (e.g., Eve Andersson's 1,000,000 digits file):
```bash
python scripts/pi_compare.py --source data/check/one-million.txt --input-dir data/pi_digits
```
Optionally write a normalized digits-only file for future comparisons:
```bash
python scripts/pi_compare.py --source data/check/one-million.txt --normalize-output data/check/one-million.digits.txt
```

# 中文

## 项目简介
本项目用于计算并保存圆周率小数点后 2 亿位数字，以便进行快速的“pi search”。提供计算脚本（按固定大小分块保存）和搜索脚本（在分块文件中查找首次出现位置）。

## 环境依赖
- Python 3.10+
- `gmpy2`（大整数运算依赖）

安装：
```bash
python -m pip install -r requirements.txt
```

## 计算数字
生成小数部分并分块保存：
```bash
python scripts/pi_compute.py --digits 200000000 --chunk-size 1000000 --output-dir data/pi_digits
```
说明：
- 输出只包含小数部分（不包含 `3.`）。
- 文件命名为 `pi_digits_<start>_<end>.txt`，位置从 1 开始计数。
- `data/pi_digits/manifest.json` 记录分块参数。

## 搜索数字
查找首次出现位置（小数部分，1-based）：
```bash
python scripts/pi_search.py 1415926 --input-dir data/pi_digits
```
找到后输出位置，未找到返回非 0 退出码。

## 输出格式
- 分块文件：仅包含数字字符，无换行。
- 清单字段：`digits`, `chunk_size`, `width`, `index_base`, `fractional_only`。

## 二进制压缩格式
把数字按“每字节两位”打包，体积约减少一半：
```bash
python scripts/pi_pack.py --input-dir data/pi_digits --output-dir data/pi_packed
```
在打包结果中检索：
```bash
python scripts/pi_search_packed.py 1415926 --input-dir data/pi_packed
```
在普通桌面机器上，扫描 2 亿位通常只需几秒级。

## 校验
生成校验清单：
```bash
python scripts/pi_hash.py --input-dir data/pi_digits
```
验证校验清单：
```bash
python scripts/pi_hash.py --input-dir data/pi_digits --verify
```

## GitHub 存储
只提交脚本、配置与文档，不提交生成的数据文件。`.gitignore` 已排除 `data/pi_digits/`。
如需共享结果，建议使用 Git LFS 或 GitHub Release。

### 结果发布建议 (中文)
方案 A：Git LFS
```bash
git lfs install
git lfs track "data/pi_digits/*.txt" "data/pi_digits/manifest.json" "data/pi_digits/checksums.txt"
git add .gitattributes data/pi_digits/manifest.json data/pi_digits/checksums.txt
```
方案 B：GitHub Release
```bash
python scripts/pi_hash.py --input-dir data/pi_digits
tar -czf pi_digits.tar.gz data/pi_digits
```
把压缩包上传到 Release，脚本仍保留在仓库中。

## 资源消耗说明
计算 2 亿位需要较高 CPU/RAM，运行时间可能很长。必要时可调整 `--guard` 以提高安全的舍入余量。

## 外部校验
使用已知来源进行对比（例如 Eve Andersson 的 100 万位文件）：
```bash
python scripts/pi_compare.py --source data/check/one-million.txt --input-dir data/pi_digits
```
可选：输出标准化纯数字文件，便于重复比对：
```bash
python scripts/pi_compare.py --source data/check/one-million.txt --normalize-output data/check/one-million.digits.txt
```
