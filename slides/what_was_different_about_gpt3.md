# What Was Different About GPT-3?

> **Status:** historical · **Fact-checked:** 2026-09-27  
> Primary source: Brown et al., *Language Models are Few-Shot Learners* (2020):  
> https://arxiv.org/abs/2005.14165

GPT-3 mattered less because it introduced a radically new transformer and more
because it showed how far a mostly familiar autoregressive architecture could
be pushed through scale, data, and in-context evaluation.

This note describes the 2020 GPT-3 paper, not current OpenAI models.

## Scale

The largest GPT-3 model had:

| Property | GPT-3 175B |
| --- | ---: |
| Parameters | 175B |
| Transformer layers | 96 |
| Model width | 12,288 |
| Attention heads | 96 |
| Head dimension | 128 |
| Context window | 2,048 tokens |

The paper trained eight model sizes from 125M to 175B parameters so the authors
could examine how language-model loss and downstream task performance changed
with scale.

All of the reported GPT-3 models were trained for 300 billion tokens.

## Architecture: mostly GPT-2, not a new foundation

The GPT-3 paper explicitly says it used the same model and architecture as
GPT-2, including GPT-2's modified initialization, pre-normalization, and
reversible tokenization.

The important architectural exception was attention: GPT-3 alternated dense
attention with locally banded sparse-attention layers.

That distinction matters. GPT-3 should not be described as introducing a new
tokenizer family or a new positional-encoding scheme.

### Tokenization

GPT-3 reused GPT-2's reversible byte-level BPE tokenizer. The paper later notes
that reusing this English-oriented tokenizer may have hurt some non-English
translation directions.

An earlier version of this repository incorrectly claimed GPT-3 switched from
BPE to SentencePiece and used "adaptive tokenization." Those claims were removed
during the 2026-09-27 factual audit because they are not supported by the GPT-3
paper.

## Training data

The authors started from very large web corpora but did not simply train on raw
Common Crawl.

For Common Crawl they describe three important steps:

1. filter documents based on similarity to higher-quality reference corpora
2. perform fuzzy document-level deduplication
3. check benchmark overlap to reduce contamination

The final mixture also included an expanded WebText dataset, two internet-based
book corpora, and English-language Wikipedia.

The paper deliberately sampled higher-quality datasets more frequently than raw
dataset size alone would imply.

## The important behavioral shift: in-context learning

GPT-3's headline evaluation setup was not task-specific fine-tuning.

The paper compared three inference-time settings:

- **zero-shot** — natural-language task description, no demonstrations
- **one-shot** — one demonstration in context
- **few-shot** — several demonstrations in context

No gradient update occurs in these settings. The demonstrations are simply part
of the model's input context.

This made a useful practical point: a sufficiently large pretrained language
model could often adapt its behavior from text instructions and examples alone,
without creating a new fine-tuned model for every task.

## What scaling improved

The paper reports that increasing model size generally improved zero-, one-, and
few-shot performance across a wide range of language tasks.

Notable examples included:

- question answering
- translation
- cloze / completion tasks
- word unscrambling
- novel-word use
- some arithmetic tasks
- synthetic and natural-language reasoning-style tasks

Few-shot performance was often strongest, but GPT-3 was not uniformly
state-of-the-art and some tasks remained weak.

## What the paper did *not* prove

GPT-3's results should not be summarized as "scale automatically creates general
reasoning."

The authors document important limitations:

- performance still varied greatly by task
- some tasks remained far behind fine-tuned systems
- the 2,048-token context window constrained long inputs
- generated text could lose coherence or repeat itself over longer passages
- benchmark contamination was a serious methodological concern
- large-scale pretraining carried substantial compute cost
- model behavior could reproduce harmful social biases

The paper devotes an entire section to benchmark memorization and contamination
because large web-scale training corpora make clean evaluation difficult.

## Why GPT-3 was historically important

GPT-3 provided strong evidence for three ideas that shaped later LLM work:

1. **Scaling could materially improve task-agnostic behavior.**
2. **Natural-language instructions and demonstrations could act as an
   inference-time interface.**
3. **Evaluation methodology becomes harder as training corpora grow**, because
   benchmark overlap and memorization are increasingly plausible.

Later work built on these ideas with instruction tuning, human-feedback
training, retrieval, tool use, longer contexts, and more deliberate evaluation.

## Source notes

The core architecture, model-size, tokenizer, context-window, and training-token
claims above come from Sections 2.1–2.3 of the original GPT-3 paper.

Useful primary sources:

- OpenAI publication page: https://openai.com/index/language-models-are-few-shot-learners/
- Paper: https://arxiv.org/abs/2005.14165
- GPT-2 paper, for the inherited tokenizer/architecture details:
  https://cdn.openai.com/better-language-models/language-models.pdf
