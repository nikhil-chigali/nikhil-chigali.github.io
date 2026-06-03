---
title: "Why T=0 Doesn't Give You the Same Answer Twice"
date: 2026-06-02 09:00:00 +0530
categories: [machine-learning, llms]
tags: [llm, decoding, determinism, inference, decoding-llms]
math: false
---

*Part 2 of [Decoding LLMs](/tags/decoding-llms/), a series on what happens after a model produces its raw output.*

## A model that should repeat itself

> **Same prompt, temperature zero, sent twice — why are the answers different?**
{: .prompt-tip }

You set `temperature` to 0. To be safe, you pin a `seed` too. You send the exact same prompt to a production API, wait, and send it again, byte for byte. The two completions come back different. Not wildly different, sometimes a single word, but different. And you were told that `T = 0` means deterministic.

This is not an academic annoyance. It bites the moment you try to reproduce a bug a user reported, cache a response so you don't pay for it twice, or write a test that asserts the model returns a specific string. Each of those assumes the same input gives the same output. At `T = 0`, you expected that assumption to hold.

The resolution turns on a distinction that most explanations of temperature skip right over. The seven-step pipeline from [Part 1](/posts/the-knobs-that-shape-the-next-token/) is the map: logits come out of the model, get reshaped and trimmed, and one final draw picks the token. This post zooms in on step 7, that final draw, and on the logits feeding into it.

## The case for determinism

Start with the argument you already half-believe, and give it full strength. In Part 1 we saw what temperature does to the distribution as it shrinks: softmax piles more and more probability onto the single highest logit, and in the limit, all of it lands there. So implementations don't bother running the arithmetic at `T = 0`. They define it to mean **greedy decoding**: take the token with the highest logit, the argmax, and skip the random draw entirely.

Now look at what that leaves. The argmax of a fixed list of numbers is a fixed result. The largest number in `[2.1, 5.3, 0.8]` is 5.3 today and 5.3 tomorrow. There is no random number drawn, so there is nothing for a `seed` to control. Run the same prompt twice and step 7 returns the same token at the first position, which fixes the input to the next position, which fixes its argmax too. Walk that forward and both runs produce the same token at every step, and therefore the same completion.

The argument is airtight — *if the logits are the same on both runs.*

## Two kinds of determinism

The argument in the last section is correct. So if the answers still differ, the only way out is that its premise fails: the logits were not the same on both runs. The puzzle was never about the draw. It was about the numbers being drawn from.

That splits "deterministic" into two claims that get quietly bundled into one. The first is **sampling determinism**: given a fixed list of logits, the token you pick is a fixed result. At `T = 0` that pick is the argmax, the position of the largest number, and the largest number in a fixed list does not move. Nothing random is left once the logits are fixed, so there is nothing for a `seed` to touch. This claim is settled.

The second is **inference determinism**: whether the model hands you the same list of logits every time you send it the same input. This is a property of the whole serving stack, the kernels and the batching and the hardware that runs the forward pass, not of the sampler sitting at the end. And in production, nothing guarantees it.

This is the reframe. `T = 0` buys you deterministic *sampling*, not deterministic *inference*. It nails down the draw and says nothing about the scores the draw reads from.

![A split diagram. From a T=0 "take the argmax" node, two panels branch: a green "sampling determinism" panel — given fixed logits, the argmax is a fixed fact, same scores in, same token out — and an amber "inference determinism" panel — whether the logits are the same list on every run, which production does not guarantee. T=0 fixes the draw, not the scores it draws from.](/assets/img/posts/2026-06-02-why-t0-doesnt-give-you-the-same-answer-twice/determinism-split.svg)

The real question, then, is where the logits could change between two identical requests. That is the next section.

## Where the logits drift

The same request should produce the same logits. So where do they change? Walk up the stack from the metal, and three layers each have a way to move the numbers.

**The hardware layer.** Floating-point addition is not associative: `(a + b) + c` can land on different last bits than `a + (b + c)`, because each addition rounds to a fixed number of bits and the rounding depends on the running total. A GPU computes one logit by summing thousands of products at once, spread across many threads, and the order in which those partial sums combine depends on how the work gets scheduled. Change the order, change the last bits.

