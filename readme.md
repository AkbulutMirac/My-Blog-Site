# Minimal Markdown Blog (FastAPI + Static Editor)

A small, minimal blog project with a lightweight frontend editor and a FastAPI backend. Posts are stored as Markdown files in the `entries/` folder; the editor supports headings, image uploads, and simple formatting. This repository is intended as a compact personal/blogging tool.
To see what it looks like [blog.miracakbulut.online](https://blog.miracakbulut.online/)

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

## Contributing
- Contributions and improvements are welcome.
---

