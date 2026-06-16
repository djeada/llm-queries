# Transformer Architecture

The Transformer architecture was introduced in 2017 in the paper *Attention Is All You Need*. It changed how sequence models were built.

Before Transformers, many models processed text step by step using recurrent neural networks, or RNNs. For example, to understand the last word of a sentence, an RNN had to pass information through every previous time step. This made long-range dependencies hard to learn and also made training difficult to parallelize.

Transformers solve this problem with attention.

Instead of reading tokens one at a time, a Transformer lets every token directly compare itself with every other token in the sequence. This means the model can connect related words even when they are far apart.

For example, in the sentence:

```text
The dog chased the ball because it was excited.
```

The word `"it"` probably refers to `"dog"`. Attention helps the model learn that relationship.

The main advantage is that attention can be computed in parallel, making Transformers much better suited to modern GPUs.

# 1. Core Building Blocks

Most Transformer models are built from the same few components:

1. Self-attention
2. Multi-head attention
3. Positional encoding
4. Feed-forward layers
5. Residual connections
6. Layer normalization

These pieces are repeated many times to create a deep network.

A simplified Transformer block looks like this:

```text
Input embeddings
      |
      v
Self-attention
      |
Residual connection + normalization
      |
Feed-forward network
      |
Residual connection + normalization
      |
Output to next block
```

The important idea is:

> Attention lets tokens communicate. Feed-forward layers transform the information. Residual connections and normalization make deep training stable.

# 2. Why Attention Is Needed

A sentence is not just a list of independent words. Words depend on each other.

Consider:

```text
The bank approved the loan.
```

and:

```text
The fisherman sat by the bank.
```

The word `"bank"` has different meanings in each sentence. The model needs context to understand whether it means a financial institution or the side of a river.

Attention gives each token a way to ask:

> Which other tokens in this sentence are important for understanding me?

# 3. Scaled Dot-Product Attention

The main mathematical operation in a Transformer is scaled dot-product attention.

Each token is turned into three vectors:

* a query vector,
* a key vector,
* a value vector.

These are usually written as:

$$
Q, K, V
$$

The attention formula is:

$$
\text{Attention}(Q, K, V) = \text{softmax}
\left(
\frac{QK^\top}{\sqrt{d_k}}
\right)V
$$

where:

* (Q) is the query matrix,
* (K) is the key matrix,
* (V) is the value matrix,
* (d_k) is the key dimension,
* (QK^\top) computes similarity scores,
* (\sqrt{d_k}) prevents the scores from becoming too large,
* softmax turns scores into probabilities.

An analogy:

* A query is like a question.
* A key is like a label on a piece of information.
* A value is the actual information.

The query asks, "Which keys match me? " Then the model blends the corresponding values.

# 4. Example by Hand: Attention Scores

Suppose we have two tokens:

```text
Token 1: "cat"
Token 2: "sat"
```

Assume their query and key vectors are:

$$
Q = \begin{bmatrix}
1 & 0 \
0 & 1
\end{bmatrix}
$$

$$
K = \begin{bmatrix}
1 & 1 \
1 & 0
\end{bmatrix}
$$

We compute:

$$
QK^\top
$$

First compute (K^\top):

$$
K^\top = \begin{bmatrix}
1 & 1 \
1 & 0
\end{bmatrix}
$$

In this example, (K) happens to equal (K^\top).

Now multiply:

$$
QK^\top = \begin{bmatrix}
1 & 0 \
0 & 1
\end{bmatrix}
\begin{bmatrix}
1 & 1 \
1 & 0
\end{bmatrix}
$$

This gives:

$$
QK^\top = \begin{bmatrix}
1 & 1 \
1 & 0
\end{bmatrix}
$$

So the raw attention scores are:

$$
\begin{bmatrix}
1 & 1 \
1 & 0
\end{bmatrix}
$$

Each row tells us how much one token attends to each token.

# 5. Scaling the Scores

The scaled attention formula divides by:

$$
\sqrt{d_k}
$$

Here, the key dimension is:

