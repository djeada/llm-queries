## Transformer Architecture

The Transformer architecture arrived in 2017 as a fresh alternative to recurrent and convolutional sequence models. Instead of transmitting information step by step through time, it lets every token attend to every other token in a single pass. This section sets the stage by explaining why that shift mattered so much. While earlier networks struggled with long-range dependencies, the Transformer solved the bottleneck with pure attention, achieving parallelism that fit modern hardware beautifully. In the paper *Attention Is All You Need*, Vaswani and colleagues showed that translation quality could rise while training time plummeted—a rare win-win.

## Core Building Blocks

Before diving into arithmetic, it helps to sketch the four pillars that show up in almost every Transformer variant.

* Multi-head self-attention lets tokens exchange information in several subspaces at once.
* Positional encoding injects the idea of word order, which would otherwise be lost in a bag-of-tokens view.
* Position-wise feed-forward layers transform each token independently with depth-wise non-linearity.
* Layer normalization and residual connections keep gradients healthy and make stacking dozens of layers feasible.

Throughout the rest of these notes each pillar receives a close-up, complete with formulas and a short analogy to make the intuition stick.

## Scaled Dot-Product Attention

A natural first question is how the network decides “what to look at.” The answer is a small batch of matrices named query $Q$, key $K$, and value $V$. Every token produces a row in each matrix.

The raw attention scores come from

$$
\mathrm{scores} = \frac{QK^{\top}}{\sqrt{d_k}}
$$

where $d_k$ is the key dimension. Dividing by the square root prevents the dot products from exploding as dimensions grow.

Applying the softmax function row-wise yields

$$
\mathrm{weights} = softmax(\mathrm{scores})
$$

and finally the layer returns

$$
\mathrm{Attention}(Q,K,V) = \mathrm{weights}\,V.
$$

In practice the three matrices are obtained by multiplying the input $X$ with learned projection matrices $W_Q,W_K,W_V$:

$$
Q = X W_Q,\quad K = X W_K,\quad V = X W_V.
$$

An informal analogy views queries as questions and keys as book chapter headings. The softmax essentially says, “Given my question, which chapters are most relevant?” The answers in the value matrix are then blended to form a context-aware representation.

```
              ┌─────────────── Token dimension d_model ───────────────┐
Q  = X W_Q →  [ q₁  q₂  … q_n ]                (n = sequence length)
K  = X W_K →  [ k₁  k₂  … k_n ]
V  = X W_V →  [ v₁  v₂  … v_n ]
                ↑     ↑
                │     └─── self-attention lets q₂ peek at k₁ … k_n
                └───────── and vice versa for every token
```

## Multi-Head Attention

Using one attention calculation is helpful but can be myopic. Multi-head attention tackles this by splitting the model dimension into $h$ smaller chunks, running attention in each chunk independently, and concatenating the results.

Formally, for head $i$:

$$
\text{head}_i = \mathrm{Attention}\bigl(QW_Q^{(i)}, K W_K^{(i)}, V W_V^{(i)}\bigr),
$$

then

$$
\text{MHA}(Q,K,V) = \bigl[\text{head}_1 \;\|\; \dots \;\|\; \text{head}_h\bigr]W_O.
$$

The projection $W_O$ recombines information so that later layers see every head’s contribution. An everyday comparison is scanning a scene with different senses—color, depth, motion—and then synthesizing those impressions into one perception.

```
           ┌────────── head 1 ──────────┐
           │                            │
Input ──► split ──► attention ─┐        ▼
           │                  concat ─► W_O ─► output
           └────────── head h ──────────┘
```

## Positional Encoding

Because attention alone is permutation-invariant, the model needs a hint about word order. The original solution was to add a deterministic signal $P_t$ to each token embedding $E_t$:

$$
X_t = E_t + P_t.
$$

The sine–cosine pattern

$$
P_{t,2i}   = \sin\!\bigl(t / 10000^{2i/d_{\text{model}}}\bigr),\quad
P_{t,2i+1} = \cos\!\bigl(t / 10000^{2i/d_{\text{model}}}\bigr),
$$

lets the network derive relative positions through linear combinations. Some modern variants learn $P_t$ instead, yet the mathematical spirit remains: inject a smoothly varying, information-rich sequence.

## Encoder Stack

Each encoder layer follows the pattern

1. Multi-head self-attention with residual connection.
2. Position-wise feed-forward network, again wrapped in a residual path.

Layer normalization precedes (or follows, in Pre-Norm variants) each sub-layer. Stacking $N$ identical layers gives the encoder the capacity to build progressively richer representations.

```
[Input] ──► MHA ──► Add & Norm ──► FFN ──► Add & Norm ──► … (× N)
```

The encoder can be compared to a thoughtful committee: every layer listens to the entire sentence, discusses internally, and passes forward an improved consensus.

## Decoder Stack

The decoder resembles the encoder with one twist: it includes an extra attention sub-layer that looks at the encoder’s outputs. Moreover, self-attention inside the decoder is masked so that a position may not peek at future tokens, ensuring autoregressive generation.

Structure of each decoder layer:

1. Masked multi-head self-attention.
2. Encoder–decoder (cross) attention that focuses on encoder states.
3. Position-wise feed-forward network.

Residual and normalization layers wrap each step as before.

## Training Objective and Optimization

Most language implementations train the model to predict the next token, minimizing cross-entropy loss:

$$
\mathcal{L}
= -\sum_{t=1}^{n} \log p_\theta\bigl(x_t \mid x_{<\, t}\bigr).
$$

Adam or AdamW optimizers with warm-up schedules are standard. The original paper warmed up the learning rate for 4 000 steps, then decayed it proportionally to $1/\sqrt{\text{step}}$. Label smoothing of $0.1$ improved calibration and generalization.

## Why Residual Connections Matter

By adding the sub-layer’s input to its output,

$$
\text{Residual}(x) = x + \text{Sublayer}(x),
$$

the network avoids vanishing gradients, enabling depth. Empirically, removing residuals cripples convergence, much like taking away lanes from a busy highway and expecting traffic to flow smoothly.

## Variations and Extensions

* **BERT** drops the decoder and trains with masked-token prediction plus next-sentence discrimination.
* **GPT** removes the encoder and doubles down on a taller decoder, facilitating left-to-right generation.
* **T5** reinstates the full encoder–decoder but casts all tasks as text-to-text.
* **Longformer, Performer, FlashAttention** tackle quadratic memory by approximating or sparsifying attention.
* **Vision Transformers (ViT)** feed image patches instead of words, showing the architecture’s modality-agnostic nature.

Each variant tweaks attention patterns or objectives yet keeps the foundational math intact.

## Applications

Transformers now power translation, summarization, protein folding, code completion, recommendation engines, and even music generation. A neat analogy is the Swiss Army knife—the same core mechanism unfolds into blades suited to many jobs simply by changing the training data and loss.

## Strengths and Limitations

* Impressive parallelism and contextual reach grant high performance on long sequences.
* Pretraining on massive corpora yields representations transferrable to fine-tuning tasks.
* Quadratic attention cost still bites for very long texts, prompting approximate solutions.
* Large parameter counts raise energy and latency concerns, leading to research in distillation and sparsity.
