---
description: Capture a voice correction, or run the voice-evolver to propose gated brand-voice updates from accumulated feedback (Wave 3 voice loop).
argument-hint: "[note <correction> | evolve]"
allowed-tools: Read, Write, Edit, Glob, Grep, Task, Agent
---

The voice loop has two modes. With no arguments, run **evolve**.

## Capture — `/blog-voice note <text>`

1. Resolve the current series: the most recently updated `docs/blog/*/manifest.yaml`. Read its
   `series_slug`, `current_post`, and the furthest gate of that post.
2. If `docs/blog/<slug>/voice-feedback-log.md` does not exist, create it from
   `docs/blog/_templates/voice-feedback-log.template.md` (substitute the slug in the heading).
3. Append ONE line:
   `<today YYYY-MM-DD> | post <current_post> | <gate> | signal: <kebab-label> | type: <correction|principle> | <text>`
   Derive `<kebab-label>` as the NAME OF THE PATTERN, not the specific words (e.g.
   `imperative-conditional-callout-opener`, not `pin-t0`). Use `type: principle` only if Nikhil
   phrased it as a rule ("always…", "never…"); otherwise `type: correction`.
4. Confirm the line written. Touch nothing else.

## Evolve — `/blog-voice` or `/blog-voice evolve`

1. Dispatch the `voice-evolver` subagent.
2. Present its proposed promotions one at a time at the gate: the signal, the evidence (count +
   the log lines), and the exact proposed edit to `.claude/skills/nikhil-brand-voice/SKILL.md`.
   Also show its "watching" (parked) list so Nikhil sees what is building but not yet promoted.
3. For each proposal Nikhil **approves**: apply that edit to `SKILL.md`, and append the
   evolver's one-line entry to `.claude/skills/nikhil-brand-voice/voice-changelog.md`. For each
   he **rejects**: change nothing — it stays in the logs (still parked, may surface later).
4. NEVER apply an edit Nikhil did not approve. NEVER `git add` or commit — the SKILL.md +
   changelog edits are left in the working tree for Nikhil to review and commit himself.
5. Report which promotions were applied and the new tail of the changelog.
