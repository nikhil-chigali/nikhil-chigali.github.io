---
name: nikhil-blog-post-plan
description: Use when outlining a single post within a planned series for Nikhil's blog. Produces a section-by-section Feynman/Socratic plan — the question each section opens with, the naive-attempt beat, chosen examples, the per-section component plan, and target callouts — before drafting.
---

# Outlining One Post in a Planned Series

This is phase ③ of Nikhil's blog pipeline. You take an approved series design plus the cited research and turn one post into a precise, section-by-section teaching plan. The drafter and diagram-maker execute this plan in phase ④; they have your plan and little else. Write it so they never have to guess.

You are forking the *shape* of the superpowers `writing-plans` skill: precise and complete (no placeholders), broken into small units, defined output doc, a self-review pass, a handoff. You are dropping everything code-specific — no TDD, no file/test tasks, no commit-per-step. The unit here is a **post section**, and each one is a teaching arc, not a code change.

<HARD-GATE>
Do NOT draft prose, scaffold the post `.md`, generate diagrams, or invoke any other blog skill. This skill produces the plan and stops. Drafting is phase ④ (`/blog-build`). The user runs it after they approve the plan.
</HARD-GATE>

## Inputs

Read all three before planning. The plan is only as good as the design and research behind it.

1. `docs/blog/<slug>/series-design.md` — the through-line, this post's question/hook, its key beats, and its scope fences (what it must NOT cover). The plan stays inside those fences.
2. `docs/blog/<slug>/research-dump.md` — the cited facts, numbers, attributions, and depth this post can draw on. Examples and claims in the plan come from here, not from memory.
3. The post's entry in `docs/blog/<slug>/manifest.yaml` — confirm `n`, `slug`, and `title` for the post you are outlining (the `<N>` the user passed).

If the design or research leaves something the plan needs unresolved, ask the user one question — don't invent the answer.

## Per-section outline schema

This replaces `writing-plans`' task/TDD schema. The post is a sequence of sections; plan each one as a Feynman arc. For **every** section, capture all six:

**(a) Opening question (motivate).** The question the section opens with — the thing the reader wants answered before they'll absorb the concept. A real question, not a heading restated. "Why does the same prompt at T=0 come back different?" not "This section covers determinism."

**(b) Naive-attempt beat.** Where a non-obvious choice is made: the obvious move shown first → why it fails → the real answer. Not every section has one; mark those `naive-attempt: n/a` and say why (e.g. pure setup, or a recap). Where it applies, name the wrong reflex and the exact reason it breaks before the real lever.

**(c) Chosen example(s).** Name the concrete case(s), drawn from the research. Each must pass the **earns-its-place** check, all three:
   - the reader can picture it without prior context,
   - the math/numbers fit in their head,
   - it surfaces the real difficulty (not a trivially-structured case that hides it).
   Give the actual values the example uses (the coin landing "heads" at 9.731043 vs "tails" a few millionths behind, not "some close logits"). If an example fails the check, swap it or name the simplification explicitly.

**(d) Component plan.** The one visual/structural component the section needs, if any:
   - **Diagram** — state the single message it must convey in one sentence (the drafter writes alt text and the diagram-maker builds to this one message). Note it imports the shared `svg_theme` convention (light/dark `@media` block, explicit width/height) used across the series. One message per diagram; if you need two messages, you need two diagrams.
   - **Table** — only for genuine tabular reference data (a recipe/lookup), as a native Markdown table, not an SVG.
   - **Code block** — the snippet and what it shows.
   - Or `component: none` for prose-only sections. Don't manufacture a diagram for a section that doesn't need one.

**(e) Target callouts.** Which Chirpy callout, and where in the section:
   - `.prompt-tip` — the Feynman opening question highlight (series convention: the hook sits in a tip box) and reframes.
   - `.prompt-info` — a clarifying aside that prevents a misread.
   - `.prompt-warning` — a genuine caveat or trap.
   Don't over-callout; one or two per section is plenty. If a section needs none, say so.

**(f) Transition into the next section.** The last beat that hands off — the open question or unresolved thread the next section picks up. This is the coherence spine made local. The final section's transition is the post's closing landing instead (substantive last point, no grand summary).

Write each section's entry as finished, specific instructions — the drafter should not have to make a teaching decision you left open.

## Coherence spine

After the section entries, write one explicit ordered list of the post's beats end-to-end — the argument a reader follows from the opening question to the closing line. Each section's transition (f) should chain into the next section's opening question (a). This list is what the later flow-auditor (phase ⑦) checks the draft against, so it must read as one escalating argument, not a list of topics.

## Output

Write `docs/blog/<slug>/post-N-plan.md` (N is the post number), with this shape:

```
# <Post Title> — Post N Plan

**Answers:** the one question this post resolves (from series-design).
**Hook:** the one-line opening question (the .prompt-tip).
**Scope fence:** what this post does NOT cover (from series-design).

## Section <k>: <working heading>
- **Opening question:** …
- **Naive attempt:** reflex → why it fails → real answer   (or `n/a` + why)
- **Example(s):** named case + actual values; earns-its-place note
- **Component:** diagram (single message) / table / code / none
- **Callouts:** which, where   (or none)
- **Transition:** the thread handed to the next section

## Coherence spine
1. … → 2. … → 3. …   (end-to-end beats)
```

Then update the manifest's entry for this post:
- `status: outlined`
- `gate: G3_outline`
- bump the top-level `updated` to today (`YYYY-MM-DD`)
- append one `log` line: `"<YYYY-MM-DD> outlined: post <N> plan written"`

Do not invent manifest fields — use only what the template defines.

## Self-review

After writing the plan, read it once with fresh eyes against the inputs. This is a checklist you run yourself, not a subagent dispatch.

1. **Placeholder scan.** No "TBD", "flesh out later", "add an example here", "appropriate diagram", "etc.". Every section's six fields are filled with real content. A vague field is a plan failure — fix it inline.
2. **Beat coverage.** Every planned section has an opening question (a) and a component decision (d) — even if the decision is `none`. The naive-attempt beat is present or explicitly marked `n/a`. No section is half-specified.
3. **Example quality.** Each named example earns its place on all three counts (picturable, fits-in-head, surfaces the real difficulty) and its values come from the research dump, not invented. If one only works because it's trivially structured, replace it or flag the simplification.
4. **Spine continuity.** Each section's transition (f) feeds the next section's opening question (a). Read the coherence spine top to bottom — if a step doesn't follow from the one before, the order or a transition is wrong. Fix it.
5. **Inside the fences.** Nothing in the plan strays into what the series-design said this post defers.

Fix issues inline. No need to re-review — fix and move on.

## Voice reference

Any sample prose in the plan — the hook line, example phrasings, a draft transition, an alt-text message — follows the `nikhil-brand-voice` skill. Motivate before naming, define terms inline, no throat-clearing, no significance inflation, no tricolon decoration. A hook is a real opening question, not a table-of-contents line. The plan tells the drafter *what each section teaches and in what order*; it does not have to be the final prose, but any sample of it must already sound right.

## Terminal state

After the plan is written and the manifest is updated, stop. Tell the user:

> Post N plan is written to `docs/blog/<slug>/post-N-plan.md` and the manifest is at `G3_outline`. Run `/blog-build <N>` to draft the post and build its diagrams.

Do NOT auto-proceed to building, drafting, or any other phase. The next move is the user's.