$$
d_k = 2
$$

So:

$$
\sqrt{d_k} = \sqrt{2} \approx 1. 414
$$

Now divide each score by 1. 414:

$$
\frac{1}{1. 414} \approx 0. 707
$$

$$
\frac{0}{1. 414} = 0
$$

So the scaled scores are:

$$
\begin{bmatrix}
0. 707 & 0. 707 \
0. 707 & 0
\end{bmatrix}
$$

Scaling matters because large dot products can make softmax too sharp. If softmax becomes too sharp too early, training becomes less stable.

# 6. Example by Hand: Softmax

Now apply softmax to each row.

For the first row:

$$
[0. 707, 0. 707]
$$

Since both scores are equal, both tokens get equal attention:

$$
[0. 5, 0. 5]
$$

For the second row:

$$
[0. 707, 0]
$$

Compute exponentials:

$$
e^{0. 707} \approx 2. 028
$$

$$
e^0 = 1
$$

Sum:

$$
2. 028 + 1 = 3. 028
$$

Normalize:

$$
\frac{2. 028}{3. 028} \approx 0. 670
$$

$$
\frac{1}{3. 028} \approx 0. 330
$$

So the attention weights are approximately:

$$
\begin{bmatrix}
0. 5 & 0. 5 \
0. 670 & 0. 330
\end{bmatrix}
$$

This means:

* Token 1 attends equally to token 1 and token 2.
* Token 2 attends more to token 1 than to token 2.

# 7. Example by Hand: Weighted Sum of Values

Now suppose the value matrix is:

$$
V = \begin{bmatrix}
10 & 0 \
0 & 10
\end{bmatrix}
$$

The attention output is:

$$
\text{weights} \times V
$$

Using:

$$
\text{weights} = \begin{bmatrix}
0. 5 & 0. 5 \
0. 670 & 0. 330
\end{bmatrix}
$$

we compute:

$$
\begin{bmatrix}
0. 5 & 0. 5 \
0. 670 & 0. 330
\end{bmatrix}
\begin{bmatrix}
10 & 0 \
0 & 10
\end{bmatrix}
$$

First row:

$$
[0. 5 \cdot 10 + 0. 5 \cdot 0, \quad 0. 5 \cdot 0 + 0. 5 \cdot 10]
$$

$$
= [5, 5]
$$

Second row:

$$
[0. 670 \cdot 10 + 0. 330 \cdot 0, \quad 0. 670 \cdot 0 + 0. 330 \cdot 10]
$$

$$
= [6. 70, 3. 30]
$$

So the final attention output is approximately:

$$
\begin{bmatrix}
5 & 5 \
6. 70 & 3. 30
\end{bmatrix}
$$

Each token now contains a mixture of information from other tokens.

# 8. Python Example: Scaled Dot-Product Attention

```python
import numpy as np

def softmax(x):
    # subtract max for numerical stability
    x = x - np.max(x, axis=-1, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

Q = np.array([
    [1, 0],
    [0, 1]
], dtype=float)

K = np.array([
    [1, 1],
    [1, 0]
], dtype=float)

V = np.array([
    [10, 0],
    [0, 10]
], dtype=float)

d_k = K.shape[1]

scores = Q @ K.T
scaled_scores = scores / np.sqrt(d_k)
weights = softmax(scaled_scores)
output = weights @ V

print("Raw scores:")
print(scores)

print("\nScaled scores:")
print(scaled_scores)

print("\nAttention weights:")
print(weights)

print("\nAttention output:")
print(output)
```

Expected output will be close to:

```text
Raw scores:
[[1. 1.]
 [1. 0.]]

Scaled scores:
[[0.707 0.707]
 [0.707 0.   ]]

Attention weights:
[[0.5   0.5  ]
 [0.67  0.33 ]]

Attention output:
[[5.0  5.0 ]
 [6.7  3.3 ]]
```

# 9. Where Do Q, K, and V Come From?

The model does not receive (Q), (K), and (V) directly.

It starts with token embeddings.

Suppose the input matrix is:

