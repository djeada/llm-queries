# Contributing to llm-queries

Thank you for your interest in improving this repository! This guide will help you make effective contributions that align with the project's goals.

## Our Vision

This repository aims to be a practical, well-organized resource for anyone working with LLMs—from beginners exploring prompt engineering to practitioners deploying production systems. We prioritize:

- **Clarity** over comprehensiveness
- **Practical examples** over abstract theory
- **Tested prompts** over untested ideas
- **Good organization** over rapid growth

## Ways to Contribute

### 🔧 Quick Fixes

- Fix typos, broken links, or formatting issues
- Correct factual errors with citations
- Improve unclear explanations

### 📝 Content Additions

- Add new prompt templates with working examples
- Write or expand course review summaries
- Create local setup guides for new tools or models
- Add entries to the glossary

### 🏗️ Structural Improvements

- Improve navigation and cross-linking
- Standardize file formats and structure
- Enhance README files in each directory

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/llm-queries.git
cd llm-queries
git checkout -b your-feature-name
```

### 2. Find Something to Work On

- Check [open issues](https://github.com/djeada/llm-queries/issues) for ideas
- Look for files with "Status: pending" markers
- Review the `todo.md` files in each directory

### 3. Make Your Changes

Follow the content standards below, then commit:

```bash
git add .
git commit -m "Add: descriptive commit message"
git push origin your-feature-name
```

### 4. Open a Pull Request

Include:
- What you changed and why
- Any testing you performed (e.g., which models you tested prompts with)
- Screenshots if relevant (especially for formatting changes)

## Repository Structure

```
llm-queries/
├── prompts/                 # Prompt templates organized by category
│   ├── job_search/          # Career-related prompts
│   ├── text/                # Writing and formatting prompts
│   ├── math/                # Mathematical notation prompts
│   └── social_media/        # Social content prompts
├── skills/                  # Practical LLM workflow skill prompts
├── local_setup_guides/      # Self-hosted LLM tutorials
├── resources/               # External reference summaries
├── course_reviews/          # Course notes and reviews
├── slides/                  # Teaching and presentation content
├── INDEX.md                 # Complete file listing
├── GLOSSARY.md              # Terminology definitions
└── CHANGELOG.md             # Version history
```

## Content Standards

### File Naming

- Use **kebab-case** for all file names: `my-new-prompt.md`
- Keep names **descriptive but concise**: `improve-article.md` not `a-prompt-for-improving-articles-and-making-them-better.md`
- Use **ASCII characters only**: no accents, special characters, or spaces

### Markdown Structure

Every content file should follow this structure:

```markdown
# Title

Brief description of what this file contains and who it's for.

## Expected Output (for prompts)

- What the user should expect to receive
- Format specifications
- Any constraints

## Main Content

The actual content, organized with clear headings.

## Examples (when applicable)

Before/after examples or usage demonstrations.
```

### Heading Hierarchy

- `#` — Document title (one per file)
- `##` — Major sections
- `###` — Subsections
- `####` — Rarely needed; consider restructuring if you need this level

### Prompt Files

Each prompt file should include:

1. **Title** — Clear, action-oriented name
2. **Description** — What the prompt does and when to use it
3. **Expected Output** — What format and content to expect
4. **The Prompt** — In a code block with `text` language tag
5. **Example** — Before/after demonstration
6. **Notes** — Model compatibility, limitations, variations

Example structure:

```markdown
# Improve Article

Revise and expand draft content with concrete examples and clearer language.

## Expected Output

- Expanded paragraphs with examples
- Corrected errors
- Clearer, more direct prose

## Prompt

\`\`\`text
Revise the following text by:
1. Expanding each paragraph with concrete examples.
2. Correcting any errors.
3. Enhancing clarity.
\`\`\`

## Example

**Before:**
> Caching improves performance.

**After:**
> Caching speeds up websites by storing frequently used data...

## Notes

- Tested with: GPT-4, Claude 3
- Works best with technical content
```

### Citations and Sources

- Link to sources for factual claims
- Cite benchmark results with links to papers or reports
- When summarizing external content, link to the original

### Writing Style

- **Be direct** — Avoid filler words and unnecessary hedging
- **Be specific** — Concrete examples over abstract descriptions
- **Be practical** — Focus on "how to use" over "how it works" (unless in slides/)
- **Be inclusive** — Write for readers with varying experience levels

## Quality Checklist

Before submitting, verify:

- [ ] File name follows kebab-case convention
- [ ] Document has a clear `#` title
- [ ] Prompts include expected output and examples
- [ ] Links are valid and point to the right places
- [ ] No trailing whitespace or inconsistent formatting
- [ ] Content is original or properly attributed
- [ ] Changes are tested where applicable

## Review Process

1. Maintainers will review your PR within a few days
2. Feedback may be requested before merging
3. Once approved, your contribution will be merged and attributed

## Questions?

- Open an issue for discussion before starting large changes
- Tag maintainers if you need guidance on approach
- Check existing issues and PRs for similar work

## Recognition

Contributors are listed in the repository's contributor graph. Significant contributions may be called out in the CHANGELOG.

---

Thank you for helping make llm-queries better! 🙏
