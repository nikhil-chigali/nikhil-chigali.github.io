---
description: Architect a new blog series from a seed (phase 1). Invokes the nikhil-blog-series skill.
argument-hint: "<path-to-seed>"
allowed-tools: Read, Write, Glob, Grep, Skill
---

Start a new blog series from the seed at `$1`.

1. If `$1` is empty or the file does not exist, ask for a valid seed path and stop.
2. Read the seed.
3. Invoke the `nikhil-blog-series` skill and follow it to completion: clarifying
   questions one at a time, 2–3 proposed series shapes, section-by-section design,
   approval gate, then write `docs/blog/<slug>/series-design.md` and the manifest.

Do not research or draft in this command — that is /blog-research and later phases.
