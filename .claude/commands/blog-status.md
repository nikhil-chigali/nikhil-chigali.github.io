---
description: Show where the current blog series is in the pipeline (reads the manifest).
argument-hint: "[series-slug]"
allowed-tools: Read, Glob
---

Report the pipeline status for the blog series.

1. If `$1` is given, read `docs/blog/$1/manifest.yaml`. Otherwise, find the most
   recently updated `docs/blog/*/manifest.yaml` (by the `updated` field) and use that.
   If none exists, say "No active series — start one with /blog-series <seed>" and stop.
2. Print: series title + slug, `series_phase`, `current_post`, and a per-post table
   (n, title, status, furthest gate).
3. Print the **next action**: map the furthest state to the command that advances it
   (architected → /blog-research; researched → /blog-plan 1; outlined → /blog-build N;
   built → /blog-verify N; etc.).
4. Print the last 3 `log` entries.

Read-only. Do not modify the manifest.
