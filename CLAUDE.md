# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Serve locally (live reload):**
```bash
./tools/run.sh
# Custom host: ./tools/run.sh -H 0.0.0.0
# Production mode: ./tools/run.sh -p
```

**Build & test (html-proofer):**
```bash
./tools/test.sh
```

Both scripts wrap `bundle exec jekyll` — run them instead of invoking Jekyll directly. The underlying commands are:
- Dev: `bundle exec jekyll s -l -H 127.0.0.1`
- Prod build: `JEKYLL_ENV=production bundle exec jekyll b -d _site`

## Architecture

**Theme:** `jekyll-theme-chirpy` (~7.4.1) via the Chirpy Starter. Most layout/styling comes from the theme gem and `assets/lib` (a git submodule pointing to `cotes2020/chirpy-static-assets`). Avoid editing theme internals; override by creating matching files in `_layouts/`, `_includes/`, or `_sass/`.

**Key config files:**
- `_config.yml` — site URL, title, tagline, author, social links, pagination, permalink structure (`/posts/:title/`), PWA, and plugin settings
- `_data/contact.yml` / `_data/share.yml` — social/contact links rendered in the sidebar and share buttons
- `_plugins/posts-lastmod-hook.rb` — auto-populates `last_modified_at` for posts from git history; requires `fetch-depth: 0` in CI (already set)

**Deployment:** GitHub Actions (`.github/workflows/pages-deploy.yml`) builds on push to `main` and deploys to GitHub Pages. Manual trigger via `workflow_dispatch` is also available.

## Content Structure

All posts live in `_posts/` with filename format `YYYY-MM-DD-title.md`.

**Front matter template:**
```yaml
---
title: Title Here
date: YYYY-MM-DD HH:MM:SS +0530
categories: [TOP_CATEGORY, SUB_CATEGORY]  # max 2 levels
tags: [tag1, tag2]                         # lowercase, topic/tool descriptors
---
```

**Category taxonomy (defined in README.md):**
- `project` → `[llm-systems, mlops-infra, computer-vision, experiments]`
- `blog` → `[theory, practical-guides, career]`
- `paper-summary` → `[llm, peft, knowledge-graphs, reinforcement-learning]`
- `note` → `[debugging, infra-gotchas, tiny-insights]`
- `miscellaneous`

Each post has exactly 1 category, optionally 1 subcategory, and multiple tags.

**Site tabs** (navigation pages) are in `_tabs/` — `about.md`, `categories.md`, `tags.md`, `archives.md`.

## Scaffolding Posts

`jekyll-compose` is installed for convenient post creation:
```bash
bundle exec jekyll post "My Post Title"
```
