---
name: nikhil-blog-build
description: Use when building a planned post for Nikhil's blog. Dispatches the drafter and diagram-maker subagents in parallel against the approved outline, then routes the draft and each diagram through their approval gates.
---

# Building a Planned Post

This is phase ④ of Nikhil's blog pipeline. You take an approved post plan and turn it into a built post: the section prose in `_posts/`, and every diagram as a themed SVG under `assets/img/posts/<slug>/`. You do this by dispatching two subagents — `drafter` and `diagram-maker` — against the plan, then routing their output through Nikhil's approval gates.

You are forking the *shape* of the superpowers `subagent-driven-development` skill: a fresh subagent per bounded job, you curate exactly the context each one needs (they never inherit your session history), and you handle their status reports. You are dropping everything that skill does for code — no TDD, no red-green, no spec-vs-code reviewer subagents, no test runs, no commit-per-task. The review here is Nikhil approving the draft content (**G4**) and each diagram visually (**G5**), not a code reviewer.

**Why subagents:** the diagram visual loop runs several iterations per diagram; containing each in its own subagent keeps that churn out of your main thread. The drafter and diagram-maker run as independent tracks, so dispatch them together.

## Preconditions

The post you are building must be at `status: outlined` (gate `G3_outline`) in `docs/blog/<slug>/manifest.yaml`.

- Read the post's `posts[]` entry for the `<N>` you were given. Confirm `status: outlined`.
- If it is not outlined, **refuse and stop.** Tell the user the post is not planned yet and point them at `/blog-plan <N>`. Do not draft or diagram from an un-approved plan.

## Inputs you curate for the subagents

Read these yourself first, so you hand each subagent exactly what it needs and nothing else:

1. `docs/blog/<slug>/post-N-plan.md` — the section-by-section teaching plan. The authority on what each section teaches, in what order, and which components it needs.
2. `docs/blog/<slug>/research-dump.md` — the cited facts and numbers the drafter draws on.
3. The post's `manifest.yaml` entry — for `n`, `slug`, and `title`.

## Track A — drafting (gate G4)

Dispatch ONE `drafter` subagent for the whole post.

- Give it the path to `post-N-plan.md` and `research-dump.md`, plus the target file `_posts/YYYY-MM-DD-<slug>.md`.
- Its contract: it loads the `nikhil-brand-voice` skill, writes the Chirpy front matter and the section prose per the plan, leaves **image placeholders** at the agreed `/assets/img/posts/<slug>/<name>.svg` paths with descriptive alt text, and marks any claim it cannot source from the dump as `<!-- VERIFY: ... -->` rather than inventing it. It does NOT restructure into callouts/bullets (that is phase ⑥) and does NOT commit.
- When it returns, present the draft for the **G4** content-correct review: is each section teaching the right thing, in the plan's order, with the chosen examples and correct values? Surface the `<!-- VERIFY: ... -->` markers so Nikhil knows what the verifier (phase ⑤) will need to check.

On a G4 change request, re-dispatch the `drafter` only — with the specific section and the requested change — never the diagram-maker.

When the draft clears G4 — even if diagrams are still looping — record progress so a resumed build does not re-draft from scratch: set the post's `gate: G4_draft` (leave `status: outlined`), bump `updated`, and append a `log` line. On resume, if the post is already at `gate: G4_draft`, skip the drafter and run only the diagrams that have not yet cleared G5.

## Track B — diagrams (gate G5)

For **each** component in the plan marked as a diagram, dispatch one `diagram-maker` subagent (one per diagram).

- Give it that one component's single message (one sentence) plus the post `slug`. One message per diagram; if the plan lists two messages, that is two diagrams and two dispatches.
- Its contract: it writes `make_<name>.py` (importing the shared `svg_theme`) and `<name>.svg` under `assets/img/posts/<slug>/`, emits explicit width/height and light/dark theming, renders locally (`python -m http.server` + the browser tools), and screenshots in both light and dark.
- It drives the **G5** visual-approval sub-loop itself: it shows the screenshot, takes Nikhil's feedback, regenerates, and re-shows. **Expect several iterations per diagram** — that loop is contained inside the subagent. The diagram passes G5 when Nikhil approves it visually.

On a G5 change request for a diagram already returned, re-dispatch the `diagram-maker` for that one diagram with the specific feedback.

## Parallelism

Tracks A and B are independent — dispatch them together, in one batch, so the draft and the diagrams build concurrently.

- But present **G4 and each G5 to the user ONE AT A TIME** for review. Do not dump the draft and three diagrams on Nikhil at once; walk each gate separately.
- **Never dispatch two subagents that write the same file simultaneously.** The drafter owns the `_posts/<slug>.md` file; each diagram-maker owns its own `make_<name>.py`/`<name>.svg`. These never collide, which is what makes the parallel dispatch safe. If you ever need two writes to the same path, serialize them.

## Handling subagent results

Each subagent reports one of four statuses. Handle each:

**DONE:** proceed to its gate (G4 for the drafter, G5 for that diagram).

**DONE_WITH_CONCERNS:** the work is finished but the subagent flagged a doubt. Read it before presenting the gate. If it bears on content correctness (a claim it could not source, a value it had to approximate), surface it to Nikhil at the gate. If it is a passing observation, note it and proceed.

**NEEDS_CONTEXT:** it is missing something you did not hand it (a value, a path, a plan detail). Provide exactly that and re-dispatch. Do not make it read the whole plan to find one fact.

**BLOCKED:** it cannot complete. Assess: a context gap → provide context and re-dispatch; a harder job than the model can handle → re-dispatch with a more capable model; a plan that is actually wrong → escalate to Nikhil rather than forcing a fix. Never re-dispatch the same model with the same input and expect a different result.

## Gate bookkeeping

Record two checkpoints, so a resumed build knows exactly what is left:

- **When the draft clears G4** (diagrams may still be in flight): set `gate: G4_draft`, leave `status: outlined`, bump `updated`, append `"<YYYY-MM-DD> drafted: post <N> draft cleared G4"`.
- **When the draft has passed G4 and every diagram has passed G5:** set `status: built`, `gate: G5_diagrams`, bump `updated`, append `"<YYYY-MM-DD> built: post <N> drafted + diagrams approved"`.

Do not invent manifest fields — use only what the template defines. Do not set `gate: G5_diagrams` until the draft and all diagrams have cleared.

## No commits in this skill

Building **writes files** — the post `.md`, the generator `.py` scripts, the `.svg` outputs. It does **not** commit them. Committing is reviewed by Nikhil separately (the review-before-commit flow, or `/blog-review` in a later wave). Do **not** `git add` or `git commit` anything from this skill, and never `git add .` / `-A`.

## Terminal state

After the draft passes G4, every diagram passes G5, and the manifest reads `status: built` / `gate: G5_diagrams`, stop. Tell the user:

> Post N is built: the draft is in `_posts/YYYY-MM-DD-<slug>.md` and its diagrams are in `assets/img/posts/<slug>/`. The manifest is at `G5_diagrams`. Run `/blog-verify <N>` (a later wave) to fact-check the draft, or review and commit it manually.

Do NOT auto-proceed to verification, polishing, or any other phase, and do not commit. The next move is the user's.