$$
X
$$

Each row is a token embedding.

The model learns three projection matrices:

$$
W_Q, W_K, W_V
$$

Then it computes:

$$
Q = XW_Q
$$

$$
K = XW_K
$$

$$
V = XW_V
$$

These learned matrices decide what information should become a query, key, or value.

So the model learns how tokens should ask questions, match against other tokens, and pass information forward.

# 10. Multi-Head Attention

A single attention operation can learn one type of relationship. But language contains many relationships at once.

For example, in one sentence, the model may need to track:

* subject and verb agreement,
* pronoun references,
* word meaning,
* phrase boundaries,
* syntax,
* sentiment,
* named entities.

Multi-head attention lets the model learn several attention patterns in parallel.

Instead of doing attention once, the Transformer does it multiple times using different learned projections.

For head (i):

$$
\text{head}_i = \text{Attention}
\left(
QW_Q^{(i)},
KW_K^{(i)},
VW_V^{(i)}
\right)
$$

Then all heads are concatenated:

$$
[\text{head}_1 | \text{head}_2 | \cdots | \text{head}_h]
$$

Finally, a learned output matrix (W_O) mixes them:

$$
\text{MHA}(Q, K, V) = [\text{head}_1 | \cdots | \text{head}_h]W_O
$$

## Example by Hand: Head Dimensions

Suppose:

$$
d_{\text{model}} = 512
$$

and the model uses:

$$
h = 8
$$

attention heads.

Each head usually gets dimension:

$$
d_{\text{head}} = \frac{d_{\text{model}}}{h}
$$

So:

$$
d_{\text{head}} = # \frac{512}{8}

64
$$

Each attention head works in a 64-dimensional space.

After all 8 heads finish, their outputs are concatenated:

$$
8 \times 64 = 512
$$

So the model returns to the original model dimension.

## Python Example: Multi-Head Dimension Calculation

```python
d_model = 512
num_heads = 8

d_head = d_model // num_heads

print("Model dimension:", d_model)
print("Number of heads:", num_heads)
print("Dimension per head:", d_head)
print("Concatenated size:", num_heads * d_head)
```

Output:

```text
Model dimension: 512
Number of heads: 8
Dimension per head: 64
Concatenated size: 512
```

# 11. Positional Encoding

Attention compares tokens with other tokens, but by itself it does not know the order of the tokens.

For example, these two sentences contain the same words:

```text
The dog chased the cat.
```

```text
The cat chased the dog.
```

The meaning is different because the order is different.

Transformers need a way to represent position.

The original Transformer used sine and cosine positional encodings:

$$
P_{t, 2i} = \sin
\left(
\frac{t}{10000^{2i/d_{\text{model}}}}
\right)
$$

$$
P_{t, 2i+1} = \cos
\left(
\frac{t}{10000^{2i/d_{\text{model}}}}
\right)
$$

where:

* (t) is the position,
* (i) is the dimension index,
* (d_{\text{model}}) is the embedding size.

The positional encoding is added to the token embedding:

$$
X_t = E_t + P_t
$$

where:

* (E_t) is the token embedding,
* (P_t) is the positional encoding.

## Example by Hand: Positional Encoding

Suppose:

$$
d_{\text{model}} = 4
$$

and we want the positional encoding for position:

$$
t = 1
$$

The dimensions are 0, 1, 2, and 3.

For dimension 0:

$$
P_{1, 0} = \sin
\left(
\frac{1}{10000^{0/4}}
\right)
$$

$$
10000^{0/4} = 1
$$

$$
P_{1, 0} = \sin(1) \approx 0. 841
$$

For dimension 1:

$$
P_{1, 1} = \cos
\left(
\frac{1}{10000^{0/4}}
\right)
$$

$$
P_{1, 1} = \cos(1) \approx 0. 540
$$

For dimension 2, (i = 1):

$$
P_{1, 2} = \sin
\left(
\frac{1}{10000^{2/4}}
\right)
$$

$$
10000^{2/4} = 10000^{0. 5} = 100
$$

