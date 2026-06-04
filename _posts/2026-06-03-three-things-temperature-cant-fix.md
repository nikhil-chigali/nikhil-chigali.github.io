---
title: "Three Things Temperature Can't Fix"
date: 2026-06-03 09:00:00 +0530
categories: [machine-learning, llms]
tags: [llm, decoding, structured-outputs, safety, decoding-llms]
math: false
---

*Part 3 of [Decoding LLMs](/tags/decoding-llms/), a series on what happens after a model produces its raw output.*

## The first knob becomes the only knob

> **When the output is wrong, is reaching for the temperature dial the fix — or a reflex?**
{: .prompt-tip }

Temperature is the first decoding control anyone meets. It sits in every quickstart, every tutorial, every "getting started" snippet, so it becomes the one tool you know you have. And when the only tool you reach for is a hammer, every bad output starts to look like a nail.

[Part 1](/posts/the-knobs-that-shape-the-next-token/) built that dial from the logits up. [Part 2](/posts/why-t0-doesnt-give-you-the-same-answer-twice/) showed where it quietly slips, why `T = 0` still gives you two different answers. This post is the other failure mode: three problems where the dial is the wrong tool from the start.

Each one is a real complaint. Each comes with a temperature "fix" that feels right and isn't. And each has a different lever that actually moves the thing you care about.

## "My output keeps repeating itself"

The model gets stuck. "The best way to learn is to practice, the best way to learn is to practice," the same clause circling back on itself. The output is too repetitive, so you reach for the one knob you know controls randomness and turn the temperature *up*. More randomness, surely, means less of the same thing over and over.

It helps a little, and it is still the wrong tool. Turning the temperature up sprays randomness across every choice the model makes, so to break one repeated phrase you loosen the whole output and lose some of its coherence — and the model can still drift back to a wording it favors. The opposite move is worse. Reaching for a *lower* temperature to make the model behave sharpens the distribution toward the tokens that already score highest, which are the exact tokens the loop keeps picking, so the rut only gets deeper. The greedy loop from Part 1 is this at its limit: at `T = 0` the model always takes the top token, so it loops the hardest of all. Either way the dial is aimed at the wrong thing. Temperature knows nothing about what the model has already said, and repetition is entirely about that history.

The lever that works acts on a different thing entirely. Instead of reshaping the whole distribution, it reaches into the output already on the page and pushes down the tokens you have used. Two knobs do this, and they do it differently. A **frequency penalty** subtracts from a token's logit in proportion to how many times that token has already appeared, so a word you have used five times is pushed down five times as hard as a word you have used once. A **presence penalty** subtracts a flat amount the moment a token has appeared at all, once, regardless of how many times after that.

