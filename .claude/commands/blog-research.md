---
description: Gather a cited knowledge dump for the current series (phase 2). Dispatches the researcher subagent.
argument-hint: "[series-slug]"
allowed-tools: Read, Glob, Task, Agent
---

Run research for the blog series.

1. Resolve the series: use `$1` if given, else the most recently updated
   docs/blog/*/manifest.yaml. If `series_phase` is `seed`, tell the user to run
   /blog-series first and stop.
2. Dispatch the `researcher` subagent with the path to this series' `series-design.md`.
3. When it returns, summarize the research-dump coverage per planned post and surface
   the "depth we missed" notes for Nikhil's review (GATE G2). Do not proceed past the
   gate automatically.
4. On approval, confirm the manifest shows `series_phase: researched` and tell the user
   to run /blog-plan 1.
