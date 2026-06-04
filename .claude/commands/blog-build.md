---
description: Build post N — draft + diagrams in parallel (phase 4). Invokes the nikhil-blog-build skill.
argument-hint: "<post-number> [series-slug]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, Agent
---

Build a planned post.

1. Parse the post number from `$1`. Resolve the series from `$2` if given, else the
   most recently updated manifest. If post `$1` status is not `outlined`, tell the user
   to run /blog-plan $1 first and stop.
2. Invoke the `nikhil-blog-build` skill for post `$1`: dispatch drafter (track A) and
   diagram-maker (track B) against the approved plan, then present G4 (draft content)
   and each G5 (diagram visual) for review, one at a time.
3. Do not commit automatically — leave the draft and assets for Nikhil's review.
4. On completion, tell the user the post is built and point to /blog-verify $1 (Wave 2)
   or a manual review/commit.
