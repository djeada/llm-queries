# Glossary

Definitions for terms used across the repository. Definitions prefer durable
concepts over product-specific defaults or parameter ranges.

## Core Concepts

- **LLM (Large Language Model)**: A language model with enough capacity and
  training scale to perform a broad range of language tasks. "Large" is
  relative to its era and does not imply a fixed parameter threshold.
- **Token**: A unit produced by a tokenizer and consumed by a model. A token can
  represent a whole word, part of a word, punctuation, bytes, or other symbol
  sequences depending on the tokenizer.
- **Prompt**: Input provided to a model or model-powered system, including task
  instructions, context, examples, and output constraints.
- **Context window**: The maximum amount of tokenized input/output state a model
  can attend to in one inference context. The exact limit is model- and
  runtime-specific.
- **Inference**: Running a trained model to produce predictions, scores, or
  generated outputs from new input.

## Model Training & Adaptation

- **Pre-training**: Large-scale training before task-specific adaptation. For
  autoregressive language models this commonly includes next-token prediction.
- **Fine-tuning**: Updating a pretrained model on additional data to change or
  specialize its behavior.
- **RLHF (Reinforcement Learning from Human Feedback)**: A family of methods
  that uses human preference information in post-training, often through a
  learned reward/preference signal and an optimization step.
- **LoRA (Low-Rank Adaptation)**: A parameter-efficient adaptation method that
  learns low-rank updates to selected weight matrices while leaving the base
  weights frozen.
- **Checkpoint**: A saved set of model parameters and associated training state
  or configuration at a particular point.

## Prompting & Context

- **Zero-shot prompting**: Asking a model to perform a task without providing
  demonstrations in the prompt.
- **One-shot prompting**: Providing one demonstration of the desired behavior.
- **Few-shot prompting**: Providing a small number of demonstrations in the
  prompt.
- **Chain-of-thought prompting**: A historical prompting technique that asks for
  intermediate reasoning text. Generated reasoning text should be treated as an
  output to evaluate, not as guaranteed access to the model's internal
  reasoning process.
- **System instruction / system prompt**: Higher-priority instructions supplied
  by the application or model interface to shape behavior across a
  conversation/request.
- **Prompt template**: A reusable input structure with placeholders for
  task-specific values.
- **In-context learning**: Behavior in which a model adapts to instructions or
  examples contained in its current context without updating model weights.

## Generation Parameters

- **Logit**: A model's unnormalized score for a possible output token before
  softmax or another normalization step.
- **Temperature**: A parameter that rescales logits before sampling. Lower
  temperature sharpens the distribution; higher temperature flattens it. Exact
  supported ranges and edge behavior are runtime-specific.
- **Top-p (nucleus sampling)**: Sampling restricted to the smallest set of
  tokens whose cumulative probability reaches a selected threshold (p).
- **Top-k**: Sampling restricted to the (k) highest-probability candidate
  tokens.
- **Maximum output tokens**: A limit on generated tokens. Interfaces differ in
  naming and whether the limit interacts with the overall context budget.
- **Stop sequence**: A configured sequence that causes generation to stop when
  emitted or matched, depending on the runtime.

## Performance & Efficiency

- **Latency**: Elapsed time for an inference request. Specify whether a metric
  means time to first token, time to complete response, or another boundary.
- **Throughput**: Work completed per unit time, such as generated tokens per
  second or requests per second.
- **Quantization**: Representing model weights and/or activations with reduced
  numerical precision to lower memory or compute cost, often with a quality
  tradeoff.
- **Batching**: Processing multiple inputs or generation sequences together to
  improve hardware utilization.
- **Streaming**: Returning partial output incrementally instead of waiting for a
  complete response.
- **KV cache**: Cached attention keys and values used during autoregressive
  generation so prior tokens do not need to be recomputed from scratch at each
  step.

## Retrieval & Augmentation

- **RAG (Retrieval-Augmented Generation)**: A system pattern that retrieves
  external information and supplies selected evidence to a generator.
- **Embedding**: A vector representation produced by a model. Whether geometric
  distance corresponds to semantic similarity depends on how the embedding
  model was trained and evaluated.
- **Vector index / vector database**: A system for storing vectors and
  retrieving nearby candidates under a chosen similarity or distance metric.
- **Chunking**: Splitting larger source material into retrieval units. Useful
  chunk size depends on document structure, embedding model, retrieval method,
  and task.
- **Semantic search**: Retrieval based on learned representations of meaning or
  relevance rather than only exact lexical matching.
- **Reranker**: A model or scoring stage that reorders an initial retrieval set
  using a more expensive relevance signal.

## Agent & Tool Use

- **Agent**: A model-powered system that can choose or execute actions across
  multiple steps while maintaining task state.
- **Tool calling / function calling**: Producing a structured request for an
  external operation such as search, code execution, database access, or an API
  call.
- **ReAct**: A family of agent prompting patterns that interleave model
  deliberation with actions and observations from an environment.
- **Multi-agent system**: A system that assigns work or state to multiple
  model-powered components. Multiple agents are an architectural choice, not an
  automatic quality improvement.
- **Approval gate**: A boundary that requires a person or policy check before a
  higher-risk action is executed.

## Evaluation & Reliability

- **Evaluation (eval)**: A repeatable procedure for measuring model/system
  behavior against defined examples and success criteria.
- **Regression test**: An eval intended to detect whether a previously working
  behavior became worse after a change.
- **Hallucination**: Generated content that is unsupported by the provided
  evidence or incorrect relative to the task's factual requirements.
- **Grounding**: Connecting outputs to supplied or retrieved evidence so claims
  can be checked against that evidence.
- **Calibration**: The relationship between a system's expressed confidence (or
  confidence score) and empirical correctness.
- **Benchmark contamination**: Overlap between evaluation material and training,
  fine-tuning, or development data that can make measured performance
  misleading.
- **Pass rate**: Fraction of evaluation cases that meet all defined pass
  criteria. A pass rate is meaningful only together with the evaluation set and
  scoring method.

## Safety & Security

- **Alignment**: Methods intended to make model behavior better match desired
  human, product, or policy objectives.
- **Red teaming**: Deliberate adversarial testing to discover vulnerabilities,
  unsafe behavior, or failure modes.
- **Guardrail**: A control that constrains, validates, filters, or requires
  approval for model inputs, outputs, or actions.
- **Prompt injection**: Untrusted content that attempts to alter model behavior
  or override intended instructions, especially in systems that process
  retrieved documents, webpages, email, or tool output.
- **Least privilege**: Giving an agent or tool only the permissions required for
  the current task.