$$
P_{1, 2} = \sin(0. 01)
\approx 0. 010
$$

For dimension 3:

$$
P_{1, 3} = \cos(0. 01)
\approx 1. 000
$$

So:

$$
P_1
\approx
[0. 841, \ 0. 540, \ 0. 010, \ 1. 000]
$$

## Python Example: Positional Encoding

```python
import numpy as np

def positional_encoding(position, d_model):
    encoding = np.zeros(d_model)

    for i in range(0, d_model, 2):
        denominator = 10000 ** (i / d_model)
        encoding[i] = np.sin(position / denominator)

        if i + 1 < d_model:
            encoding[i + 1] = np.cos(position / denominator)

    return encoding

print(positional_encoding(position=1, d_model=4))
```

Expected output:

```text
[0.841 0.540 0.010 1.000]
```

# 12. Feed-Forward Networks

After attention, each token passes through a feed-forward neural network.

The attention layer mixes information between tokens.

The feed-forward network transforms each token independently.

A common formula is:

$$
\text{FFN}(x) = W_2 \sigma(W_1x + b_1) + b_2
$$

where:

* (W_1) and (W_2) are learned weight matrices,
* (b_1) and (b_2) are bias vectors,
* (\sigma) is a nonlinear activation function such as ReLU or GELU.

## Example by Hand: Tiny Feed-Forward Network

Suppose:

$$
x = \begin{bmatrix}
2 \
1
\end{bmatrix}
$$

Let:

$$
W_1 = \begin{bmatrix}
1 & 0 \
0 & 1 \
1 & 1
\end{bmatrix}
$$

and:

$$
b_1 = \begin{bmatrix}
0 \
0 \
0
\end{bmatrix}
$$

Compute:

$$
W_1x + b_1 = \begin{bmatrix}
1 & 0 \
0 & 1 \
1 & 1
\end{bmatrix}
\begin{bmatrix}
2 \
1
\end{bmatrix} = \begin{bmatrix}
2 \
1 \
3
\end{bmatrix}
$$

Using ReLU:

$$
\text{ReLU}(z) = \max(0, z)
$$

Since all values are positive:

$$
\text{ReLU}
\left(
\begin{bmatrix}
2 \
1 \
3
\end{bmatrix}
\right) = \begin{bmatrix}
2 \
1 \
3
\end{bmatrix}
$$

Now let:

$$
W_2 = \begin{bmatrix}
1 & 0 & 1 \
0 & 1 & 1
\end{bmatrix}
$$

Then:

$$
W_2
\begin{bmatrix}
2 \
1 \
3
\end{bmatrix} = \begin{bmatrix}
1 \cdot 2 + 0 \cdot 1 + 1 \cdot 3 \
0 \cdot 2 + 1 \cdot 1 + 1 \cdot 3
\end{bmatrix}
$$

# [

\begin{bmatrix}
5 \
4
\end{bmatrix}
]

So the feed-forward network maps:

$$
[2, 1]
\to
[5, 4]
$$

## Python Example: Tiny Feed-Forward Network

```python
import numpy as np

def relu(x):
    return np.maximum(0, x)

x = np.array([[2], [1]])

W1 = np.array([
    [1, 0],
    [0, 1],
    [1, 1]
])

b1 = np.array([[0], [0], [0]])

W2 = np.array([
    [1, 0, 1],
    [0, 1, 1]
])

b2 = np.array([[0], [0]])

hidden = relu(W1 @ x + b1)
output = W2 @ hidden + b2

print("Hidden:")
print(hidden)

print("\nOutput:")
print(output)
```

# 13. Residual Connections

Deep neural networks can be hard to train because information and gradients may weaken as they pass through many layers.

Transformers use residual connections.

Instead of only computing:

$$
\text{Sublayer}(x)
$$

the model computes:

$$
x + \text{Sublayer}(x)
$$

This gives the model a shortcut.

If a sublayer is not useful, the model can still pass the original input forward.

## Example by Hand: Residual Connection

Suppose:

$$
x = [2, 3]
$$

