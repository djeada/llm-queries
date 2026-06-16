# What Are Large Language Models?

Large language models, or LLMs, are machine learning systems trained to predict text. More precisely, they predict the next token given the tokens that came before it.

A token can be a word, part of a word, punctuation mark, or symbol. For example, the sentence

```text
The cat sat.
```

might be split into tokens like:

```text
["The", " cat", " sat", "."]
```

At first, "predict the next token" sounds simple. However, when this task is repeated over massive amounts of text, the model gradually learns patterns of grammar, facts, style, reasoning, code structure, and common forms of explanation.

An LLM does not store knowledge like a database. Instead, it stores patterns in its parameters, which are the numerical weights learned during training.

# 1. A Probabilistic View of Text

An LLM assigns probabilities to possible next tokens.

Suppose we have a sequence of tokens:

$$
x_1, x_2, \dots, x_T
$$

The model estimates the probability of the full sequence by multiplying many conditional probabilities:

$$
p_\theta(x_{1:T}) = \prod_{t=1}^{T} p_\theta(x_t \mid x_{1:t-1})
$$

This means:

$$
p(x_1, x_2, x_3) = p(x_1)
p(x_2 \mid x_1)
p(x_3 \mid x_1, x_2)
$$

The model reads the previous tokens and predicts the next one.

## Example by Hand: Probability of a Short Sentence

Suppose our sentence is:

```text
I like cats
```

Assume the model gives these probabilities:

$$
p(\text{I}) = 0. 2
$$

$$
p(\text{like} \mid \text{I}) = 0. 5
$$

$$
p(\text{cats} \mid \text{I like}) = 0. 1
$$

Then the probability of the full sequence is:

$$
p(\text{I like cats}) = 0. 2 \times 0. 5 \times 0. 1
$$

$$
= 0. 01
$$

So the model assigns a probability of:

$$
1%
$$

to the sentence `"I like cats"`.

## Training Objective: Cross-Entropy Loss

During training, the model is rewarded for assigning high probability to the correct next token.

The loss is usually written as:

$$
\mathcal{L} = -\frac{1}{T}
\sum_{t=1}^{T}
\log p_\theta(x_t \mid x_{1:t-1})
$$

This is called cross-entropy loss.

The negative sign is there because probabilities are between 0 and 1, and logs of numbers between 0 and 1 are negative.

For example:

$$
\log(0. 5) \approx -0. 693
$$

$$
\log(0. 1) \approx -2. 303
$$

A higher probability gives a smaller loss.

## Example by Hand: Cross-Entropy Loss

Using the same example:

$$
p(\text{I}) = 0. 2
$$

$$
p(\text{like} \mid \text{I}) = 0. 5
$$

$$
p(\text{cats} \mid \text{I like}) = 0. 1
$$

The loss is:

$$
\mathcal{L} = -\frac{1}{3}
[
\log(0. 2) + \log(0. 5) + \log(0. 1)
]
$$

Using approximate values:

$$
\log(0. 2) \approx -1. 609
$$

$$
\log(0. 5) \approx -0. 693
$$

$$
\log(0. 1) \approx -2. 303
$$

$$
\begin{aligned}
\mathcal{L} = -\frac{1}{3}
\left[
-1.609 - 0.693 - 2.303
\right] = -\frac{1}{3}(-4.605) = 1.535
\end{aligned}
$$

So the average loss is approximately:

$$
\mathcal{L} \approx 1. 535
$$

## Perplexity

A related measure is perplexity:

$$
\text{Perplexity} = e^{\mathcal{L}}
$$

Using the previous loss:

$$
\text{Perplexity} = e^{1. 535}
\approx 4. 64
$$

Roughly speaking, this means the model is acting as if it is choosing among about 4. 64 equally likely tokens at each step.

Lower perplexity usually means better prediction.

## Python Example: Cross-Entropy and Perplexity

