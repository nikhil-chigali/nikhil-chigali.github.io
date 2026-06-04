---
name: nikhil-brand-voice
description: Use when writing, editing, or auditing technical posts on ML/AI topics for Nikhil Chigali's blog. Builds intuition through Feynman-style teaching while maintaining a clear, precise tone free of AI-generated tells.
---

# Nikhil — Brand Voice Skill

## Core Principle

Teach by building intuition. The goal is to make the reader *understand*, not just *finish reading*. Every paragraph should leave them able to think about the concept themselves, not parrot a definition back.

Three commitments:

1. **Build understanding before naming things.** A reader who sees the structure of an idea form before its label can hold both. The reverse rarely works.
2. **Use precise words, plainly.** The right technical term is almost always clearer than a folk substitute. The trick is to define it inline at first use, not to avoid it.
3. **Cut AI-isms ruthlessly.** Hedging, throat-clearing, significance inflation, and tricolon decoration are how generated prose announces itself. They feel persuasive on first read and hollow on second.

## Teaching Architecture

The Feynman shape, applied at any scope from a paragraph to a whole post.

**Motivate.** Open with the question the concept answers, not the concept itself. The reader needs to want the answer before they will absorb it. "How do we measure how wrong a model's predictions are?" lands; "the loss function is defined as..." does not.

**Try the naive thing.** Whenever a non-obvious choice is being made, show the obvious choice first and watch it fail. The factor of $\frac{1}{2}$ in mean squared error, the log in maximum likelihood, the softmax over a raw argmax — every one of these has a "but why not the simpler thing?" question behind it. Answer it before the reader asks.

**Build up to the real answer.** The formula or definition should arrive as the conclusion of a reasoning chain, not the start of one. "We need something that does X, Y, and Z, which gives us this" beats "this is the formula, here's what it means."

**Check on a concrete case.** Close the explanation by running it on a specific example the reader can verify mentally. The example should exhibit the real difficulty of the concept, not hide it behind trivial structure.

**Pick examples that earn their place.** Three properties make an example useful: the reader can picture it without prior context, the math fits in their head, and it surfaces the real difficulty. If it only works because it's trivially structured, find a harder case or name the simplification explicitly.

**Name the weird parts.** Non-obvious conventions — a sign flip, a factor of two, a counterintuitive direction — should be flagged, not papered over. "The minus sign is there because we minimize loss but maximize likelihood" is one sentence and saves the reader thirty seconds of confusion. Reaching for this move is the difference between teaching and reciting.

## Tone Target

Direct, considered, technically precise. The reader should never feel talked down to and never feel buried.

Concretely:

- **Strong specific verbs over generic ones.** "Drops to zero" not "approaches a small value." "Punishes confident wrong predictions" not "imposes a penalty."
- **Concrete nouns over abstract ones.** "The gradient" not "the optimization signal." "Token probabilities" not "the model's outputs."
- **One idea per sentence as the default.** Combine when the second clause is a genuine qualifier, not a separate thought.
- **First person used sparingly and only when the reasoning is genuinely personal.** "I find this framing clearer" yes; "I will now show" no.
- **No throat-clearing.** Start sentences with the actual content.
- **No significance inflation.** If something is important, the reader should feel that from the explanation itself, not from being told it.
- **Use the precise technical term.** Then define it inline. Avoiding jargon by paraphrasing usually produces worse prose than naming the thing and explaining what it means.

## AI-ness Audit

Generated prose has a consistent fingerprint. The phrases below are the strongest tells. None are wrong in isolation; the pattern is the giveaway. Cut on sight.

**Throat-clearing openers**

| Cut | Replace |
|---|---|
| "At its core," | start with the actual claim |
| "In essence," / "Essentially," | cut, the sentence reads the same |
| "Fundamentally," | cut |
| "It's important to note that" | cut, just state it |
| "It's worth noting that" | cut |
| "To put it simply," | cut, then write it simply |

**Significance inflation**

| Cut | Replace |
|---|---|
| "crucial", "vital", "essential", "pivotal" | "important" if true, otherwise cut |
| "game-changing", "revolutionary" | describe what changed specifically |
| "cutting-edge", "state-of-the-art" | name the actual method and year |
| "foundational", "fundamental" (as adjective) | cut |
| "powerful" (applied to a method) | say what it does better than the alternative |

**Corporate verbs**

| Cut | Replace |
|---|---|
| "leverage" | "use" |
| "harness" | "use" |
| "unlock" | "enable", or describe the actual effect |
| "navigate" (a problem) | "handle", "address" |
| "delve into" | "look at", "examine" |
| "dive deep" | cut |

**Structural tells**

- **Tricolons everywhere.** "X, Y, and Z" appearing repeatedly. AI writing loves three-part lists. Vary to two or four when the actual content has that shape.
- **Negation-elevation.** "It's not just X — it's Y." Almost always cuttable; usually X was fine on its own.
- **Balanced "while" clauses.** "While X provides A, Y provides B." Often a fake symmetry imposed on asymmetric content.
- **Em dashes as parentheticals.** "The model — which has billions of parameters — does X." Rewrite as two sentences or use real parentheses.
- **Self-summarizing transitions.** "As we've seen above..." / "Having established X, we now turn to Y." The reader was there. Just continue.
- **Closing with a grand statement.** "This represents a paradigm shift in how we think about..." Cut. End on the substantive last point.

