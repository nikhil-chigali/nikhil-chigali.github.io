---
name: nikhil-blog-series
description: Use when turning a seed (a study cheatsheet or idea) into a planned technical blog post or series for Nikhil's blog. Architects the through-line, post breakdown, and per-post Feynman hook before any drafting.
---

# Architecting a Blog Series From a Seed

This is phase ① of Nikhil's blog pipeline. You take a seed — a study cheatsheet or a raw idea — and turn it into an approved series design: the through-line, how many posts, and what each post teaches. You do this through one-question-at-a-time dialogue, then you present the design, then you get a hard approval before anything downstream happens.

<HARD-GATE>
Do NOT research, draft, outline, scaffold posts, or invoke any other blog skill until you have presented the series design AND the user has approved it. This holds no matter how small the seed looks. A one-post idea still gets a design; it can be short, but it must be presented and approved.
</HARD-GATE>

## Anti-pattern: "this is obviously one post"

The seed often looks like it maps to a single obvious post. That assumption is exactly where the wasted work starts — wrong reader, wrong scope, two posts crammed into one. Run the process anyway. The design can be three sentences for a genuinely simple seed, but you present it and you get approval.

## Checklist

Work these in order. Do not skip ahead.

1. **Read the seed.** Open the cheatsheet or idea file. Understand what's actually in it before asking anything.
2. **Ask clarifying questions, one at a time.** Use the question bank below. One question per message. Prefer multiple choice. Wait for the answer before the next question.
3. **Propose 2–3 series shapes.** Different ways to slice the material (e.g. one deep post vs. a three-part arc vs. a concept post plus a hands-on post), with tradeoffs and a clear recommendation. Lead with the one you'd pick and say why.
4. **Present the series design section by section.** Get approval after each section. Revise in place if a section is wrong. Do not move on until the section is accepted.
5. **Write `docs/blog/<slug>/series-design.md`** using the doc shape below, where `<slug>` is the kebab-case series slug.
6. **Create `docs/blog/<slug>/manifest.yaml`** from the template (see Manifest creation).
7. **Hand off to `/blog-research`.** Tell the user the next step. Do NOT auto-proceed.

## Question bank

These replace the engineering questions a software brainstorm would ask. Ask only what the seed leaves open — don't interrogate the obvious. One at a time.

- **Reader & prerequisite floor.** Who is this for, and what do you assume they already know? Where does the explanation start — what's below the floor and gets skipped?
- **The through-line.** What single argument or understanding builds across the series? Each post should advance it one step. If you can't name the escalating line, the series probably wants to be fewer posts.
- **Post count & per-post question.** How many posts, and what is the one question each post answers? If two posts answer the same question, merge them. If one post answers three, split it.
- **Per-post Feynman hook.** The one-line opening question each post leads with — the thing the reader wants answered before they'll absorb the concept. "How does a model pick the next word when it's not just the likeliest one?" not "this post covers sampling."
- **Gate / cliffhanger boundaries.** Where does one post naturally end and the next pick up? The seam should leave a question open that the next post answers, not just stop.
- **Scope fences.** For each post, what must it NOT cover — what gets deferred to a later post or declared out of scope entirely? Name the fence so the drafter doesn't wander.

## series-design.md shape

```
# <Series Title> — Series Design

## Through-line
The single escalating argument/understanding. One paragraph. Name the step each post adds.

## Reader & prerequisites
Who it's for. What's assumed known (the floor). What's explicitly below the floor and skipped.

## Post breakdown
For each post:
- **Post N — <working title>**
  - **Answers:** the one question this post resolves
  - **Hook:** the one-line opening question
  - **Key beats:** 3–6 bullets — the reasoning steps in order
  - **Defers:** what this post explicitly does NOT cover (pushed to a later post or out of scope)

## Series arc (optional)
ASCII diagram of how the posts chain — each post's question feeding the next.

## Open questions
Anything unresolved that research (phase ②) or planning (phase ③) must settle.
```

Keep the prose in this doc in Nikhil's voice (see Voice reference). Don't pad sections that are simple.

## Manifest creation

Copy `docs/blog/_templates/manifest.template.yaml` to `docs/blog/<slug>/manifest.yaml` and fill it in:

- `series_slug` — the kebab-case slug (also the `docs/blog/<slug>` dir name).
- `title` — the human series title.
- `seed` — path to the seed file (e.g. `study_cheatsheets/foo.md`).
- `created` and `updated` — today's date, `YYYY-MM-DD`.
- `series_phase` — set to `architected`.
- `posts[]` — one entry per planned post from the breakdown. Set each post's `n`, `slug` (the `YYYY-MM-DD-<title-slug>` stem), and `title`. Leave `gate: none` and `status: planned`.
- `log` — append one line: `"<YYYY-MM-DD> architected: series planned (<N> posts)"`.

Do not invent fields. Use only what the template defines. Leave `current_post: 0` until a post is actually being worked.

Also create `docs/blog/<slug>/voice-feedback-log.md` from
`docs/blog/_templates/voice-feedback-log.template.md` (substitute the slug into the heading,
keep it otherwise empty). This gives the voice loop a home from the first post, so corrections
captured later (by `/blog-review` or `/blog-voice note`) always have a file to append to.

## Voice reference

Any sample prose you write during architecture — hooks, beat descriptions, the through-line paragraph — follows the `nikhil-brand-voice` skill. Motivate before naming, no AI throat-clearing, no significance inflation, precise terms defined inline. A hook is a real opening question, not a table-of-contents line.

## Terminal state

After the user approves the design and you've written `series-design.md` and `manifest.yaml`, stop. Tell the user:

> Series design and manifest are written to `docs/blog/<slug>/`. Run `/blog-research` to gather and cite sources for the series.

Do NOT auto-proceed to research, planning, or any other phase. The next move is the user's.
