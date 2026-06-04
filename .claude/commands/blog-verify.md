---
description: Fact-check post N against sources and flag depth gaps (phase 5). Dispatches the verifier subagent.
argument-hint: "<post-number> [series-slug]"
allowed-tools: Read, Write, Edit, Glob, Grep, Task, Agent
---

Verify a built post.

1. Parse the post number from `$1`. Resolve the series from `$2` if given, else the most
   recently updated `docs/blog/*/manifest.yaml`. If post `$1` status is not `built`
   (gate `G5_diagrams`), tell the user to run /blog-build $1 first and stop.
2. Dispatch the `verifier` subagent with the post path and `research-dump.md`.
3. When it returns, present the verify report for the **G6** gate: walk the ✗/? claims and
   the unresolved VERIFY markers, and surface the depth-gap suggestions. Do not advance
   automatically.
4. For each ✗/? claim Nikhil decides to fix, apply the verifier's proposed correction to the
   post `_posts/...md` (or re-dispatch the drafter for a larger rewrite). Re-confirm with him.
5. Only on Nikhil's approval, set the post `status: verified`, `gate: G6_verify`, bump
   `updated`, append a `log` line, and tell the user to run /blog-polish $1.
