# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website archive for the artist Benno Berneis (1883-1916). Single-page gallery with bilingual support (EN/DE) and dark/light mode. Originally a Tumblr blog, recreated as a self-hosted static site deployed on Cloudflare Pages.

## Build Command

```bash
python3 build.py
```

This reads `posts.json` and generates `index.html` with embedded post data and JavaScript.

## Architecture

**Data Flow:**
- `posts.json` → `build.py` → `index.html`

**Key Files:**
- `posts.json` - All post content with `images`, `text_en`, `text_de`, `footer`, `link`, `piclink` fields
- `build.py` - Python build script (stdlib only: json, os)
- `styles.css` - Complete styling with CSS variables for theming
- `index.html` - Generated output (do not edit directly)

**Client-Side Rendering:**
- Posts data embedded as JSON in `<script id="posts-data">`
- JavaScript renders posts dynamically based on current language
- Browser language detection with manual EN/DE toggle
- Images converted from Tumblr CDN URLs to local `images/` paths

**Local Assets:**
- `images/` - All artwork images hosted locally
- `pdfs/` - PDF documents (linked from specific posts)

## Deployment

Cloudflare Pages with:
- Build command: `python3 build.py`
- Build output directory: `.` (root)
