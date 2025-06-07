# What are LLMs?

Large-language models (LLMs) are really big statistical parrots—yet calling them that undersells the sophistication hiding inside their billions of parameters. At heart an LLM tries to guess the next token in a sequence, but by scaling the network’s width, depth, and training corpus it winds up learning grammar, facts, reasoning shortcuts, and even snippets of world knowledge. Think of the model’s weights as a compressed‐into-silicon reflection of most text the internet has ever seen.

##  A Probabilistic View of Text

Before we explore engineering details, it helps to ground the idea mathematically. For a sequence of tokens \(x_1, x_2, \dots, x_T\), a language model assigns the joint probability

$$
p_\theta(x_{1:T}) =
\prod_{t=1}^{T} p_\theta\!\bigl(x_t \mid x_{<\,t}\bigr)
$$

Training maximizes the log-likelihood, which is equivalent to minimizing the cross-entropy loss:

$$
\mathcal{L} =
-\frac{1}{T}\sum_{t=1}^{T} \log p_\theta\!\bigl(x_t \mid x_{<\,t}\bigr)
$$

Because the objective uses only the raw text itself, we call the procedure **self-supervised**: no human needs to label “cat” as the right answer; the context does that automatically.

## From “Large” to “Larger”

Parameter count matters because it governs how many patterns the model can memorize and recombine. If $N$ is the number of parameters and $D$ the number of training tokens, empirical **scaling laws** suggest a power-law falloff of loss:

$$
\mathcal{L}(N,D) \approx a\,N^{-\alpha} + b\,D^{-\beta} + \varepsilon,
\quad
\alpha,\beta \approx 0.07\text{–}0.10.
$$

The tiny exponents mean performance improves steadily—but not explosively—as we climb from millions to billions of weights. GPT-3’s 175 B parameters, for example, lie near the knee where adding one more GPU still cuts perplexity noticeably.

##  Anatomy of a Modern LLM

Every mainstream LLM today is a stack of Transformer decoder blocks. Each block contains

* a multi-head **self-attention** layer so tokens can consult one another in parallel
* a position-wise **feed-forward** network that refines each token independently
* **layer normalization** and **residual** paths to keep gradients healthy

```
Input ─► Attn ─► + ─► Norm ─► FFN ─► + ─► Norm ─► next block
          ▲                 ▲
          └──── residual ───┘
```

The sketch shows one block; real models repeat the pattern 12 to 96 times, widening internal vectors to 768, 1 536, 12 288, or more dimensions.

## Training Data: Breadth Beats Labels

Instead of curating one tidy dataset, engineers scoop up whole slices of the web: Common Crawl, Wikipedia, digitized books, news, code repositories, and scientific papers. Filtering removes HTML boilerplate, near duplicates, and obvious toxicity, but the principle stays simple—feed the model *everything* so it can learn *anything*. The result is a single model that can translate, rhyme, explain, and even write pseudo-code without switching checkpoints.

## Decoding: Turning Probabilities into Sentences

After training, generation becomes a game of sampling. Given the probability vector $p_\theta(\cdot)$ over the vocabulary at step $t$,

* **Greedy decoding** picks the arg-max token and is fast but repetitive.
* **Top-$k$ or top-$p$ sampling** draws from the highest-ranked subset, adding diversity.
* **Temperature scaling** rescales logits $z$ as $z/T$; lowering $T$ sharpens the distribution, raising it produces wilder prose.

A useful analogy is rolling weighted dice whose faces change after each word.

## Prompting: Steering Without Retraining

Because the model’s parameters stay frozen at inference time, the only control knob a user has is the prompt. Adding one adjective—say “little” before the blank in \_“They sent me a \_\_*”*—can swing probability mass from “lion” toward “cat.” This sensitivity is not a bug; it is an in-context learning feature that lets us program the model with plain English.

## Adapting LLMs to New Domains

Sometimes a prompt is not enough. Practitioners then choose among several adaptation strategies.

* Full **fine-tuning** rewrites every weight on labeled domain data, giving maximum flexibility at high compute cost.
* **Parameter-efficient fine-tuning** (LoRA, adapters) inserts tiny bottleneck layers and alters only those, achieving similar gains with $<\!1\%$ extra parameters.
* **Soft prompting** learns a handful of virtual tokens prepended to the input; the base model remains untouched.

Single-level summary table:

| Method          | Updated Parameters | Typical Data | Memory Footprint |
| --------------- | ------------------ | ------------ | ---------------- |
| Fine-tune       | All                | Labeled      | High             |
| LoRA / Adapters | < 1 %              | Labeled      | Low              |
| Soft Prompt     | Few embeddings     | Task prompts | Minimal          |

## Strengths, Weaknesses, and Open Questions

* An LLM stores vast factual and stylistic knowledge, enabling one model to multitask.
* Attention lets every token see the whole context simultaneously, so long-range dependencies come naturally.
* Quadratic cost in sequence length limits inputs to a few thousand tokens; research in sparse or linear attention aims to break that barrier.
* Models inherit biases from training data; careful evaluation and post-processing are mandatory.
* Interpretability lags behind capability—figuring out *why* the network answers as it does remains an active frontier.

## Wrapping Up

Large-language models marry an elegant probabilistic objective with colossal datasets and the hardware-friendly Transformer backbone. The recipe looks absurdly simple—predict the next token often enough and the network learns to summarize novels—but the emergent behaviours are anything but trivial. As parameter counts and context windows keep expanding, understanding, steering, and aligning these models becomes as important as the raw engineering that created them.
