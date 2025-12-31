# RAG with Vector Databases

Retrieval-Augmented Generation (RAG) extends LLM capabilities by grounding responses in external knowledge. This approach addresses key limitations of pure LLMs: knowledge cutoffs, hallucinations, and the inability to cite sources.

## The Core Problem

LLMs have impressive capabilities but significant limitations:

- **Knowledge cutoff**: Training data has a fixed end date
- **Hallucinations**: Models can generate plausible but false information
- **No source attribution**: Responses don't cite where information came from
- **Context limits**: Even large context windows can't hold entire knowledge bases

RAG solves these by retrieving relevant information at query time and including it in the prompt.

## How RAG Works

The basic RAG pipeline has two phases:

### Indexing Phase (Offline)

```
Documents ──► Chunking ──► Embedding ──► Vector Database
```

1. **Chunking**: Split documents into smaller pieces (typically 256–1024 tokens)
2. **Embedding**: Convert each chunk into a dense vector using an embedding model
3. **Storage**: Store vectors and their source text in a vector database

### Query Phase (Online)

```
Query ──► Embed ──► Search ──► Top-K Chunks ──► Prompt + Context ──► LLM ──► Answer
```

1. **Embed query**: Convert user query to a vector using the same embedding model
2. **Search**: Find the K most similar chunks using vector similarity
3. **Augment**: Add retrieved chunks to the prompt as context
4. **Generate**: LLM generates a response grounded in the retrieved content

## Key Concepts

### Vector Embeddings

Embeddings are dense numerical vectors (typically 384–4096 dimensions) that capture semantic meaning. Similar concepts have similar embeddings, enabling semantic search beyond keyword matching.

```
"How do I install Python?" → [0.12, -0.34, 0.56, ...]
                                     ↓ similar to
"Python installation guide" → [0.11, -0.32, 0.58, ...]
```

### Similarity Metrics

Common ways to measure vector similarity:

| Metric | Description | Best For |
|--------|-------------|----------|
| Cosine similarity | Angle between vectors | Normalized embeddings |
| Dot product | Magnitude-aware similarity | When magnitude matters |
| Euclidean distance | Straight-line distance | Dense clusters |

### Chunking Strategies

How you split documents affects retrieval quality:

| Strategy | Pros | Cons |
|----------|------|------|
| Fixed size (tokens) | Simple, predictable | May split sentences |
| Sentence-based | Preserves meaning | Variable chunk sizes |
| Paragraph-based | Natural boundaries | Chunks may be too large |
| Recursive | Adapts to content | More complex to implement |

### Hybrid Search

Combining vector search with keyword matching often improves recall:

```
Final Score = α × VectorScore + (1-α) × KeywordScore
```

Use keyword search for exact matches (IDs, names) and vector search for semantic similarity.

## Architecture Patterns

### Basic RAG

```
┌─────────────────────────────────────────────────────────┐
│                       User Query                         │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Embedding Model                        │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Vector Database                       │
│              (Retrieve top-K similar chunks)             │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│           Prompt = Query + Retrieved Chunks              │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                          LLM                             │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Final Response                        │
└─────────────────────────────────────────────────────────┘
```

### Advanced Patterns

- **Query expansion**: Rewrite or expand queries before retrieval
- **Re-ranking**: Use a second model to re-order retrieved chunks
- **Iterative retrieval**: Retrieve → Generate → Retrieve more if needed
- **Multi-index**: Search across multiple specialized indexes

## Vector Database Options

| Database | Type | Strengths |
|----------|------|-----------|
| Pinecone | Managed | Easy to use, scalable |
| Weaviate | Self-hosted/Cloud | Rich filtering, hybrid search |
| Qdrant | Self-hosted/Cloud | Good performance, Rust-based |
| Chroma | Self-hosted | Simple, Python-native |
| pgvector | PostgreSQL extension | Use existing Postgres |
| FAISS | Library | High performance, research-grade |

## When to Use RAG

**Good fit:**
- Knowledge bases that change frequently
- Domain-specific information not in training data
- Applications requiring source citations
- Reducing hallucinations with factual grounding

**Consider alternatives when:**
- Data is small enough to fit in context
- Real-time latency is critical (retrieval adds latency)
- Knowledge is well-covered by the base model

## Common Pitfalls

1. **Chunk size mismatch**: Chunks too small lose context; too large dilute relevance
2. **Embedding model mismatch**: Use same model for indexing and querying
3. **Ignoring metadata**: Filter by date, source, or category before vector search
4. **No evaluation**: Test retrieval quality independently from generation

## Implementation Checklist

- [ ] Choose embedding model (OpenAI, Cohere, open-source)
- [ ] Design chunking strategy based on document types
- [ ] Select vector database for your scale and requirements
- [ ] Implement retrieval pipeline with appropriate K value
- [ ] Craft prompt template that incorporates retrieved context
- [ ] Add source citations to responses
- [ ] Set up evaluation for retrieval and generation quality