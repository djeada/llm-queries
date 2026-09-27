# Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) is a system pattern: retrieve external
evidence at request time, give selected evidence to a model, and ask the model
to answer using that evidence.

A vector database is one possible retrieval component. It is not the definition
of RAG.

## Why Retrieve?

Retrieval is useful when the answer depends on information that is:

- too large to include in every prompt
- private or organization-specific
- updated more often than the model
- required for citation or auditability
- best selected from many possible documents

RAG does not automatically eliminate hallucinations. It creates an opportunity
to ground an answer in evidence; the system still has to retrieve the right
evidence and use it correctly.

## Separate the Two Problems

A RAG system has at least two distinct quality questions:

1. **Retrieval:** Did the system find the evidence needed to answer?
2. **Generation:** Given that evidence, did the model answer faithfully?

Debug them separately.

```text
question
   │
   ▼
retrieval ─────► candidate evidence
   │
   │              retrieval metrics
   │              recall / ranking / coverage
   ▼
context construction
   │
   ▼
generation ────► answer + citations
                  generation metrics
                  support / correctness / completeness
```

If the right evidence never reaches the model, changing the generation prompt
cannot repair the retrieval failure.

## Retrieval Is Broader Than Vector Search

Possible retrieval signals include:

- lexical / keyword search
- vector similarity
- metadata filters
- database queries
- graph traversal
- structured API calls
- recency or authority rules
- hybrid combinations of several methods

Choose signals based on the information need.

Exact identifiers, error codes, names, and quoted phrases may benefit from
lexical search. Paraphrased concepts may benefit from semantic embeddings.
Structured facts may be better retrieved with SQL or an API than with document
chunks.

## A General Pipeline

### Index / preparation path

```text
source data
   │
   ├─ parse / normalize
   ├─ preserve source identity and metadata
   ├─ create retrieval units
   └─ build one or more search indexes
```

### Query path

```text
user question
   │
   ├─ optional query rewrite / decomposition
   ▼
candidate retrieval
   │
   ├─ filters
   ├─ lexical / vector / structured search
   ▼
optional reranking
   ▼
context selection
   ▼
model answer
   ▼
claim / citation validation
```

Every arrow is a place where quality can fail.

## Retrieval Units

"Chunking" is not a single correct token size.

A useful retrieval unit should preserve enough context to answer a question
without adding so much unrelated text that ranking becomes noisy.

Possible boundaries include:

- headings and sections
- paragraphs
- records or rows
- functions/classes in source code
- support tickets
- table rows with surrounding headers
- fixed-size windows when natural boundaries are unavailable

Chunking strategy should be evaluated on representative queries.

## Embeddings

An embedding model maps text to vectors for a similarity or retrieval objective.

Do not choose an embedding model from vector dimension alone. Dimension affects
storage and compute; retrieval quality is empirical.

For a vector retriever, record:

- exact embedding model/version
- preprocessing
- similarity metric
- index configuration
- query/document encoding conventions

Index and query vectors must be compatible with the chosen model and retrieval
setup.

## Hybrid Retrieval

Hybrid systems combine signals instead of assuming one search method is enough.

A typical design might:

1. apply metadata filters
2. retrieve lexical candidates
3. retrieve semantic candidates
4. merge candidates
5. rerank the merged set
6. select evidence under a context budget

Do not assume a fixed linear score formula transfers across systems. Score
scales differ by retriever, so fusion/reranking should be validated empirically.

## Reranking

A first-stage retriever is usually optimized for recall and speed. A more
expensive reranker can then score a smaller candidate set more precisely.

```text
large corpus
   │
fast retrieval
   ▼
50 candidates
   │
reranker
   ▼
5 evidence units
```

The numbers are illustrative, not recommended defaults.

## Context Construction

Retrieved text should keep provenance.

Useful context fields include:

```text
source_id:
title:
document_date:
section:
retrieved_text:
permissions / tenant:
```

The model should be told how to cite source IDs and what to do when the evidence
is missing or contradictory.

Avoid mixing untrusted retrieved instructions with application instructions
without clear data-flow and permission controls. RAG introduces a prompt-
injection surface when retrieved content can contain adversarial text.

## Citations

A citation is useful only when it actually supports the claim.

Evaluate citation quality at the claim level:

- **entailment/support:** does the cited evidence support the claim?
- **completeness:** are important factual claims cited?
- **source quality:** is the source appropriate for the claim?
- **correct mapping:** does the citation point to the evidence the system used?

A system can produce perfectly formatted citations that support nothing.

## Retrieval Evaluation

Create a labeled query set representative of real usage.

Depending on the task, useful metrics can include:

- recall@k
- precision@k
- mean reciprocal rank (MRR)
- nDCG
- answerable-evidence coverage

Metrics are only meaningful relative to the labeled task.

Also inspect failure categories:

- correct document not indexed
- wrong metadata filter
- query wording mismatch
- chunk boundary lost necessary context
- stale source outranked current source
- duplicate candidates crowded out diversity

## Generation Evaluation

Given a fixed retrieved context, measure separately:

- factual support
- answer correctness
- completeness
- abstention when evidence is insufficient
- citation accuracy
- required format

Freezing retrieval while evaluating generation makes it possible to identify
which layer changed.

## End-to-End Evaluation

Finally test the complete path.

A useful case records:

```text
question:
expected evidence:
retrieved evidence:
final answer:
citations:
retrieval pass/fail:
generation pass/fail:
end-to-end pass/fail:
failure category:
```

This is more actionable than one overall "RAG quality" score.

## Failure Handling

A grounded system needs an explicit insufficient-evidence path.

Examples:

- ask a clarifying question
- state that the indexed sources do not answer the question
- broaden retrieval
- route to a structured system of record
- require human review

"Always answer" is usually a poor default when evidence is mandatory.

## When RAG Is Not the Right Tool

Consider a simpler design when:

- the authoritative data already fits reliably in context
- the answer is better produced by a structured database/API query
- retrieval latency is unacceptable
- the corpus is tiny and deterministic lookup is simpler
- the task does not benefit from external evidence

Do not add a vector database just because the application contains an LLM.

## Implementation Checklist

- [ ] Define which questions the system must answer.
- [ ] Build representative labeled retrieval queries.
- [ ] Preserve document/source metadata and access controls.
- [ ] Choose retrieval methods based on query types.
- [ ] Evaluate retrieval before tuning generation.
- [ ] Define context selection and evidence-budget rules.
- [ ] Require explicit behavior for insufficient evidence.
- [ ] Validate claim-to-citation support.
- [ ] Record retriever/model/index versions in evaluations.
- [ ] Re-run the same evals when chunking, embeddings, ranking, or prompts change.

## Key Takeaway

RAG is not "embed documents, search top-k, paste chunks into a prompt."

It is an evidence-selection system whose retrieval and generation components
need separate, repeatable evaluation.