```python
import math

probs = [0.2, 0.5, 0.1]

loss = -sum(math.log(p) for p in probs) / len(probs)
perplexity = math.exp(loss)

print("Cross-entropy loss:", loss)
print("Perplexity:", perplexity)
```

Expected output:

```text
Cross-entropy loss: 1.535
Perplexity: 4.642
```

# 2. Why the Training Is Self-Supervised

LLMs are trained with self-supervised learning.

This means the training data does not need human-written labels.

For example, from the sentence:

```text
The dog chased the ball.
```

The model can create its own training examples:

```text
Input: The
Target: dog

Input: The dog
Target: chased

Input: The dog chased
Target: the

Input: The dog chased the
Target: ball
```

The text itself provides the labels.

This is one reason LLMs can be trained on very large datasets.

# 3. From "Large" to "Larger"

The word large refers mainly to three things:

1. The number of model parameters.
2. The amount of training data.
3. The amount of computation used during training.

A parameter is a number learned by the model. These numbers control how information flows through the network.

Larger models can often learn more patterns, but size alone is not enough. The model also needs enough high-quality training data and enough compute.

## Scaling Laws

Empirical scaling laws suggest that language model loss often decreases in a predictable way as model size and dataset size increase.

A simplified form is:

$$
\mathcal{L}(N, D)
\approx
aN^{-\alpha}
+
bD^{-\beta}
+
\varepsilon
$$

where:

* (N) is the number of parameters,
* (D) is the number of training tokens,
* (a), (b), (\alpha), and (\beta) are constants,
* (\varepsilon) represents irreducible error or noise.

The exponents (\alpha) and (\beta) are usually small. This means that increasing scale helps, but improvements are gradual.

## Example by Hand: What a Small Exponent Means

Suppose loss decreases according to:

$$
N^{-0. 1}
$$

Now imagine increasing the number of parameters by a factor of 10.

The improvement factor is:

$$
10^{-0. 1}
$$

Using:

$$
10^{-0. 1} \approx 0. 794
$$

So the loss term becomes about:

$$
79. 4%
$$

of what it was before.

That is an improvement of about:

$$
20. 6%
$$

So even a 10x increase in model size does not make the loss 10x smaller. It gives a steady but limited improvement.

## Python Example: Scaling Law Toy Model

```python
def scaling_loss(N, D, a=1.0, b=1.0, alpha=0.1, beta=0.1, eps=0.1):
    return a * N**(-alpha) + b * D**(-beta) + eps

sizes = [1_000_000, 10_000_000, 100_000_000, 1_000_000_000]
tokens = 10_000_000_000

for N in sizes:
    loss = scaling_loss(N, tokens)
    print(f"Parameters: {N:,}, Loss: {loss:.4f}")
```

This program is not training a real model. It only shows the idea that loss tends to decrease gradually as scale increases.

# 4. Anatomy of a Modern LLM

Most modern LLMs are based on the Transformer architecture.

A Transformer language model is usually made from many repeated blocks. Each block contains:

1. Self-attention
2. Feed-forward neural networks
3. Residual connections
4. Layer normalization

A simplified block looks like this:

```text
Input
  |
  v
Self-Attention
  |
  +---- Residual Connection
  |
Layer Normalization
  |
Feed-Forward Network
  |
  +---- Residual Connection
  |
Layer Normalization
  |
  v
Next Block
```

Real LLMs repeat this block many times.

# 5. Self-Attention

Self-attention lets each token look at other tokens in the context.

For example, consider the sentence:

```text
The animal did not cross the street because it was tired.
```

The word `"it"` probably refers to `"animal"`.

Self-attention helps the model connect related words, even if they are far apart.

## The Basic Attention Formula

For each token, the model creates three vectors:

* Query: (q)
* Key: (k)
* Value: (v)

The attention score between a query and a key is often computed using a dot product:

$$
\text{score}(q, k) = q \cdot k
$$

Then the scores are passed through a softmax function to get attention weights:

$$
\text{softmax}(s_i) = \frac{e^{s_i}}{\sum_j e^{s_j}}
$$

