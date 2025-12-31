# Token Embeddings

This section explains how language models convert discrete tokens into continuous vector representations.

## Overview

Token embeddings are the foundation of how neural language models process text. Each token in the vocabulary is mapped to a dense vector in a high-dimensional space, allowing the model to learn semantic relationships between words.

## Key Concepts

- **Vocabulary**: The set of all tokens the model recognizes
- **Embedding dimension**: The size of the vector representing each token (e.g., 768, 1024, 4096)
- **Embedding matrix**: A learned lookup table mapping token IDs to vectors
- **Contextual embeddings**: Token representations that vary based on surrounding context

## Embedding Lookup

$$
E = \text{EmbeddingMatrix}[token\_id]
$$

The embedding matrix has shape `(vocab_size, embedding_dim)`. Looking up a token is simply indexing into this matrix.

## From Static to Contextual

Early embeddings (Word2Vec, GloVe) assigned fixed vectors to words. Transformer-based models produce contextual embeddings where the same token gets different representations depending on context.

## Status

Detailed content pending.