# RAG Quality Audit

Use this prompt to audit retrieval-augmented generation workflows. It separates
retrieval problems from generation problems and checks whether answers are
grounded in the retrieved sources.

## Best For

- Debugging hallucinations in RAG systems.
- Checking chunking, retrieval, reranking, and citation quality.
- Improving knowledge-base question answering.
- Reviewing whether retrieved context actually supports the final answer.

## Required Input

- User question.
- Retrieved chunks with source labels.
- Final model answer.
- Retrieval settings if available: top-k, filters, embedding model, chunk size,
  reranker, or hybrid search.
- Expected answer or known ground truth, if available.

## Prompt

```text
Act as a RAG quality auditor.

Audit this retrieval-augmented answer. Separate retrieval quality from answer
quality and identify the highest-impact fixes.

User question:
"""
[QUESTION]
"""

Retrieved context:
"""
[PASTE CHUNKS WITH SOURCE IDS, TITLES, DATES, AND METADATA IF AVAILABLE]
"""

Final answer:
"""
[PASTE ANSWER]
"""

Retrieval settings:
"""
[TOP-K, CHUNK SIZE, EMBEDDING MODEL, FILTERS, RERANKING, HYBRID SEARCH, OR UNKNOWN]
"""

Ground truth or expected answer:
"""
[OPTIONAL]
"""

Return:
1. Verdict: supported, partially supported, unsupported, or contradicted.
2. Retrieval audit:
   - Relevant chunks found
   - Missing evidence
   - Irrelevant or distracting chunks
   - Metadata/filtering issues
3. Answer audit:
   - Claims supported by sources
   - Claims not supported by sources
   - Claims contradicted by sources
   - Citation problems
4. Likely root cause: retrieval, chunking, ranking, prompt, generation, or data.
5. Recommended fixes ordered by impact.
6. Test queries to add to the RAG evaluation set.

Rules:
- Cite source IDs from the retrieved context when judging support.
- Do not use outside knowledge unless explicitly allowed.
- If the retrieved context is insufficient, say what evidence is missing.
- Prefer precise fixes over generic advice.
```

## Follow-Up: Improve Retrieval

```text
Suggest retrieval improvements for these failed RAG cases.

Failed cases:
"""
[PASTE QUESTIONS, RETRIEVED CHUNKS, ANSWERS, AND FAILURE NOTES]
"""

Return:
1. Failure pattern summary.
2. Chunking changes to test.
3. Metadata or filtering changes to test.
4. Query rewriting or expansion strategies.
5. Reranking or hybrid-search changes.
6. Evaluation cases to confirm improvement.
```

## Review Checklist

- Retrieval and generation are judged separately.
- Unsupported claims are listed explicitly.
- Fixes are tied to observed failures.
- Suggested tests would catch the same issue later.
