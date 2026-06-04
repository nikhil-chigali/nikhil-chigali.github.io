---
description: Two-stage review of post N — coherence then line-level AI tells (phase 7). Dispatches flow-auditor then writing-auditor.
argument-hint: "<post-number> [series-slug]"
allowed-tools: Read, Write, Edit, Glob, Grep, Task, Agent
---

Review a polished post in two stages. Order matters: structure before sentences.

1. Parse the post number from `$1`. Resolve the series from `$2` if given, else the most
   recently updated manifest. If post `$1` status is not `polished` (gate `G7_polish`), tell
   the user to run /blog-polish $1 first and stop.
2. **Stage A — coherence.** Dispatch the `flow-auditor` with the post path and
   `post-N-plan.md`. Present its report; with Nikhil, apply the structural fixes he approves
   (move/add a sentence, mend a transition) to the post. Do not start Stage B until the
   argument reads as coherent.
3. **Stage B — line level.** Dispatch the `writing-auditor` on the post. It edits AI tells
   and calibrates em dashes in place and reports each before → after. Present the changes for
   Nikhil to scan; revert any he rejects.
4. Only after both stages pass, set the post `status: reviewed`, `gate: G8_review`, bump
   `updated`, append a `log` line, and tell the user to run /blog-publish $1.
