---
description: Outline post N of the current series (phase 3). Invokes the nikhil-blog-post-plan skill.
argument-hint: "<post-number> [series-slug]"
allowed-tools: Read, Write, Glob, Grep, Skill
---

Outline a post in the current series.

1. Parse the post number from `$1`. Resolve the series from `$2` if given, else the
   most recently updated manifest. If `series_phase` is not at least `researched`, tell
   the user to run /blog-research first and stop.
2. Confirm post `$1` exists in the manifest `posts[]`.
3. Invoke the `nikhil-blog-post-plan` skill for that post and follow it to completion:
   section-by-section outline, component plan, approval gate (G3), write
   docs/blog/<slug>/post-$1-plan.md, update the manifest post status to `outlined`.
4. On completion tell the user to run /blog-build $1.
