# Repository Guidelines

## Project Structure & Module Organization
- `scripts/` contains runnable tools:
  - `pi_compute.py` generates pi digits into chunk files.
  - `pi_search.py` searches for a digit sequence.
  - `pi_utils.py` holds shared helpers.
- `data/pi_digits/` is the default output location for computed digits.
- `README.md` documents usage in English and Chinese.

## Build, Test, and Development Commands
There is no build step. Key commands:
- `python -m pip install -r requirements.txt` installs dependencies.
- `python scripts/pi_compute.py --digits 1000000` computes digits and writes chunks.
- `python scripts/pi_search.py 1415926` searches for a sequence.

## Coding Style & Naming Conventions
- Python: 4-space indentation, PEP 8 naming (`snake_case`, `PascalCase`).
- Keep scripts CLI-focused and use `pi_utils.py` for shared logic.
- Prefer explicit variable names for numeric algorithms.

## Testing Guidelines
No tests are configured yet. If adding tests:
- Use `tests/` with `test_<module>.py` naming.
- Prefer deterministic checks on small digit counts (e.g., 50–1,000 digits).
- Document the command (e.g., `python -m pytest`) in this file.

## Commit & Pull Request Guidelines
No strict commit convention is established. Use clear, imperative messages (e.g., "Add chunked output format"). PRs should include:
- Purpose and scope summary.
- Example commands used to verify changes.
- Notes on any format or data compatibility impact.

## Data & Storage
The full 200M-digit dataset is large. Keep chunk files out of git unless using Git LFS or release artifacts. Update `README.md` if storage strategy changes.