The order is not fixed across runs, and here is the part that surprises people: it depends on **batch composition**. A production API does not run your request alone. It packs your tokens into a batch with whoever else is calling in that same millisecond. A different set of neighbors makes a different batch shape, a different batch shape selects a different GPU kernel, and a different kernel sums the products in a different order. You never see the other requests, but they are in the arithmetic that produces your logits. This is the most common source of drift in real APIs.

**The model layer.** Above the hardware sits the model itself, and it may not be the one you think you are calling. Providers update weights behind a stable endpoint name without telling you, so the `gpt-4` you hit today can be a different set of parameters than yesterday. That is why you pin a dated snapshot like `gpt-4-0613` when you need a run to be reproducible: the date freezes the weights. There is a subtler version inside the model itself. A **Mixture-of-Experts** model routes each token to a small subset of its expert networks rather than running all of them, and that routing decision can depend on the batch the token rides in. The same token can take a different path on a different run, and a different path produces different logits.

**The input layer.** At the top of the stack is the prompt, and the prompt the model actually reads is often not the one you typed. A serving stack wraps your text in context you never sent: a timestamp, your user or session metadata, a system prompt that an A/B test quietly swapped since yesterday. So two requests you would call identical reach the model as different strings. Different input, different logits, by definition.

![A three-layer stack of reasons identical requests get different logits. Hardware: GPU floating-point isn't associative, and batch neighbors change the kernel path. Model: providers update versions silently, and Mixture-of-Experts routes tokens differently per batch. Input: injected timestamps, user metadata, or an updated system prompt move the logits.](/assets/img/posts/2026-06-02-why-t0-doesnt-give-you-the-same-answer-twice/drift-stack.svg)

Each of these nudges the logits by a tiny amount, often far below what you would guess could matter. The next section shows why a nudge that small is enough to flip the answer.

## When the margin is thinner than the math

Strip the whole post down and it comes to one decision. At `T = 0` the model emits the token with the highest logit, and almost always that token wins by a comfortable margin. The leader sits a full point or more above the runner-up, and the tiny wobbles from the last section move the last few bits of each score without touching the order. The same token comes out on top every run. So most of the time `T = 0` does exactly what you were promised: send the prompt twice, get the same answer twice.

The break is at the near-ties. When the top two logits are separated by less than the size of a single floating-point rounding step, a wobble of one bit can make the second-place score the larger one. The argmax picks the other token, and from that step forward the two runs are decoding different prefixes. One swapped token at one position is enough to send the completions down separate paths.

Watch it on a concrete case. Ask the model to call a coin: "I flipped a coin. It landed on ___". There is no right answer, so "heads" and "tails" come out all but tied — say "heads" at 9.731043 and "tails" a few millionths behind it. On the first run the partial sums for "heads" round up just enough to keep it ahead, and the argmax returns "heads". On the second run the same products are summed in a different order, the last bits round the other way, "tails" edges past, and the argmax returns "tails". Same prompt, same temperature, deterministic *sampling* on both runs. The token still changed.

![Two runs of the same T=0 prompt "I flipped a coin. It landed on". The top two logits, for "heads" and "tails", sit about 0.000003 apart, because the coin gives the model no reason to prefer one. In Run 1 heads edges ahead and is the argmax; in Run 2 a different sum order rounds the other way and tails wins. Same prompt, same temperature, different word.](/assets/img/posts/2026-06-02-why-t0-doesnt-give-you-the-same-answer-twice/argmax-flip.svg)

This is not constant chaos. Most steps are not near-ties, so most of the output holds steady run to run. The flip shows up exactly when two continuations were almost equally good — which is also the moment you are least likely to notice the swap, because both words read as fine.

That is the whole resolution. `T = 0` gives you deterministic *sampling*, not deterministic *inference*. The randomness you switched off was never where the variation came from; it was living one floor down, in the logits the sampler reads. Pinning the temperature pins the draw and leaves the scores free to move.

If you actually need a run you can reproduce, the levers are in the inference stack, not on the temperature dial. Pin a dated model version so the weights stay put. Request a fixed seed where the provider offers one. And accept that batched serving can still wobble the last bits, so byte-for-byte reproducibility is a goal you approach, not one you are handed.

[Part 3](/tags/decoding-llms/) picks up the same misread from the other side. Reaching for the temperature dial felt like the fix here, and it half was. Next time the reach comes back for a problem the dial cannot touch at all.