**Hedging fog**

- "may potentially" / "could possibly" — pick one or remove both
- "tends to often" — pick one
- "in many cases" / "in some cases" — if you mean "usually" or "sometimes", say that; if you mean "specifically when X", say that

**The bold-word habit.** Bolding every technical term reads as nervous emphasis. Bold a term once, at first definition, and only when it is a term the reader will need to recognize later. If everything is bold, nothing is.

## Structural Patterns

**Introducing a term**

> framing sentence that creates the need → technical term in bold at first use → one-line plain definition → one sentence on why the term exists

Example: "A model that predicts probabilities can be confidently wrong, and the loss should punish that harder than being unconfidently wrong. **Cross-entropy loss** does this by taking the log of the predicted probability of the correct answer. The log is what makes it work — it explodes as the probability approaches zero, so confident wrong predictions get a large loss."

**Introducing math**

> question the formula answers → bridge ("this gives us:", "what we end up with is:") → equation → variable list only when non-obvious → one sentence describing the *shape* of what the formula does, not a restatement

The shape-not-restatement rule is the one that matters. "$L = -\sum p_i \log q_i$ — here, $p$ is the true distribution and $q$ is the predicted distribution" restates the symbols. "The sum is over outcomes, and each term grows large when the true probability is high but the predicted probability is low" describes what the formula actually does.

**Section openings**

- Open with content, not orientation. "Cross-entropy comes from information theory" not "In this section, we will discuss cross-entropy."
- If a transition is needed, make it substantive: "The same idea shows up when we ask how surprised the model should be by the true answer."

**Section closings**

- End on the substantive last point. No "in summary", no "as we have seen", no "this lays the groundwork for".
- If the next section follows naturally, the reader will feel it. If it does not, fix the structure, not the transition.

## Grammar Pitfalls

**Redundant locative prepositions**

- ❌ "the slope of the cost surface at wherever we currently are"
- ✅ "the slope of the cost surface wherever we currently are"
- Don't prefix `wherever`/`whenever`/`however` with a preposition that duplicates its meaning.

**Mismatched subjects joined by `and`**

- ❌ "Logistic regression is a supervised algorithm, and a bit of calculus will go a long way."
- ✅ "Logistic regression is a supervised algorithm. A bit of calculus will go a long way."
- When `and` joins clauses with different subjects and the second is a separate thought, split into two sentences.

**"X is when" definitions**

- ❌ "Joint probability is when multiple events occur together."
- ✅ "Joint probability is the probability that multiple events occur together."
- Use the matching noun form, not a temporal clause.

## Before / After Examples

The target sits between AI-inflation and casual-filler. Compare three flavors:

**Topic: introducing gradient descent**

*AI-ish (avoid):*
> "Gradient descent is a foundational optimization algorithm that lies at the heart of modern machine learning. By iteratively leveraging the gradient of the loss function, it enables models to navigate the loss landscape and converge toward optimal parameters. This powerful technique has revolutionized how we train neural networks."

*Casual-filler (also avoid):*
> "So how do we actually train the model? That's where gradient descent comes in, and honestly it's the step that matters most. The basic idea is pretty simple — we just follow the slope downhill."

*Target:*
> "Training a model means finding parameters that make the loss small. Gradient descent does this by computing the slope of the loss with respect to each parameter and stepping in the opposite direction. The slope points toward where the loss increases fastest; the opposite direction is therefore the steepest local decrease. Repeat the step, and the parameters drift toward a minimum."

What changed: the AI version inflates significance and uses corporate verbs. The casual version pads with filler. The target states the goal, defines the method by what it computes, and explains the geometric reason it works. No filler, no hype, no labels-before-substance.

---

**Topic: the log in maximum likelihood**

*AI-ish:*
> "It is important to note that multiplying many small probabilities together can lead to numerical underflow. Therefore, the log transformation is essentially crucial. By taking the log, we leverage the fact that maximizing the log-likelihood is equivalent to maximizing the likelihood itself, since the log function is monotonically increasing."

*Target:*
> "Multiplying many small probabilities together drives the product to zero faster than floating-point can represent. The fix is to take the log, which turns the product into a sum and keeps the numbers in a workable range. This is safe because $\log$ is monotonically increasing — the $\theta$ that maximizes $\log P(\text{data} \mid \theta)$ is the same $\theta$ that maximizes $P(\text{data} \mid \theta)$."

What changed: cut "it is important to note", "essentially", "crucial", "leverage". State the problem concretely (underflow, and why). State the fix and what it gives (product becomes sum, range stays workable). State the justification with the actual reason ($\log$ is monotonic, so the argmax is preserved).

## Final Pass: Self-Audit

Before publishing, run through:

- [ ] Does every section open with content, not orientation?
- [ ] Does every formula answer a question already raised in the text?
- [ ] Are concepts motivated before being named?
- [ ] Are weird conventions (sign flips, factors, choices) flagged explicitly?
- [ ] Are examples small enough to verify mentally, and do they exhibit the real difficulty?
- [ ] Have I cut all of: "essentially", "fundamentally", "leverage", "delve", "crucial", "in essence", "at its core", "it is worth noting", "powerful"?
- [ ] Are em dashes doing real work, or are they parentheticals in disguise?
- [ ] Are bolded terms doing real work, or just decoration?
- [ ] Does the closing land on the substantive last point, not on a grand summary?