and a sublayer outputs:

$$
\text{Sublayer}(x) = [0. 5, -1]
$$

Then the residual output is:

$$
x + \text{Sublayer}(x) = [2, 3] + [0. 5, -1]
$$

# [

[2. 5, 2]
]

So the model keeps most of the original information while adding a learned adjustment.

# 14. Layer Normalization

Layer normalization helps keep activations stable.

For a vector (x), layer normalization computes:

$$
\text{LayerNorm}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}}
$$

where:

* (\mu) is the mean of the vector,
* (\sigma^2) is the variance,
* (\epsilon) is a small number to avoid division by zero.

Usually the model also learns a scale and shift after normalization, but the core idea is to standardize the values.

## Example by Hand: Layer Normalization

Suppose:

$$
x = [2, 4, 6]
$$

The mean is:

$$
\mu = \frac{2 + 4 + 6}{3} = 4
$$

Subtract the mean:

$$
x - \mu = [-2, 0, 2]
$$

The variance is:

$$
\sigma^2 = \frac{(-2)^2 + 0^2 + 2^2}{3}
$$

# [

# \frac{4 + 0 + 4}{3}

\frac{8}{3}
\approx 2. 667
]

The standard deviation is:

$$
\sqrt{2. 667} \approx 1. 633
$$

Normalize:

$$
\frac{[-2, 0, 2]}{1. 633}
\approx
[-1. 225, 0, 1. 225]
$$

So:

$$
\text{LayerNorm}([2, 4, 6])
\approx
[-1. 225, 0, 1. 225]
$$

## Python Example: Layer Normalization

```python
import numpy as np

x = np.array([2, 4, 6], dtype=float)

mean = np.mean(x)
variance = np.mean((x - mean) ** 2)
normalized = (x - mean) / np.sqrt(variance + 1e-5)

print("Mean:", mean)
print("Variance:", variance)
print("Normalized:", normalized)
```

# 15. Encoder Stack

The original Transformer has an encoder and a decoder.

The encoder reads the input sequence and builds contextual representations.

For example, in machine translation, the encoder reads the source sentence:

```text
I love apples.
```

It creates a rich internal representation of that sentence.

Each encoder layer contains:

1. Multi-head self-attention
2. Add and normalization
3. Feed-forward network
4. Add and normalization

A simplified encoder layer:

```text
Input
  |
  v
Multi-head self-attention
  |
Add + LayerNorm
  |
Feed-forward network
  |
Add + LayerNorm
  |
Output
```

Stacking several encoder layers lets the model build more abstract representations.

Early layers may learn local word relationships, while later layers may learn broader sentence-level meaning.

# 16. Decoder Stack

The decoder generates the output sequence.

In translation, the decoder might generate:

```text
J'aime les pommes.
```

one token at a time.

Each decoder layer contains:

1. Masked self-attention
2. Encoder-decoder attention, also called cross-attention
3. Feed-forward network

A simplified decoder layer:

```text
Output tokens so far
      |
      v
Masked self-attention
      |
Add + LayerNorm
      |
Cross-attention over encoder output
      |
Add + LayerNorm
      |
Feed-forward network
      |
Add + LayerNorm
      |
Next token prediction
```

The key difference is that decoder self-attention is masked.

# 17. Causal Masking

In a decoder, the model must not look at future tokens.

Suppose the target sequence is:

```text
I like cats
```

When predicting `"like"`, the model may look at:

```text
I
```

but it must not look at:

```text
cats
```

Otherwise, it would cheat during training.

A causal mask allows each position to attend only to itself and previous positions.

For 4 tokens, the allowed attention pattern is:

$$
\begin{bmatrix}
1 & 0 & 0 & 0 \
1 & 1 & 0 & 0 \
1 & 1 & 1 & 0 \
1 & 1 & 1 & 1
\end{bmatrix}
$$

This means:

* Token 1 sees token 1.
* Token 2 sees tokens 1 and 2.
* Token 3 sees tokens 1, 2, and 3.
* Token 4 sees tokens 1, 2, 3, and 4.

