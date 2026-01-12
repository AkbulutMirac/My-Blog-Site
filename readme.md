# Minimal Markdown Blog (FastAPI + Static Editor)

A small, minimal blog project with a lightweight frontend editor and a FastAPI backend. Posts are stored as Markdown files in the `entries/` folder; the editor supports headings, image uploads, and simple formatting. This repository is intended as a compact personal/blogging tool you can host locally.
To see what it looks like blog.miracakbulut.onlie

## Features

- Password-protected posting endpoint (simple shared-password flow).
- Rich editor UI.
- Image paste / drag-and-drop support in the editor (saved as data URLs in posts).
- Posts saved as Markdown files with a human-friendly title and auto-added timestamp.
- Safe filename slugs: user-visible titles are free-form; server sanitizes slugs for filenames.

## Key Files

- `static/index.html` — Frontend UI and in-browser editor.
- `api/endpoints.py` — FastAPI endpoints for listing, rendering, posting, and deleting posts.
- `entries/` — Directory where Markdown posts are stored (one `.md` per post).

## Quickstart (local development)

1. Install dependencies. If this repository has a `requirements.txt`, use it; otherwise install core packages:

```powershell
pip install -r requirements.txt
# or, if no requirements file is present:
pip install fastapi uvicorn markdown
```

2. Open the frontend: open `static/index.html` in your browser and configure the API base URL if needed (the editor assumes the API is reachable at the same host used in development).

3. Run the FastAPI app. If your app object is exposed as `app` inside `api/endpoints.py`, run:

- run 'run.py'.

## Usage Notes

- Posts are stored under `entries/` as Markdown files. Each file is prefixed with the chosen title (as an H1) and contains a timestamp line.
- The project uses a simple shared password approach for authorizing writes/deletes. For production use, replace with a proper auth mechanism.
- Password for adding is in the 'service.py'. You can change it from there.
- The editor performs client-side slug generation for preview; the server re-sanitizes the slug before saving to ensure safe filenames.

## Contributing
- Contributions and improvements are welcome.
---

