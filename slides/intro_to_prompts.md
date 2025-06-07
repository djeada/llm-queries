# Intro to Prompt Engineering

Large language models behave a bit like improv actors: given a short cue, they spin an entire story. *Prompt engineering* is the craft of writing those cues so that the model’s continuation lands exactly where we need it. At first glance a prompt looks like plain text, yet in practice it is a carefully tuned control signal that shapes probabilities inside the neural network. 
## In-Context Learning Fundamentals

When the model reads a prompt $x_{1{:}t}$ it internally computes

$$
p_\theta(x_{t+1}\mid x_{1{:}t}),
$$

then samples or selects the next token and appends it to the context. No gradient ever flows during this inference pass, so all “learning” happens purely in activations. Because the weights stay frozen, we call the phenomenon *in-context learning* rather than fine-tuning.

### What “K-Shot” Really Means

If the prompt embeds $K$ solved examples followed by an unsolved one, the conditional becomes

$$
p_\theta(y\mid x, D_{1{:}K}) \quad\text{with}\quad D_i=(x_i,y_i).
$$

Here the demonstrations $D_{1{:}K}$ act like a mini-training set that exists only inside the model’s temporary memory. When $K=0$ we speak of *zero-shot*, with $K=1$ we have *one-shot*, and any larger $K$ yields *few-shot* prompting.

```
┌────────────── Sliding Window ──────────────┐
|  D₁  |  D₂  | … |  D_K  |  Query x |  ▢    |
└─────────────────────────────────────────────┘
```

The empty square marks the place where the model must supply the answer $y$.

### Why Examples Help

Each demonstration biases the hidden representation toward functions that map inputs to outputs in the observed manner. A helpful metaphor is a musician asked to improvise: hearing a quick riff in the target style nudges her performance far more than abstract instructions alone.

## Prompt Patterns and Styles

### Zero-Shot Instructions

A crisp task description plus a clear output placeholder often suffices for routine translations or classifications. Because no examples are provided, the prompt relies on knowledge distilled during pre-training.

### One-Shot Guidance

A single example teaches the format. Picture a child shown one “2+2=4” card before solving “3+3=?”. The brain instantly grasps the pattern; the language model exhibits similar generalization.

### Few-Shot Scaffolding

Multiple demonstrations let the prompt cover edge cases and rare vocab. Empirically, performance rises roughly as $\mathcal{O}(1-\exp(-K))$ until saturation, echoing classic learning-curve theory.

## Chain-of-Thought Reasoning

Long prompts can also request that the model *explain its work*. Suppose the question involves arithmetic:

> “Sam buys two packs of balls; each pack has three balls. He already had three. How many now?”

Including the phrase *“Let’s think step by step”* encourages the network to emit intermediate statements such as

1. “Each pack contains 3 balls.”
2. “Two packs therefore add 6 balls.”
3. “Total is 3 + 6 = 9.”

Mathematically, we factor the joint probability over latent reasoning tokens $r_{1{:}m}$:

$$
p_\theta(y\mid x) = \sum_{r_{1{:}m}} p_\theta(y\mid r_{1{:}m},x)\,p_\theta(r_{1{:}m}\mid x).
$$

By asking for the chain itself we force the model to sample a high-probability trajectory through the latent space rather than marginalizing it away.

```
Question ──► [ think ]──►  r₁, r₂, … r_m  ──► Answer
                ↑                           ↓
        ASCII rail tracks mark the reasoning path
```

##  Least-to-Most Decomposition

Certain prompts instruct the model to solve a hierarchy of increasingly difficult sub-questions, reusing each answer to tackle the next. The structure resembles dynamic programming where early, cheap computations cache information for later expensive steps. If $s_i$ is the state after subproblem $i$, the policy is

$$
s_{i+1} = f_\theta(s_i,\,\text{subtask}_{i+1}),
$$

with $s_0$ derived from the original question. Evidence suggests this staged strategy reduces hallucinations because the network can condition on concrete partial results instead of juggling everything in hidden activations.

## Practical Crafting Tips

* Reserve special delimiters such as `"""` or XML tags to fence off user instructions from model completions; clear boundaries lower the risk of bleed-through.
* Keep demonstrations stylistically homogenous; abrupt style shifts confuse token-level statistics.
* Place the most relevant example closest to the query token since attention decays roughly as $1/\sqrt{d_k}$ with distance when scaled dot-product is used.
* Monitor latency: longer prompts inflate the quadratic cost $O(n^2)$ of self-attention.

## Common Pitfalls to Dodge1

Large shots can overfit the local pattern, causing rigid parroting that ignores nuanced instructions. Conversely, overly generic prompts may trigger the model’s default biases, reviving stereotypes or irrelevant trivia. Striking a balance is part art, part iterative testing.

## Wrapping Up

Prompt engineering turns raw language models into adaptable tools by manipulating **context** rather than **weights**. Whether you rely on zero-shot efficiency, few-shot clarity, chain-of-thought transparency, or least-to-most rigor, the core principle is the same: craft the textual prefix so that the conditional probability mass flows toward desired outcomes. Like composing a good question to a seasoned expert, the better the prompt, the richer—and safer—the answer you will receive.
