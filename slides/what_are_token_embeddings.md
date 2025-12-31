# Token Embeddings

Token embeddings are the foundation of how neural language models process text. They transform discrete symbols (words, subwords, characters) into continuous vector representations that neural networks can manipulate.

## Why Embeddings?

Neural networks operate on numbers, not text. Embeddings solve the representation problem:

**The challenge**: How do you represent "cat" in a way that captures:
- Its similarity to "dog" (both are pets)
- Its difference from "car" (different category)
- Its relationship to "kitten" (same species, different age)

**The solution**: Map each token to a point in high-dimensional space where distance reflects semantic relationships.

## From Tokens to Vectors

### Tokenization First

Before embedding, text is split into tokens:

```
"The cat sat on the mat"
    ↓ tokenization
["The", " cat", " sat", " on", " the", " mat"]
    ↓ token IDs
[464, 3797, 3332, 319, 262, 2603]
```

Modern models use subword tokenization (BPE, SentencePiece) to handle rare words:

```
"unbelievably" → ["un", "believ", "ably"]
```

### The Embedding Matrix

The embedding layer is a learned lookup table:

$$
E = W_e[token\_id]
$$

Where:
- $W_e$ is the embedding matrix with shape `(vocab_size, embedding_dim)`
- Typical dimensions: 768 (BERT), 4096 (GPT-3), 12288 (GPT-4)

```
Vocabulary: [cat, dog, car, ...]  (50,000+ entries)
                ↓
Embedding Matrix: 50,000 × 768
                ↓
"cat" → [0.12, -0.34, 0.56, ..., 0.89]  (768 numbers)
```

## Static vs. Contextual Embeddings

### Static Embeddings (Word2Vec, GloVe)

Each word has one fixed vector, regardless of context:

```
"I went to the bank to deposit money"
"I sat on the river bank"
         ↓
"bank" → same vector in both sentences ❌
```

### Contextual Embeddings (Transformers)

The same token gets different representations based on surrounding words:

```
"I went to the bank to deposit money"
"bank" → [0.12, -0.34, ...] (financial meaning)

"I sat on the river bank"
"bank" → [0.45, 0.23, ...]  (geographical meaning)
```

This is achieved by processing all tokens together through attention layers.

## How Embeddings Capture Meaning

### Semantic Similarity

Similar concepts cluster together in embedding space:

```
                    "royalty"
                       ↑
"king" ←-------- "queen" --------→ "prince"
   ↓                                   ↓
"man" ←------ distance --------→ "woman"
```

### Analogies as Vector Arithmetic

The famous Word2Vec result:

$$
\vec{king} - \vec{man} + \vec{woman} \approx \vec{queen}
$$

This works because the embedding space encodes relationships consistently.

### Visualization

Embeddings can be projected to 2D/3D for visualization using t-SNE or UMAP:

```
         ↑
     "cat" • • "dog"
           •
         "pet"
         
    "car" • • "truck"
           •
       "vehicle"
         ↓
```

## The Embedding Process in Transformers

### Input Processing

```
┌─────────────────────────────────────────────────────────┐
│  Input Text: "The cat sat"                               │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Tokenizer: [464, 3797, 3332]                           │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Token Embeddings: Look up each ID in W_e               │
│  → [[0.1, -0.2, ...], [0.3, 0.1, ...], [0.2, -0.1, ...]]│
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Position Embeddings: Add position information          │
│  → Token embedding + Position embedding                 │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Transformer Layers: Contextualize through attention    │
└─────────────────────────────────────────────────────────┘
```

### Position Embeddings

Since attention is permutation-invariant, position must be injected:

**Sinusoidal (original Transformer)**:
$$
PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d})
$$
$$
PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d})
$$

**Learned** (BERT, GPT): Train position embeddings like token embeddings

**Rotary (RoPE)**: Encode position in the attention mechanism itself

## Embedding Models for Applications

### Sentence Embeddings

For search and similarity, you often want to embed entire sentences:

| Model | Dimensions | Use Case |
|-------|------------|----------|
| text-embedding-3-small | 1536 | OpenAI, balanced |
| text-embedding-3-large | 3072 | OpenAI, high quality |
| all-MiniLM-L6-v2 | 384 | Open source, fast |
| e5-large-v2 | 1024 | Open source, high quality |
| bge-large-en-v1.5 | 1024 | Open source, multilingual |

### Computing Similarity

Common metrics for comparing embeddings:

**Cosine similarity** (most common):
$$
\text{sim}(a, b) = \frac{a \cdot b}{\|a\| \|b\|}
$$

**Dot product** (when embeddings are normalized):
$$
\text{sim}(a, b) = a \cdot b
$$

## Practical Considerations

### Dimension vs. Quality Trade-offs

| Dimension | Memory | Speed | Quality |
|-----------|--------|-------|---------|
| 384 | Low | Fast | Good |
| 768 | Medium | Medium | Better |
| 1536+ | High | Slower | Best |

### Embedding Caching

Embeddings are deterministic—cache them:

```python
# Pseudo-code
cache = {}
def get_embedding(text):
    if text not in cache:
        cache[text] = model.embed(text)
    return cache[text]
```

### Batch Processing

Embed multiple texts at once for efficiency:

```python
# Slow: one at a time
embeddings = [model.embed(text) for text in texts]

# Fast: batched
embeddings = model.embed(texts)  # All at once
```

## Key Takeaways

1. Embeddings convert discrete tokens to continuous vectors
2. Modern embeddings are contextual—same word, different meanings
3. Semantic similarity maps to vector distance
4. Choose embedding models based on your quality/speed trade-offs
5. Cache and batch embeddings for efficiency