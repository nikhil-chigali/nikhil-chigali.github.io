---
title: "The Knobs That Shape the Next Token"
date: 2026-06-01 09:00:00 +0530
categories: [machine-learning, llms]
tags: [llm, decoding, sampling, temperature, decoding-llms]
math: true
---

*Part 1 of [Decoding LLMs](/tags/decoding-llms/), a series on what happens after a model produces its raw output.*

## Picking a word out of fifty thousand

You type a prompt, hit enter, and a word appears.

> **Where does that word come from?**
{: .prompt-tip }

The last thing a language model does, before any text shows up, is produce a list of numbers. One number for every token it knows — every word, word-piece, and punctuation mark in its vocabulary. For a typical model that vocabulary runs to tens of thousands of entries, so the model hands back tens of thousands of numbers, all at once.

Each of those numbers is a **logit**: an unnormalized score the model assigns to a token. A higher logit means the model favors that token more as the next one. The logits are not probabilities yet. They can be negative, they can be large, and they don't add up to anything in particular. They are raw scores, nothing more.

So at the moment just before you see a word, the model isn't holding a word at all. It is holding a list of fifty thousand scores. The whole rest of this post answers one question: how does that list collapse into the single next word you actually read?

## "Just pick the most likely one"

The obvious answer is to take the token with the highest logit. The model already told you which one it favors most, so read that score off the list, emit that token, and repeat for the next position. This is **greedy decoding**: at every step, pick the single highest-scoring token and never look back.

It works, and for a sentence or two it often reads fine. Then you notice two things.

**It's deterministic.** The highest logit is a fixed fact about the list, so the same prompt produces the exact same continuation every time you run it. Ask for a birthday message twice and you get the identical sentence, word for word. There is no second take.

**It collapses into loops.** Once the model lands on a phrasing it scores highly, that phrasing makes the same high-scoring continuation even more likely next time, and greedy decoding has no reason to step off the path. You get output like:

> The best way to learn is to practice. The best way to learn is to practice. The best way to learn is to practice.

The deeper problem is hiding underneath both symptoms. Taking the most likely token at each step does not give you the most likely sentence. A token that scores second-best right now can open onto a far better continuation three words later, and greedy decoding throws that branch away before it ever sees it. It commits to whatever looks best locally, and it never surprises you.

What we want is the freedom to sometimes pick the second- or third-best token instead of the top one. That means treating the list of scores as a distribution to draw from, not a maximum to read off. To do that, two things have to fall into place: we need to turn those raw logits into probabilities, and we need a way to control how adventurous the draw is.

## Temperature: a dial for how random

Drawing from a distribution needs an actual distribution: positive numbers that sum to 1. The standard way to get one from logits is **softmax**. It exponentiates each score and divides by the sum of all the exponentials, which makes every result positive and forces the whole list to add up to 1. Higher logits get more probability, lower logits get less, and nothing is thrown away.

Softmax alone gives you one fixed distribution. To control how adventurous the draw is, we add a single knob to it. That knob is **temperature**, written $T$, and it sets how spread-out the resulting distribution comes out.

So how do we widen or narrow the gaps between scores before normalizing them? Slip $T$ into softmax as a divisor on each logit:

$$P(\text{token}_i) = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$$

where $z_i$ is the logit for token $i$.

Dividing every logit by $T$ before exponentiating rescales the gaps between the scores. A small $T$, below 1, stretches the gaps apart, so the top token's probability climbs toward 1 and the distribution sharpens to a spike. A large $T$, above 1, squeezes the gaps together, flattening the distribution toward uniform.

![Same logits rendered as probabilities at three temperatures: at T=0.3 the top token "the" takes almost all the probability; at T=1.0 the distribution is moderate; at T=1.8 the five tokens are nearly level](/assets/img/posts/2026-06-01-the-knobs-that-shape-the-next-token/softmax-temperature.svg)

The figure runs the same five logits through three temperatures, and you can watch the peak melt as $T$ rises. At $T=0.3$ the token "the" holds about 0.96 of the probability and the rest are slivers. At $T=1.8$ that same token drops to about 0.40 and the five tokens sit nearly level.

A few parts of this trip people up.

