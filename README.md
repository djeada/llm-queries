# llm-queries

[![License](https://img.shields.io/github/license/djeada/llm-queries?color=2a9d8f)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/djeada/llm-queries)](https://github.com/djeada/llm-queries/graphs/contributors)
[![Stars](https://img.shields.io/github/stars/djeada/llm-queries)](https://github.com/djeada/llm-queries/stargazers)
[![Issues](https://img.shields.io/github/issues/djeada/llm-queries)](https://github.com/djeada/llm-queries/issues)

Practical prompts, local LLM setup guides, and curated references for building, using, and evaluating language-model workflows.

## Table of contents

- [Quick start](#quick-start)
- [Repository map](#repository-map)
- [Use cases](#use-cases)
- [How to use this repo](#how-to-use-this-repo)
- [Contributing](#contributing)
- [License](#license)

## Quick start

1. Pick a goal:
   - write or refine prompts in `prompts/`
   - run models locally in `local_setup_guides/`
   - study background material in `resources/`
2. Open the relevant README in that folder.
3. Start with the shortest file in that section and iterate.

## Repository map

```
llm-queries/
├─ prompts/                Prompt templates by category
├─ local_setup_guides/     Local LLM setup and optimization
├─ resources/              External references and deep dives
├─ course_reviews/         Course notes and summaries
└─ slides/                 Slide decks and teaching notes
```

## Use cases

- **Prompt building**: start with `prompts/README.md` and try `prompts/text/improve_article.md`
- **Job search prompts**: see `prompts/job_search/resume.md` and `prompts/job_search/interview_questions.md`
- **Local LLM setup**: begin with `local_setup_guides/local_models_intro.md`
- **Course overviews**: scan `course_reviews/anthropic-prompt-engineering.md`
- **Framework comparisons**: check `slides/rag_with_vector_database.md`

## Example prompt in action

**Prompt (excerpt)** from `prompts/text/improve_article.md`:

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
Caching speeds up a website by storing frequently used data so the server does not have to rebuild the same response each time. The result is faster page loads for users and less work for your backend during traffic spikes.
```

## How to use this repo

- Prefer small, single-purpose prompts and keep variants next to each other
- Add citations for benchmarks, model claims, or factual statements
- Note model/version assumptions when testing prompts
- Use `INDEX.md` to browse everything and `GLOSSARY.md` for shared terminology

## Related projects and resources

- `resources/README.md` curated external readings and guides
- `course_reviews/README.md` links to courses with notes
- `slides/` teaching notes and slide-style overviews

## Contributing

See `CONTRIBUTING.md`.

## License

See `LICENSE`.
