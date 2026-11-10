"""Generate data/manifest.json from all text-like files under data/.

Run from the repository root after adding/removing data files:
    python scripts/generate_manifest.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MANIFEST_PATH = DATA_DIR / "manifest.json"

# Keep this list to text formats that the browser can safely load as UTF-8.
TEXT_EXTENSIONS = {
    ".txt", ".csv", ".tsv", ".json", ".md", ".log", ".xml",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".py",
    ".sql", ".html", ".css", ".js", ".tex", ".rst",
}

files = sorted(
    path.relative_to(DATA_DIR).as_posix()
    for path in DATA_DIR.rglob("*")
    if path.is_file()
    and path != MANIFEST_PATH
    and path.suffix.lower() in TEXT_EXTENSIONS
)

MANIFEST_PATH.write_text(
    json.dumps({"files": files}, indent=2) + "\n",
    encoding="utf-8",
)
print(f"Updated {MANIFEST_PATH.relative_to(ROOT)} with {len(files)} file(s).")