## Python Example: Causal Mask

```python
import numpy as np

n = 4

mask = np.tril(np.ones((n, n)))

print(mask)
```

Output:

```text
[[1. 0. 0. 0.]
 [1. 1. 0. 0.]
 [1. 1. 1. 0.]
 [1. 1. 1. 1.]]
```

In real implementations, disallowed positions are often given a very large negative score before softmax.

# 18. Cross-Attention

Cross-attention is used in encoder-decoder Transformers.

In self-attention, queries, keys, and values all come from the same sequence.

In cross-attention:

* queries come from the decoder,
* keys and values come from the encoder.

So the decoder asks:

> Which parts of the input sentence are useful for generating the next output token?

For translation, when generating the French word `"pommes"`, the decoder may attend strongly to the English word `"apples"`.

# 19. Training Objective

Many Transformer language models are trained to predict the next token.

Given tokens:

$$
x_1, x_2, \dots, x_n
$$

the model estimates:

$$
p_\theta(x_t \mid x_{<t})
$$

The cross-entropy loss is:

$$
\mathcal{L} = -\sum_{t=1}^{n}
\log p_\theta(x_t \mid x_{<t})
$$

Sometimes the average loss is used:

$$
\mathcal{L} = -\frac{1}{n}
\sum_{t=1}^{n}
\log p_\theta(x_t \mid x_{<t})
$$

The model gets a low loss when it assigns high probability to the correct next token.

## Example by Hand: Cross-Entropy Loss

Suppose the correct next tokens receive these probabilities:

$$
[0. 8, 0. 5, 0. 25]
$$

The average cross-entropy loss is:

$$
\mathcal{L} = -\frac{1}{3}
[
\log(0. 8) + \log(0. 5) + \log(0. 25)
$$

]

Approximate logs:

$$
\log(0. 8) \approx -0. 223
$$

$$
\log(0. 5) \approx -0. 693
$$

$$
\log(0. 25) \approx -1. 386
$$

So:

$$
\mathcal{L} = -\frac{1}{3}
[
-0. 223 - 0. 693 - 1. 386
$$

]

# [

-\frac{1}{3}
[-2. 302]
]

# [

0. 767
]

So the average loss is approximately:

$$
0. 767
$$

## Python Example: Cross-Entropy Loss

```python
import math

correct_token_probs = [0.8, 0.5, 0.25]

loss = -sum(math.log(p) for p in correct_token_probs) / len(correct_token_probs)

print("Average cross-entropy loss:", loss)
```

# 20. Learning Rate Warmup

The original Transformer used a learning rate schedule with warmup.

During warmup, the learning rate increases gradually. After warmup, it decays.

A simplified version of the schedule is:

$$
\text{lr} = d_{\text{model}}^{-0. 5}
\cdot
\min
\left(
\text{step}^{-0. 5},
\text{step} \cdot \text{warmup}^{-1. 5}
\right)
$$

The reason for warmup is that early training can be unstable. A small learning rate at the beginning helps the model avoid large destructive updates.

## Python Example: Learning Rate Schedule

```python
def transformer_lr(step, d_model=512, warmup=4000):
    return (d_model ** -0.5) * min(step ** -0.5, step * (warmup ** -1.5))

for step in [1, 100, 1000, 4000, 8000, 16000]:
    print(step, transformer_lr(step))
```

This shows the learning rate rising at first, then slowly decreasing.

# 21. Computational Cost of Attention

Self-attention compares every token with every other token.

If the sequence length is (n), the attention score matrix has size:

$$
n \times n
$$

So the memory and compute cost grows approximately like:

$$
O(n^2)
$$

This is called quadratic complexity.

## Example by Hand: Attention Matrix Size

If:

$$
n = 100
$$

then the attention matrix has:

$$
100 \times 100 = 10{,}000
$$

entries.

If:

$$
n = 1000
$$

then it has:

$$
1000 \times 1000 = 1{,}000{,}000
$$

entries.

