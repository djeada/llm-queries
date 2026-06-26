# llm-queries

[![License](https://img.shields.io/github/license/djeada/llm-queries?color=2a9d8f)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/djeada/llm-queries)](https://github.com/djeada/llm-queries/graphs/contributors)
[![Stars](https://img.shields.io/github/stars/djeada/llm-queries)](https://github.com/djeada/llm-queries/stargazers)
[![Issues](https://img.shields.io/github/issues/djeada/llm-queries)](https://github.com/djeada/llm-queries/issues)

> A comprehensive collection of practical prompts, local LLM setup guides, and curated references for building, using, and evaluating language-model workflows.

## Why This Repository?

Working with LLMs effectively requires more than just access to a model—it requires well-crafted prompts, understanding of model behavior, and practical knowledge of deployment options. This repository provides:

- **Battle-tested prompts** for common tasks like writing, job searching, and content creation
- **Local deployment guides** for running models on your own hardware
- **Curated learning resources** from leading AI labs and practitioners
- **Slide decks** for teaching and learning core LLM concepts

## Table of Contents

- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [Featured Content](#featured-content)
- [Use Cases](#use-cases)
- [Example Prompt in Action](#example-prompt-in-action)
- [Best Practices](#best-practices)
- [Related Resources](#related-resources)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

Choose your path based on what you want to accomplish:

| Goal | Start Here | Skill Level |
|------|------------|-------------|
| ✍️ Improve your writing | [`prompts/text/improve_article.md`](prompts/text/improve_article.md) | Beginner |
| 📝 Optimize your resume | [`prompts/job_search/resume.md`](prompts/job_search/resume.md) | Beginner |
| 🎯 Debug LLM workflows | [`skills/README.md`](skills/README.md) | Intermediate |
| 🖥️ Run models locally | [`local_setup_guides/local_models_intro.md`](local_setup_guides/local_models_intro.md) | Intermediate |
| 🔍 Learn about RAG | [`slides/rag_with_vector_database.md`](slides/rag_with_vector_database.md) | Intermediate |
| 🤖 Build AI agents | [`resources/practical_guide_to_building_agents.md`](resources/practical_guide_to_building_agents.md) | Advanced |

## Repository Structure

```
llm-queries/
├── prompts/                  # 📝 Ready-to-use prompt templates
│   ├── job_search/           #    Resume, interview prep
│   ├── text/                 #    Writing, formatting, editing
│   ├── math/                 #    LaTeX cleanup, equations
│   └── social_media/         #    Captions, engagement posts
├── skills/                   # 🎯 Practical LLM workflow skills
│   ├── prompt_debugging.md
│   ├── context_engineering.md
│   ├── llm_evaluation.md
│   ├── rag_quality_audit.md
│   ├── agent_tool_design.md
│   └── local_model_selection.md
├── local_setup_guides/       # 🖥️ Run LLMs on your machine
│   ├── local_models_intro.md #    Getting started with Ollama
│   └── deepseek_r1.md        #    DeepSeek R1 setup
├── resources/                # 📚 External guides and references
│   ├── gpt_4_1_prompting_guide.md
│   ├── guide_for_coding_ai_agents.md
│   └── ...                   
├── course_reviews/           # 🎓 Course notes and summaries
│   ├── anthropic-prompt-engineering.md
│   ├── hugging-face-llm-intro.md
│   └── ...
├── slides/                   # 📊 Teaching materials
│   ├── what_are_llms.md      #    LLM fundamentals
│   ├── transformer_architecture.md
│   └── ...
├── GLOSSARY.md               # 📖 Terminology definitions
├── INDEX.md                  # 🗂️ Complete file listing
└── CONTRIBUTING.md           # 🤝 How to contribute
```

## Featured Content

### Prompts Library

| Category | Description | Key Files |
|----------|-------------|-----------|
| **Text Processing** | Improve, format, and simplify written content | `improve_article.md`, `format_lists.md`, `simplify_vocabulary.md` |
| **Job Search** | Resume optimization and interview preparation | `resume.md`, `interview_questions.md` |
| **Skills** | Debug prompts, design context, evaluate outputs, audit RAG, and design agent tools | `prompt_debugging.md`, `context_engineering.md`, `llm_evaluation.md` |
| **Math/LaTeX** | Clean up mathematical notation | `sanitize_latex.md` |
| **Social Media** | Engaging captions and posts | `instagram.md` |

### Learning Paths

**For Beginners:**
1. Start with [`slides/what_are_llms.md`](slides/what_are_llms.md) to understand fundamentals
2. Learn prompting basics in [`slides/intro_to_prompts.md`](slides/intro_to_prompts.md)
3. Try the text prompts in [`prompts/text/`](prompts/text/)

**For Practitioners:**
1. Review [`resources/gpt_4_1_prompting_guide.md`](resources/gpt_4_1_prompting_guide.md)
2. Set up local models with [`local_setup_guides/local_models_intro.md`](local_setup_guides/local_models_intro.md)
3. Explore agent patterns in [`resources/practical_guide_to_building_agents.md`](resources/practical_guide_to_building_agents.md)

## Use Cases

### Writing & Content

```
prompts/text/improve_article.md  → Expand and polish draft content
prompts/text/format_lists.md     → Convert prose to structured lists
prompts/text/simplify_vocabulary.md → Remove jargon and buzzwords
```

### Career Development

```
prompts/job_search/resume.md     → Tailor resume to job descriptions
prompts/job_search/interview_questions.md → Generate practice Q&A
```

### Local Deployment

```
local_setup_guides/local_models_intro.md → Ollama setup and model selection
local_setup_guides/deepseek_r1.md        → Run DeepSeek reasoning models
```

### Learning & Teaching

```
slides/what_are_llms.md          → Core LLM concepts with math
slides/transformer_architecture.md → Attention and transformers
slides/rag_with_vector_database.md → RAG implementation patterns
```

## Example Prompt in Action

**Prompt** (from [`prompts/text/improve_article.md`](prompts/text/improve_article.md)):

```text
Revise the following text by:
1. Expanding each paragraph with concrete examples or explanations.
2. Correcting any factual or grammatical errors.
3. Enhancing clarity with straightforward language.
```

**Input:**

```text
Caching improves web performance.
```

**Output:**

```text
Caching speeds up a website by storing frequently used data so the server 
does not have to rebuild the same response each time. The result is faster 
page loads for users and less work for your backend during traffic spikes.
```

## Best Practices

When using prompts from this repository:

1. **Test with your target model** — Prompts may perform differently across GPT-4, Claude, Llama, etc.
2. **Iterate and refine** — Start with the base prompt, then customize for your specific use case
3. **Check the "Expected output" section** — Most prompt files describe what good output looks like
4. **Combine prompts** — Chain multiple prompts for complex workflows
5. **Document your variations** — Keep notes on what works for your specific needs

## Related Resources

### Internal Navigation

- **[`INDEX.md`](INDEX.md)** — Complete listing of all files with descriptions
- **[`GLOSSARY.md`](GLOSSARY.md)** — Terminology and definitions
- **[`CONTRIBUTING.md`](CONTRIBUTING.md)** — Guidelines for contributors

### External Links

- [OpenAI Cookbook](https://cookbook.openai.com/) — Official OpenAI examples and guides
- [Anthropic Prompt Library](https://docs.anthropic.com/en/prompt-library/library) — Claude prompt patterns
- [Hugging Face Courses](https://huggingface.co/learn) — Free ML and NLP courses

## Contributing

We welcome contributions! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

**Quick contribution ideas:**
- Add new prompt templates with examples
- Expand course review summaries
- Improve documentation and fix typos
- Add model compatibility notes to existing prompts

## License

This project is licensed under the terms in [`LICENSE`](LICENSE).
