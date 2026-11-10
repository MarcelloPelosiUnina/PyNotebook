# PyNotebook — GitHub Pages version

This is the modified PyNotebook. It loads text files committed to the repository's `data/` directory into Pyodide's Python virtual filesystem.

## Folder structure

```text
.
├── index.html
├── README.md
├── scripts/
│   └── generate_manifest.py
└── data/
    ├── manifest.json
    ├── sample.csv
    ├── notes.txt
    └── examples/
        └── extra.csv
```

## Add your own data files

1. Put your `.txt`, `.csv`, `.tsv`, `.json`, `.md`, or other UTF-8 text files inside `data/`. Subfolders are supported.
2. Update `data/manifest.json` so it lists each file path **relative to `data/`**. Example:

   ```json
   {
     "files": [
       "customers.csv",
       "readme.txt",
       "archive/2026/sales.csv"
     ]
   }
   ```

3. To generate that list automatically, run this from the repository root whenever you add or remove files:

   ```bash
   python scripts/generate_manifest.py
   ```

   The script scans common text formats and rewrites `data/manifest.json`. Review and commit the updated manifest together with your data files.

## Read files in Python

Paths are relative to the notebook's virtual filesystem root, so prefix repository data files with `data/`:

```python
from pathlib import Path
import pandas as pd

# CSV
sales = pd.read_csv("data/examples/extra.csv")

# TXT
notes = Path("data/notes.txt").read_text(encoding="utf-8")
print(notes)

# List all loaded files, including nested folders
for path in sorted(Path("data").rglob("*")):
    if path.is_file():
        print(path)
```

The example notebook cells show the same operations when the page first opens.

## Deploy with GitHub Pages

1. Push this project structure to a GitHub repository.
2. In the repository, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select your branch (usually `main`) and the folder `/ (root)`, then save.
4. Open the published Pages URL. The app and the `data/` files are served from the same site, so the relative URLs also work when the repository is published as a project site (for example, `https://username.github.io/repository/`).

## Important deployment note

GitHub Pages is static hosting. A browser cannot ask a static host to enumerate arbitrary directory contents, so the app reads the list in `data/manifest.json` and fetches each listed file. The manifest generator above avoids having to maintain that list by hand.

Only put text files in `data/`; the app reads fetched content as UTF-8 text. Files committed under `data/` are refreshed from the repository when the page is loaded and are read-only in the browser file manager. Files you create elsewhere in the notebook are stored in that browser's local storage, not committed back to GitHub.

For local testing, serve the project folder over HTTP (for example, `python -m http.server 8000`) and open `http://localhost:8000/`. Opening `index.html` directly as a `file://` URL will not work reliably because browsers block these fetch requests.