Increasing sequence length by 10x increases the attention matrix size by 100x.

That is why very long contexts are expensive.

## Python Example: Attention Cost Growth

```python
lengths = [100, 500, 1000, 2000, 4000]

for n in lengths:
    entries = n * n
    print(f"Sequence length: {n:>4}, attention entries: {entries:,}")
```

Output:

```text
Sequence length:  100, attention entries: 10,000
Sequence length:  500, attention entries: 250,000
Sequence length: 1000, attention entries: 1,000,000
Sequence length: 2000, attention entries: 4,000,000
Sequence length: 4000, attention entries: 16,000,000
```

# 22. Encoder-Only, Decoder-Only, and Encoder-Decoder Models

Different Transformer models use different parts of the architecture.

## Encoder-Only Models

Encoder-only models are good for understanding text.

Examples:

* BERT
* RoBERTa

They are often used for:

* classification,
* search,
* sentence similarity,
* named entity recognition.

They usually see the whole input at once.

## Decoder-Only Models

Decoder-only models are good for generating text.

Examples:

* GPT-style models
* many modern chat models

They use causal masking so they generate from left to right.

They are often used for:

* chatbots,
* story generation,
* code completion,
* question answering,
* summarization.

## Encoder-Decoder Models

Encoder-decoder models are useful when one sequence is transformed into another.

Examples:

* original Transformer for translation,
* T5,
* BART.

They are often used for:

* translation,
* summarization,
* text-to-text tasks.

# 23. Transformer Variants

Many later models modify the original Transformer.

## BERT

BERT uses an encoder-only Transformer.

It is trained by hiding some tokens and asking the model to predict them.

Example:

```text
The cat sat on the [MASK].
```

The model might predict:

```text
mat
```

BERT is strong for text understanding tasks.

## GPT

GPT-style models use decoder-only Transformers.

They predict the next token from left to right.

Example:

```text
The cat sat on the
```

The model predicts:

```text
mat
```

This makes GPT-style models strong for text generation.

## T5

T5 uses an encoder-decoder Transformer.

It treats every task as a text-to-text problem.

For example:

```text
translate English to French: I like apples
```

The output is:

```text
J'aime les pommes
```

## Long-Context Transformers

Standard attention is expensive for long sequences.

Models and methods such as Longformer, Performer, and other efficient-attention approaches try to reduce this cost through sparse, approximate, or kernel-based attention patterns.

FlashAttention is different: it computes exact attention but uses memory-efficient GPU operations to make attention faster and less memory-hungry.

## Vision Transformers

Vision Transformers, or ViTs, apply the Transformer idea to images.

Instead of tokens being words, tokens are image patches.

For example, an image can be split into small square patches, and each patch is treated like a token.

This shows that Transformers are not limited to language.

# 24. Applications of Transformers

Transformers are used in many areas, including:

* machine translation,
* text summarization,
* question answering,
* chatbots,
* code generation,
* search ranking,
* recommendation systems,
* speech recognition,
* image classification,
* protein structure prediction,
* music generation.

The same basic mechanism can work across many data types because attention is a general way to relate parts of an input.

# 25. Strengths of Transformers

Transformers are powerful because they:

* handle long-range dependencies better than many older models,
* train efficiently in parallel,
* work well with large datasets,
* scale to very large models,
* transfer well from pretraining to downstream tasks,
* can be adapted to text, images, audio, code, and other modalities.

Their main strength is that every token can directly communicate with every other token.

# 26. Limitations of Transformers

Transformers also have limitations.

## Quadratic Cost

Self-attention requires comparing every token with every other token.

This becomes expensive for very long sequences.

## Large Compute Requirements

Training large Transformers requires powerful hardware, lots of memory, and significant energy.

## Data Dependence

Transformers learn from data. If the data is biased, incomplete, or low quality, the model may learn those problems.

## Limited Interpretability

Although attention weights can sometimes give clues, they do not fully explain why a model makes a decision.

## Context Window Limits

A Transformer can only directly use information inside its context window.

If relevant information is outside the context, the model may not know it.
