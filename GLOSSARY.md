# Glossary

Definitions for common terms used across the repository, organized by category for easy reference.

## Core Concepts

- **LLM (Large Language Model)**: A neural network with billions of parameters trained to predict and generate text. Examples include GPT-4, Claude, and Llama.
- **Token**: The smallest unit of text a model processes—typically a word, subword, or character. Most models use subword tokenization (e.g., BPE, SentencePiece).
- **Prompt**: The input text provided to guide a model's output. Effective prompts are clear, specific, and structured.
- **Context window**: The maximum number of tokens a model can process in a single request. Ranges from 4K to 1M+ tokens depending on the model.
- **Inference**: The process of running a trained model to generate predictions or outputs from new inputs.

## Model Training & Adaptation

- **Pre-training**: Initial training phase where models learn language patterns from large text corpora using self-supervised learning.
- **Fine-tuning**: Training a pre-trained model on task-specific data to specialize its behavior for particular use cases.
- **RLHF (Reinforcement Learning from Human Feedback)**: A training technique that uses human preferences to align model outputs with desired behaviors.
- **LoRA (Low-Rank Adaptation)**: A parameter-efficient fine-tuning method that trains small adapter layers instead of all model weights.
- **Checkpoint**: A saved snapshot of model weights during or after training, used for inference or continued training.

## Prompt Engineering

- **Zero-shot prompting**: Asking a model to perform a task without providing examples in the prompt.
- **Few-shot prompting**: Including a small number of examples in the prompt to demonstrate the desired output format or behavior.
- **Chain-of-thought (CoT)**: A prompting technique that encourages models to show reasoning steps before providing a final answer.
- **System prompt**: Instructions that set the model's role, behavior, and constraints—typically processed before user messages.
- **Prompt template**: A reusable prompt structure with placeholders for variable content.

## Generation Parameters

- **Temperature**: A sampling parameter (typically 0–2) controlling output randomness. Lower values produce more focused, deterministic outputs; higher values increase creativity and variability.
- **Top-p (nucleus sampling)**: Limits token selection to the smallest set whose cumulative probability exceeds p. Typical values: 0.9–0.95.
- **Top-k**: Limits token selection to the k most probable next tokens. Often combined with temperature or top-p.
- **Max tokens**: The maximum number of tokens the model will generate in its response.
- **Stop sequences**: Strings that signal the model to stop generating further output.

## Performance & Efficiency

- **Latency**: The time elapsed between sending a request and receiving the first token or complete response.
- **Throughput**: The number of tokens generated per unit of time, often measured in tokens per second.
- **Quantization**: Reducing the numerical precision of model weights (e.g., from 32-bit to 4-bit) to decrease memory usage and increase inference speed.
- **Batching**: Processing multiple requests simultaneously to improve GPU utilization and throughput.
- **Streaming**: Returning tokens incrementally as they're generated rather than waiting for the complete response.

## Retrieval & Augmentation

- **RAG (Retrieval-Augmented Generation)**: A technique that retrieves relevant documents and includes them in the prompt context to ground model responses in external knowledge.
- **Embedding**: A dense vector representation of text that captures semantic meaning, enabling similarity comparisons.
- **Vector database**: A database optimized for storing and searching high-dimensional vectors using similarity metrics like cosine distance.
- **Chunking**: Splitting documents into smaller segments for embedding and retrieval, typically 256–1024 tokens each.
- **Semantic search**: Finding documents based on meaning similarity rather than keyword matching.

## Agent & Tool Use

- **Agent**: An LLM-powered system that can take actions, use tools, and pursue goals across multiple steps.
- **Tool calling (function calling)**: The ability for models to generate structured requests to invoke external tools or APIs.
- **ReAct**: A prompting pattern combining reasoning and acting, where the model alternates between thinking and taking actions.
- **Multi-agent system**: An architecture where multiple specialized agents collaborate to complete complex tasks.

## Evaluation & Safety

- **Hallucination**: When a model generates plausible-sounding but factually incorrect or unsupported information.
- **Grounding**: Techniques to anchor model outputs in verified information sources to reduce hallucinations.
- **Alignment**: The process of training models to behave in accordance with human values and intentions.
- **Red teaming**: Adversarial testing to identify model vulnerabilities, biases, or harmful outputs.
- **Guardrails**: Safety mechanisms that filter, validate, or constrain model inputs and outputs.