![Two penalty schemes on the same two tokens. "moonlight" has appeared three times, "silver" once. Frequency penalty cuts each token's score in proportion to its count, so moonlight is pushed down three times as far as silver. Presence penalty applies one flat cut to any token that has appeared at all, so moonlight and silver are pushed down by the same amount.](/assets/img/posts/2026-06-03-three-things-temperature-cant-fix/repetition-penalties.svg)

The same idea wears other clothes depending on whose API you are using, so it helps to recognize the family:

- **`frequency_penalty` and `presence_penalty`** — the additive, OpenAI-style pair above: subtract from a token's logit by count, or by mere presence.
- **`repetition_penalty`** — HuggingFace's [multiplicative version](https://huggingface.co/docs/transformers/main_classes/text_generation): it divides the logit of any token already seen, the prompt included, rather than subtracting from it. From the [2019 CTRL paper](https://arxiv.org/abs/1909.05858); typical values run 1.1 to 1.3.
- **`no_repeat_ngram_size`** — the blunt hard rule next door: forbid any n-gram of that length from ever occurring twice.

One mechanism underneath all of them — lean away from what you have already said — in a handful of forms.

Here is the part that gets skipped. None of these penalties know *which* repetition is the bad one. They see that a token repeated, not that it should not have.

> Push them too high and they start suppressing the words you genuinely need to reuse: "the", "is", a character's name in a story. The text frays as the model contorts to avoid words it ought to say. **You tune these knobs, you don't crank them.**
{: .prompt-warning }

Land it on a concrete case. "My poems all reuse the same imagery across generations" sounds like a repetition problem, and it is, but it is a *presence* problem: you want new concepts to show up at all from one poem to the next, not to limit how often a word repeats inside one. That is the presence penalty's job, not the frequency penalty's, and certainly not the temperature's. For the additive pair, both around 0.3 to 0.8 is a sane starting point.

## "I need valid JSON every time"

You call the model in a pipeline that expects JSON back. Most of the time it returns clean JSON. Then one call in fifty comes back with a stray sentence before the brace, or a trailing comma, or a quote that never closes, and the parser throws. The output has to match a fixed schema every single time, and it doesn't. So you drop the temperature, on the theory that a calmer model will stop improvising and start behaving.

It won't, and the reason is in what a prompt actually is. "Please return JSON" is a *request* you hand to a sampler, not a *rule* the sampler has to obey. The sampler still does what Part 1 described: it reshapes the logits and draws a token. At `T = 0` that draw is the argmax, the highest-scoring token at each position, and nothing in your instruction reaches down to guarantee that the highest-scoring token keeps the JSON well-formed. If a stray token scores highest somewhere in the middle, that is the token you get. Lowering the temperature makes the output more *predictable*, the same call drifts less from run to run, but predictable is not the same as valid. Format is a property of the token sequence. Temperature only reshapes the odds over tokens. It never decides which sequences are allowed.

The fix is to stop asking and start enforcing, and that means moving the guarantee out of the prompt and into the decoder, the step that turns logits into tokens. There is a ladder here, from weak to strong. The bottom rung is the prompt instruction you already tried: "return JSON." A step up is few-shot examples, where you show the model two or three filled-in responses so it copies the shape. Both of these still only *ask*. The middle rung stops asking and starts checking: validate the output after the fact, and if it fails to parse, call again. That catches the bad ones but pays for every retry. The top rungs build the guarantee into the decoder itself. JSON mode constrains the model to emit syntactically valid JSON. And the strongest rung is **constrained decoding**: at every step, the decoder masks out any token that would break the schema — sets its probability to zero before the draw — so the model literally cannot emit it. The bad token isn't unlikely. It isn't on the menu.

![A weak-to-strong ladder for getting a fixed output format. Bottom rungs only ask: a prompt instruction, then few-shot examples. The middle rung checks after the fact: validate and retry. The top rungs enforce: JSON mode guarantees valid JSON, and constrained decoding masks invalid tokens so the schema cannot be broken. A dashed line marks where the format becomes guaranteed.](/assets/img/posts/2026-06-03-three-things-temperature-cant-fix/enforcement-ladder.svg)

That dashed line on the ladder is the whole point of the section.

> Prompting *asks* for a format; structured outputs *enforce* it.
{: .prompt-tip }

The practical default, when you need the schema to hold every time, is to climb above the line rather than reach for a lower temperature. Every major provider now ships a way up there:

- **OpenAI** — a JSON schema through [`response_format`](https://developers.openai.com/api/docs/guides/structured-outputs), held to exactly (since August 2024).
- **Google** — the same through Gemini's [`response_schema`](https://ai.google.dev/gemini-api/docs/structured-output).
- **Anthropic** — [constrained decoding and strict tool-use schemas](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) (added November 2025).

The detail varies, but the move is the same: you hand the API the schema, and the decoder keeps the output inside it.

> **The guarantee is not free.** Masking a token bends the model away from what it would have said: when the token it wanted is forbidden, that probability reshuffles onto the tokens that survive the mask, and under a tight grammar that can measurably dent the quality of what comes back. Spend constrained decoding where the schema has to hold, not on every call out of habit.
{: .prompt-warning }

One limit comes with you into the next problem. Enforcement guarantees the *shape* of the answer, never the *substance*. A response can be flawless, well-formed JSON and still put a wrong number in the field. Constrained decoding fixes whether the output *parses*, not whether it is *true* — and "true" is the next thing people expect the temperature dial to deliver.

## "Set the temperature to zero so it's safe"

The last section left enforcement with a hole in it. Constrained decoding pins the *shape* of the answer and says nothing about its *substance*: the JSON parses, the field is filled, and the number in it can still be wrong. That gap is small in a format checker. Move it up one level, to whether the answer is correct at all, and it is where the last reflex lives.

Picture the setting that triggers it. The app is high-stakes, a symptom checker, a contract reviewer, a tool that quotes a price, and a wrong answer costs something real. So someone reasons: randomness is what makes the model unreliable, kill the randomness, set `T = 0`, and now the system is safe and deterministic.

It isn't, and the reason is that `T = 0` buys you a *consistent* answer, not a *correct* one. Lowering the temperature sharpens the distribution toward the model's top-scoring token, which fixes what the model says. It does nothing about whether that top token was right in the first place. If the model's favorite answer is wrong, `T = 0` is the setting that hands that same wrong answer to every user, on every call, forever. You have not removed the error. You have made it reproducible.

These are two different axes, and the temperature dial only moves along one of them. *Consistency* is how much the answer changes from run to run. *Correctness* is whether the answer matches the truth. Turning the temperature down walks you toward the consistent end of the first axis and leaves your position on the second exactly where it was.

![A 2x2 grid. The horizontal axis is correctness, increasing to the right, driven by RAG, tools, and guardrails. The vertical axis is the temperature dial, pointing down: lowering the temperature moves you down the grid, toward more consistent. The bottom row is the consistent row, and its left cell — consistent and wrong — is the trap, the same wrong answer to every user. Lowering temperature walks you down into a consistent cell but never right into a correct one.](/assets/img/posts/2026-06-03-three-things-temperature-cant-fix/consistency-correctness.svg)

And `T = 0` does not even deliver the consistency it promises. [Part 2](/posts/why-t0-doesnt-give-you-the-same-answer-twice/) is the whole story: in production, batching and floating-point arithmetic let the logits drift between two identical requests, so the argmax can flip and the "deterministic" setting returns two different answers anyway. The safe-because-deterministic argument fails on its own terms before it ever reaches the question of correctness.

Correctness lives on the other axis, and you move along it by changing where the answer comes from, not how sharply it is sampled:

- **Retrieval-augmented generation (RAG)** — pull the facts from a vetted source and have the model write from those, instead of free-generating them.
- **Tool calls** — for any value with a ground truth (a lab result, a dose, a current price), call a tool rather than letting the model produce the digits from memory.
- **Guardrails and refusals** — put hard checks in front of inputs the system should not answer, so an out-of-scope or emergency query hits a refusal instead of a confident guess.
- **Escalation** — set a confidence threshold below which the request goes to a human.

None of these touch the temperature. All of them move correctness.

There is one more turn, and it runs against the reflex. A *little* randomness gives you one of the cheapest error checks you can run. Sample the same prompt several times and check whether the answers agree — **self-consistency**, the idea [Wang et al. introduced in 2022](https://arxiv.org/abs/2203.11171) — and the spread tells you something the single answer can't: when the samples converge, the model is steady on that answer; when they scatter, it isn't, and that is your cue to flag it, retrieve more, or escalate.

> At `T = 0`, every run returns the same answer, so there is no disagreement to measure and nothing for this check to catch. The setting people reach for to feel *safe* is the one that quietly throws away their cheapest way to notice the model is wrong.
{: .prompt-tip }

## A dial for every job

Every parameter in this table has already shown up somewhere in the series, so read it as a recap rather than a lookup you take on faith.

| Scenario | Temperature | top-p | Reach past the dial for |
|---|---|---|---|
| Classification (URGENT / NORMAL / SPAM) | 0 | — | Structured output, or read the class logits directly |
| Code generation | 0–0.2 | 0.95 | Stop sequences |
| Factual Q&A / chatbot | 0–0.3 | 0.9 | RAG and tool calls for ground-truth values |
| Summarization (with human review) | 0.3–0.5 | 0.95 | — |
| Creative writing | 0.8–1.0 | 0.95 | Frequency and presence penalties around 0.5 |
| Brainstorming / ideation | 1.0–1.2 | 0.95 | A high presence penalty for variety |
| Safety-critical (medical / legal, direct to user) | low, but not sufficient on its own | — | RAG, guardrails, escalation, refusal patterns |

The right-hand column is where the three problems all landed.

> Temperature controls *how* the model samples, not *what* it is allowed to say or *whether* it is right. For those, you reach past the dial.
{: .prompt-tip }

A penalty, a constrained decoder, a retrieval step, a guardrail — the dial shapes the odds over tokens and stops there. Everything else lives in the column on the right.

That is the arc across three posts. Part 1 built the dial from a vector of logits up. Part 2 found its limits, the spot where `T = 0` still hands back two different answers. Part 3 walked the failures the dial was never going to touch. Put the three together and you have a model of the whole decode, from the raw scores the network produces to the single word that lands on the screen, and a sense of which control to reach for when that word comes out wrong.

If you arrived here first, [the rest of the series](/tags/decoding-llms/) is where the dial gets built before it gets pushed past.