Finally, the model uses the attention weights to take a weighted average of the value vectors.

## Example by Hand: Softmax Attention

Suppose one token has attention scores for three previous tokens:

$$
[2, 1, 0]
$$

We compute softmax.

First exponentiate each score:

$$
e^2 \approx 7. 389
$$

$$
e^1 \approx 2. 718
$$

$$
e^0 = 1
$$

Now sum them:

$$
7. 389 + 2. 718 + 1 = 11. 107
$$

Now divide each by the sum:

$$
\frac{7. 389}{11. 107} \approx 0. 665
$$

$$
\frac{2. 718}{11. 107} \approx 0. 245
$$

$$
\frac{1}{11. 107} \approx 0. 090
$$

So the attention weights are approximately:

$$
[0. 665, 0. 245, 0. 090]
$$

This means the model pays the most attention to the first token.

## Python Example: Softmax

```python
import math

scores = [2, 1, 0]

exps = [math.exp(s) for s in scores]
total = sum(exps)

weights = [x / total for x in exps]

print(weights)
```

Expected output:

```text
[0.665, 0.245, 0.090]
```

# 6. Feed-Forward Networks

After attention, each token passes through a small neural network called a feed-forward network, or FFN.

The attention layer lets tokens exchange information.

The feed-forward layer then transforms each token representation independently.

A simplified feed-forward layer looks like:

$$
\text{FFN}(x) = W_2 \sigma(W_1x + b_1) + b_2
$$

where:

* (W_1) and (W_2) are weight matrices,
* (b_1) and (b_2) are bias vectors,
* (\sigma) is a nonlinear activation function.

The FFN helps the model build more complex representations.

# 7. Training Data

LLMs are usually trained on large collections of text, such as:

* web pages,
* books,
* Wikipedia articles,
* code repositories,
* academic papers,
* news articles,
* forums and discussions.

The goal is to expose the model to many domains, styles, facts, and reasoning patterns.

However, raw internet data is messy. Training data usually needs filtering to remove:

* duplicate text,
* broken formatting,
* spam,
* boilerplate,
* low-quality pages,
* unsafe or toxic content.

The quality of the dataset matters a lot. More data helps only if the data is useful.

# 8. Decoding: Turning Probabilities into Text

After training, the model generates text one token at a time.

At each step, it produces a probability distribution over the vocabulary.

For example, after the phrase:

```text
The cat sat on the
```

the model might assign probabilities like:

| Token | Probability |
| ------ | ----------: |
| mat | 0. 50 |
| floor | 0. 25 |
| chair | 0. 15 |
| roof | 0. 07 |
| banana | 0. 03 |

Different decoding methods choose the next token in different ways.

## Greedy Decoding

Greedy decoding always chooses the most likely token.

In the example above, it chooses:

```text
mat
```

because it has probability:

$$
0. 50
$$

Greedy decoding is simple and fast, but it can become repetitive.

## Sampling

Sampling chooses randomly according to the probability distribution.

Using the table above, `"mat"` is most likely, but `"floor"` or `"chair"` could still be chosen.

This makes outputs more varied.

## Temperature Scaling

Before probabilities are computed, the model produces raw scores called logits.

Temperature changes how sharp or flat the probability distribution is.

If the logits are (z_i), temperature scaling uses:

$$
\frac{z_i}{\tau}
$$

where (\tau) is the temperature.

* Low temperature makes the model more confident and predictable.
* High temperature makes the model more random and creative.

## Example by Hand: Temperature

Suppose the logits are:

$$
[2, 1, 0]
$$

With temperature:

$$
\tau = 1
$$

the scaled logits stay the same:

$$
[2, 1, 0]
$$

The softmax probabilities are approximately:

$$
[0. 665, 0. 245, 0. 090]
$$

Now use a lower temperature:

$$
\tau = 0. 5
$$

Divide each logit by 0. 5:

$$
[4, 2, 0]
$$

Softmax gives approximately:

$$
[0. 867, 0. 117, 0. 016]
$$

The largest option becomes much more likely.

Now use a higher temperature:

$$
\tau = 2
$$

Divide each logit by 2:

$$
[1, 0. 5, 0]
$$

Softmax gives approximately:

$$
[0. 506, 0. 307, 0. 186]
$$

The distribution becomes flatter and more random.

## Python Example: Temperature Scaling

```python
import math

def softmax(logits):
    exps = [math.exp(x) for x in logits]
    total = sum(exps)
    return [x / total for x in exps]

def apply_temperature(logits, temperature):
    scaled = [x / temperature for x in logits]
    return softmax(scaled)

logits = [2, 1, 0]

for temp in [0.5, 1.0, 2.0]:
    probs = apply_temperature(logits, temp)
    print(f"Temperature {temp}: {probs}")
```

# 9. Top-k and Top-p Sampling

Two common sampling methods are top-k and top-p sampling.

## Top-k Sampling

Top-k sampling keeps only the (k) most likely tokens.

For example, if:

$$
k = 3
$$

then only the top 3 tokens are considered.

Using this distribution:

| Token | Probability |
| ------ | ----------: |
| mat | 0. 50 |
| floor | 0. 25 |
| chair | 0. 15 |
| roof | 0. 07 |
| banana | 0. 03 |

Top-3 sampling keeps:

| Token | Probability |
| ----- | ----------: |
| mat | 0. 50 |
| floor | 0. 25 |
| chair | 0. 15 |

Then the probabilities are renormalized.

The total probability is:

$$
0. 50 + 0. 25 + 0. 15 = 0. 90
$$

So the new probabilities are:

$$
p(\text{mat}) = \frac{0. 50}{0. 90} \approx 0. 556
$$

$$
p(\text{floor}) = \frac{0. 25}{0. 90} \approx 0. 278
$$

$$
p(\text{chair}) = \frac{0. 15}{0. 90} \approx 0. 167
$$

Top-k sampling removes unlikely tokens such as `"banana"`.

## Top-p Sampling

Top-p sampling, also called nucleus sampling, keeps the smallest set of tokens whose cumulative probability is at least (p).

For example, if:

$$
p = 0. 90
$$

Using the same table:

| Token | Probability | Cumulative |
| ------ | ----------: | ---------: |
| mat | 0. 50 | 0. 50 |
| floor | 0. 25 | 0. 75 |
| chair | 0. 15 | 0. 90 |
| roof | 0. 07 | 0. 97 |
| banana | 0. 03 | 1. 00 |

Top-p sampling with (p = 0. 90) keeps:

```text
mat, floor, chair
```

because their cumulative probability reaches 0. 90.

# 10. Prompting: Steering Without Retraining

At inference time, the model's weights usually stay fixed.

The main way to control the model is by changing the prompt.

For example:

```text
Complete the sentence:
The small furry animal was a
```

The model may assign high probability to:

```text
cat
```

But if the prompt changes to:

```text
Complete the sentence:
The huge wild animal was a
```

the model may assign higher probability to:

```text
lion
```

The model is sensitive to context because its job is to predict the next token from the previous tokens.

This is why prompting matters.

A prompt can specify:

* the task,
* the tone,
* the format,
* examples,
* constraints,
* the role the model should imitate.

## Example Prompt

```text
Explain gradient descent in simple terms.
Use one analogy.
Then give one small numerical example.
```

This prompt gives the model clear instructions about content and structure.

# 11. In-Context Learning

LLMs can often learn from examples placed directly in the prompt.

This is called in-context learning.

For example:

```text
Convert English to French.

English: cat
French: chat

English: dog
French: chien

English: house
French:
```

The model sees the pattern and completes:

```text
maison
```

No weights are updated. The learning happens inside the context window.

# 12. Adapting LLMs to New Domains

Sometimes prompting is not enough.

For example, a company may want a model to understand:

* internal documents,
* legal contracts,
* medical terminology,
* customer support style,
* software documentation.