- **The range is 0 to 2, not 0 to 1.** The knob does not stop at 1; pushing past it is how you make a model wilder than its raw scores suggest.
- **$T=0$ is not a division by zero.** As $T$ shrinks toward 0, the distribution piles all of its mass onto the single highest logit. That is exactly the greedy decoding from before, so implementations define $T=0$ to mean "take the argmax" and skip the arithmetic.
- **Temperature reshapes; it never deletes.** Even at low $T$, every token keeps a nonzero probability, a tiny one for the long tail of unlikely tokens.

> Providers don't agree on the ceiling. OpenAI's API takes a `temperature` from 0 to 2 and defaults to 1; Anthropic's takes 0 to 1, also defaulting to 1, and won't go higher. So `temperature = 1` is the midpoint of OpenAI's range but the maximum of Anthropic's — check the docs before assuming 1.5 is even a legal value.
{: .prompt-warning }

That surviving tail raises a question we have stepped past: given a distribution like this, how does a single token actually come out of it?

## What "drawing" a token actually means

We keep saying *draw* and *sample*. If your background is classification, the instinct is to read off the highest-probability token and stop. That instinct is greedy decoding again, and we already saw where it leads. Sampling is a different move.

Picture the distribution as a strip of length 1, with every token holding a piece of it as wide as its probability. The token at 0.62 covers most of the strip, a token at 0.27 takes a shorter stretch, and the long tail splits the thin piece left over. To draw a token, pick a single random number between 0 and 1 from a uniform distribution, then read off whichever token's piece it lands on. That token is what you emit.

![A strip from 0 to 1 split into slices sized by probability: summer at 0.62 takes most of it, winter 0.27, autumn 0.10, and a thin grey tail. A random number of 0.71 lands in the winter slice, so winter is the token drawn rather than the most likely one](/assets/img/posts/2026-06-01-the-knobs-that-shape-the-next-token/sampling-strip.svg)

Because each piece is as wide as its token's probability, the likely tokens come up most of the time and the unlikely ones still surface once in a while. A piece of width 0.62 catches the random number about 62 times in 100; a one-in-a-thousand token catches it about once in a thousand.

> **Greedy decoding is just sampling with the dice removed:** skip the random number and always stand on the widest slice.
{: .prompt-tip }

Every knob in this post feeds into this one draw. Temperature, top-k, and top-p all act before it, stretching the pieces or removing some outright. The draw itself never changes; the strip it lands on does. Which puts the spotlight back on that long tail, because it still owns a sliver of the strip.

## The leftover problem: cutting off the tail

A nonzero probability is still a probability. A token sitting in the tail at one-in-a-thousand looks harmless on a single draw, but you don't draw once. A paragraph is hundreds of tokens, and at every position you reach back into the distribution and sample again. Run a one-in-a-thousand event a few hundred times and it stops being rare. Sooner or later that junk token gets drawn.

![At the prompt "My favorite season is", the next-word odds are summer 0.62, winter 0.27, autumn 0.10, with "penguin" far down the tail at 0.0008. That tail token gets drawn this time, derailing the continuation into "My favorite season is penguin, which falls in the months between October and the harvest"](/assets/img/posts/2026-06-01-the-knobs-that-shape-the-next-token/tail-derailment.svg)

One bad draw is all it takes. A single absurd word lands in the middle of a sentence, and the model now conditions everything after it on that word being there. The continuation bends to make sense of nonsense, and the rest of the generation follows it off the cliff.

So we want to remove the tail before we sample, not hope to dodge it. Cut the unlikely tokens out of the running entirely, then draw only from what's left.

## Top-k and top-p

The obvious cut is to keep a fixed number of tokens and drop everything else. Sort the tokens by probability, keep the top few, throw the rest away, and renormalize the survivors so they sum to 1 again before you sample. This is **top-k**: keep the `k` highest-probability tokens and discard the tail. A typical `k` is 40 to 50.

This helps, and then you watch it break on two distributions that pull in opposite directions.

Take a position where the model is confident. One token, say the word after "the United States of", holds 0.95 of the probability on its own. With `k = 40`, you keep that token and 39 others, almost all of them near zero. You've kept 39 candidates that had no business being in the running, and on a flat enough day the renormalization hands them more weight than they earned.

Now take a position where the model is genuinely uncertain. The next word could reasonably be any of two hundred things, and the probability is spread thinly across all of them. With `k = 40`, you keep 40 and chop off 160 perfectly good candidates. The model had a wide, legitimate set of options and you threw most of them out.

The same `k` is wrong in both cases, and for the same reason. `k` is a fixed count. It can't see whether the distribution is a tall spike or a low plateau, so it keeps too many tokens when the model is sure and too few when the model is hedging.

