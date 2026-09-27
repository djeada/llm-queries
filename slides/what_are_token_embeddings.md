# Token Embeddings

Token embeddings convert discrete token IDs into vectors that a neural network
can process.

They are one stage in a language model's representation pipeline. The raw
lookup vector for a token is not the same thing as the token's final,
context-dependent representation after transformer layers.

## From Text to Token IDs

A tokenizer maps text to a sequence of token IDs.

```text
"The cat sat."
     ↓ tokenizer
[token_17, token_204, token_991, token_4]
     ↓ IDs
[17, 204, 991, 4]
```

The exact token boundaries and IDs depend on the tokenizer.

Common tokenizer families include byte-pair encoding and unigram /
SentencePiece-style tokenization. Different models can tokenize the same text
differently.

## The Embedding Lookup

Let the vocabulary size be $V$ and model width be $d$.

The learned token-embedding matrix can be written as:

$$
W_E \in \mathbb{R}^{V \times d}
$$

For token ID $i$, the initial embedding is the corresponding row:

$$
e_i = W_E[i]
$$

This is effectively a learned lookup table.

```text
token ID
   │
   ▼
┌────────────────────────────┐
│ token embedding matrix W_E │
└────────────────────────────┘
   │
   ▼
d-dimensional vector
```

The embedding dimension is an architectural choice. It should not be inferred
from a product name unless the architecture is publicly documented.

## Input Embeddings vs Contextual Representations

This distinction is important.

### Input embedding

Before the transformer processes context, a token ID maps to an initial vector.

The same token ID receives the same lookup vector from $W_E$.

### Contextual representation

After attention and feed-forward layers, the representation depends on the
surrounding sequence.

For example, the token corresponding to "bank" can participate in different
contextual states in:

```text
I deposited money at the bank.
We sat on the river bank.
```

The contextual difference is produced by the network processing the sequence,
not by changing the underlying token ID.

## Position Information

Attention alone does not encode token order, so transformer architectures add or
incorporate positional information.

Common approaches include:

- learned absolute position embeddings
- sinusoidal position encodings
- rotary position embeddings (RoPE)
- relative-position biases or related mechanisms

The exact mechanism is architecture-specific.

It is therefore safer to say:

```text
token representation = token information + architecture-specific position information
```

than to assume every transformer literally adds a learned position vector.

## Do Embeddings "Contain Meaning"?

Learned vector spaces often organize useful linguistic and semantic
relationships, but the statement needs precision.

For older static word embeddings such as Word2Vec, one word type is assigned one
vector, and geometric relationships can directly encode useful regularities.

For transformer language models:

- the input embedding is only an initial representation
- meaning is heavily shaped by later contextual processing
- geometric distance in the raw token-embedding matrix is not automatically a
  calibrated semantic-similarity metric

For semantic search, use an embedding model specifically trained or evaluated
for representing sentences/documents for similarity or retrieval.

## Static Word Embeddings

Classic systems such as Word2Vec and GloVe assign one learned vector per word.

That means the vector for "bank" is the same before context is considered.

A famous observation from Word2Vec-style spaces is that some relationships can
appear approximately linear, for example:

$$
v(\text{king}) - v(\text{man}) + v(\text{woman})
\approx v(\text{queen})
$$

This is an empirical property of some trained spaces, not a law that all
embedding models must satisfy.

## Sentence and Document Embeddings

Retrieval systems usually need one vector for a larger piece of text.

A text-embedding model may map:

```text
"How do I reset my password?"
```

to:

$$
z \in \mathbb{R}^{d}
$$

The model is typically trained so that texts with useful semantic relationships
are close under a chosen similarity measure.

Different embedding models can use different vector dimensions. Higher
dimension by itself does **not** imply higher quality.

## Similarity Measures

### Cosine similarity

$$
\operatorname{cos}(a,b)
=
\frac{a \cdot b}{\|a\|\|b\|}
$$

Cosine similarity compares direction while normalizing vector magnitude.

### Dot product

$$
a \cdot b
$$

Dot product is often used when the embedding model and index are designed for
it. If vectors are unit-normalized, dot product and cosine similarity are
equivalent.

### Distance

Some systems use Euclidean or other distances.

Use the metric recommended for the embedding model and evaluate it on the actual
retrieval task.

## Embeddings in Retrieval

A simple semantic-retrieval pipeline looks like:

```text
documents
   │
   ├─ chunk / prepare text
   │
   ├─ embed
   ▼
vector index

query
   │
   ├─ embed with compatible model
   ▼
nearest-neighbor search
   │
   ▼
candidate documents
   │
   ▼
optional reranking / filtering
```

The quality of the system depends on more than the embedding model:

- document chunking
- query formulation
- index metric
- metadata filtering
- domain mismatch
- reranking
- evaluation data

## Dimension, Memory, and Index Size

If one embedding contains $d$ floating-point values, raw storage grows roughly
linearly with $d$ and the number of vectors.

For $N$ vectors stored as 32-bit floats:

$$
\text{bytes} \approx N \times d \times 4
$$

This is only the raw vector storage. Real indexes also have metadata and
index-structure overhead.

Dimension therefore affects memory and search cost, but it is not a quality
score.

## Caching

If the same embedding model, model version, preprocessing, and input text are
used repeatedly, caching can avoid redundant work.

A robust cache key should include more than the text:

```text
(model identifier, model version, preprocessing version, input text)
```

This avoids silently reusing old vectors after changing the embedding model or
normalization pipeline.

## Batch Processing

Many embedding runtimes can process multiple texts per request or batch.

Batching can improve throughput, but the ideal batch size depends on:

- runtime
- hardware
- sequence lengths
- memory limits
- latency requirements

Measure it instead of assuming that the largest batch is best.

## How to Evaluate an Embedding Model

Do not select an embedding model from vector dimension or a generic leaderboard
alone.

Build a task-specific evaluation set:

1. collect representative queries
2. label relevant documents or pairs
3. run retrieval with each candidate
4. measure metrics such as recall@k, precision@k, MRR, or nDCG as appropriate
5. inspect important failure cases
6. record latency, index size, and operational constraints

For RAG, retrieval quality should be measured separately from generation
quality.

## Common Misconceptions

### "The nearest token vectors must have similar meanings"

Not necessarily. Raw language-model token embeddings are not guaranteed to be a
semantic-search space.

### "More dimensions means better embeddings"

No. Dimension is an architecture and storage tradeoff. Quality is empirical.

### "The same word has one embedding in a transformer"

Its initial token lookup is fixed for the token ID, but later hidden states are
context-dependent.

### "Embeddings are always deterministic"

Do not assume this as a universal API guarantee. Treat determinism as something
to verify for the specific model/runtime and version.

## Key Takeaways

- Token IDs are mapped to learned input vectors.
- Transformer layers turn those inputs into contextual representations.
- Position handling is architecture-specific.
- Semantic-search embeddings should be selected for the retrieval task.
- Vector dimension affects storage and compute, not guaranteed quality.
- Evaluate embeddings with labeled retrieval examples and record the exact
  model/configuration used.