There are several ways to adapt an LLM.

## Full Fine-Tuning

In full fine-tuning, all model parameters are updated using new training data.

This gives the most flexibility, but it is expensive.

It requires:

* labeled or carefully prepared data,
* GPUs,
* memory,
* training expertise,
* evaluation to avoid damaging existing capabilities.

## Parameter-Efficient Fine-Tuning

Parameter-efficient fine-tuning updates only a small number of extra parameters.

Examples include:

* LoRA,
* adapters,
* prefix tuning.

The original model mostly stays frozen.

This is cheaper than full fine-tuning.

## LoRA Idea

LoRA stands for Low-Rank Adaptation.

Instead of updating a large weight matrix (W), LoRA learns a small update:

$$
W' = W + \Delta W
$$

where:

$$
\Delta W = AB
$$

If (A) and (B) are small low-rank matrices, then the number of trainable parameters is much smaller.

## Example by Hand: LoRA Parameter Savings

Suppose a normal weight matrix has size:

$$
1000 \times 1000
$$

That means it has:

$$
1000 \times 1000 = 1{,}000{,}000
$$

parameters.

Now suppose LoRA uses rank:

$$
r = 10
$$

Then LoRA uses two smaller matrices:

$$
A: 1000 \times 10
$$

$$
B: 10 \times 1000
$$

The number of LoRA parameters is:

$$
1000 \times 10 + 10 \times 1000
$$

$$
= 10{,}000 + 10{,}000
$$

$$
= 20{,}000
$$

So instead of training 1, 000, 000 parameters, we train only 20, 000.

The percentage is:

$$
\frac{20{,}000}{1{,}000{,}000} = 0. 02
$$

$$
= 2%
$$

LoRA updates only about 2% as many parameters in this example.

## Python Example: LoRA Parameter Count

```python
def full_params(in_dim, out_dim):
    return in_dim * out_dim

def lora_params(in_dim, out_dim, rank):
    return in_dim * rank + rank * out_dim

in_dim = 1000
out_dim = 1000
rank = 10

full = full_params(in_dim, out_dim)
lora = lora_params(in_dim, out_dim, rank)

print("Full fine-tuning parameters:", full)
print("LoRA parameters:", lora)
print("Percentage:", 100 * lora / full, "%")
```

# 13. Summary of Adaptation Methods

| Method | What Changes? | Data Needed | Cost | Main Use |
| ---------------- | -------------------------- | --------------------- | ---------- | ---------------------- |
| Prompting | Nothing | Instructions/examples | Very low | Quick control |
| Soft prompting | Learned prompt embeddings | Task data | Low | Specialized prompting |
| LoRA/adapters | Small extra parameter sets | Task data | Medium-low | Domain adaptation |
| Full fine-tuning | All weights | Larger training set | High | Major behavior changes |

# 14. Strengths of LLMs

LLMs are powerful because they can:

* answer questions,
* summarize text,
* translate languages,
* write code,
* explain concepts,
* classify text,
* imitate writing styles,
* reason through some problems,
* combine information from long contexts.

A single model can perform many tasks because the training objective is general: predict the next token.

# 15. Weaknesses of LLMs

LLMs also have important limitations.

## Hallucinations

An LLM may generate something that sounds correct but is false.

This happens because the model is generating likely text, not directly checking truth.

## Bias

Models can learn biases from their training data.

If the data contains stereotypes or unfair patterns, the model may reproduce them.

## Limited Context

A model can only use the information inside its context window.

If important information is missing from the prompt, the model may guess.

## Cost

Large models require expensive hardware for training and sometimes for inference.

## Interpretability

It is often difficult to know exactly why a model produced a specific answer.

# 16. Open Research Questions

Important open questions include:

* How can we make LLMs more truthful?
* How can we reduce hallucinations?
* How can we make models cheaper to train and run?
* How can models handle longer contexts efficiently?
* How can we better understand what is happening inside the network?
* How can we make models safer and better aligned with human goals?