The fix is to stop counting tokens and start measuring probability mass. Sort the tokens by probability, then walk down the list adding them up until the running total reaches `p`. Keep exactly that set, the smallest group whose probabilities sum to `p`, discard the rest, renormalize, and sample. This is **top-p**, also called nucleus sampling, with a typical `p` of 0.9 to 0.95.

> top-k commits to a fixed *number* of tokens; top-p commits to a fixed *amount* of probability. That single difference is the whole reason top-p adapts to confidence and top-k can't.
{: .prompt-tip }

Run the same two positions through it. In the confident case, the 0.95 token already clears a `p` of 0.9 by itself, so top-p keeps one token, maybe two, and the 39 near-zero candidates never enter the draw. In the uncertain case, no single token carries much mass, so the keep-set has to grow wide, pulling in many tokens before the total reaches 0.9. The cutoff moved on its own, because it watches the model's confidence instead of a token count.

![A comparison of top-k and top-p on the same two steps. Top-k keeps a fixed 40 tokens in both cases: 39 near-zero junk tokens ride along when the model is confident, and 160 good options get cut when the model is uncertain. Top-p keeps 1 token in the confident case and about 140 in the uncertain case, adapting to the model's confidence](/assets/img/posts/2026-06-01-the-knobs-that-shape-the-next-token/topk-vs-topp.svg)

Both filters leave the same loose end. Once you throw tokens away, the survivors no longer sum to 1, and the strip from earlier no longer fills its full length. Renormalizing repairs that: divide each surviving probability by the total that survived.

$$P'(\text{token}_i) = \frac{P(\text{token}_i)}{\sum_{j \,\in\, \text{kept}} P(\text{token}_j)}$$

The kept tokens stretch back out to fill the whole 0-to-1 strip, in the same proportions they had before, so the random draw has a complete range to land in.

That adaptive cutoff is the second knob, sitting alongside temperature. With both in hand, the question is how they stack.

## Putting it together: the decoding pipeline

Every token you have read about happens in a fixed order, one stage feeding the next. The whole run from raw scores to a single word goes like this:

1. The model produces raw logits, one per token in the vocabulary.
2. Divide every logit by the temperature $T$.
3. Apply softmax to turn the scaled logits into a probability distribution.
4. Apply the top-k filter, dropping all but the $k$ highest-probability tokens.
5. Apply the top-p filter, dropping the tail past cumulative probability $p$.
6. Renormalize the survivors so they sum to 1.
7. Sample one token from what is left.

![A vertical flowchart of the decoding pipeline: raw logits, then divide by temperature, then softmax, then a top-k and/or top-p filter that trims the unlikely tail (often only one of the two is used), then renormalize, then sample one token, producing the next word](/assets/img/posts/2026-06-01-the-knobs-that-shape-the-next-token/pipeline-flow.svg)

> **Steps 4 and 5 rarely both fire.** In practice you reach for one filter, not both: top-p is the common default, and some APIs only offer that one — OpenAI exposes top-p but no top-k, while Anthropic gives you both. When both are set, they run in the order above, top-k narrowing the field before top-p trims what is left.
{: .prompt-info }

The order is the part worth slowing down on. Temperature runs before the filters, so it reshapes the distribution that top-k and top-p then cut from. Change $T$ and you change which tokens are still standing when the filters make their call. The knobs are not independent. Heat first, then trim.

The consequence is concrete. Turn the temperature up and you fatten the tail, which means top-p has to reach further down the list to collect the same probability mass $p$. The nucleus widens. A `p` of 0.9 keeps a tight set at $T=0.7$ and a much looser one at $T=1.5$, off the same logits. The filter setting did not move; the distribution underneath it did.

> **The one-paragraph version.** Softmax turns logits into probabilities; temperature reshapes that distribution, sharper or flatter; top-k or top-p trims the unlikely tail; renormalizing rescales what's left; then one weighted random draw picks the token. Greedy decoding is the same pipeline with the draw swapped for "always take the max."
{: .prompt-tip }

Those seven steps are the map for the rest of this series. Every question that comes later is a question about one of them. Part 2 asks why step 7 doesn't give you the same token twice even when $T=0$ pins the distribution to a single peak. Part 3 asks about the failures none of these steps can fix, the cases where no temperature and no cutoff will save the output. If you want to keep going, [the rest of the series](/tags/decoding-llms/) picks up from here.
