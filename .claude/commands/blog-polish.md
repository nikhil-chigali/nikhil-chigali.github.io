---
description: Restructure post N for digestibility and add cited external links (phase 6). Dispatches the restructurer subagent.
argument-hint: "<post-number> [series-slug]"
allowed-tools: Read, Write, Edit, Glob, Grep, Task, Agent
---

Polish a verified post.

1. Parse the post number from `$1`. Resolve the series from `$2` if given, else the most
   recently updated manifest. If post `$1` status is not `verified` (gate `G6_verify`), tell
   the user to run /blog-verify $1 first and stop.
2. Dispatch the `restructurer` subagent with the post path, `post-N-plan.md`,
   `research-dump.md`, and `post-N-verify.md`.
3. When it returns, present the diff for the **G7** gate: the callouts, bullets, and links it
   added, and any section it deliberately left as prose. Iterate on Nikhil's feedback by
   re-dispatching the restructurer. Do not advance automatically.
4. Only on approval, set the post `status: polished`, `gate: G7_polish`, bump `updated`,
   append a `log` line, and tell the user to run /blog-review $1.
