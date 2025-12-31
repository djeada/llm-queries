# Prompts Library

A curated collection of ready-to-use prompt templates organized by category. Each prompt includes examples, expected outputs, and tips for customization.

## Quick Reference

| Category | Prompts | Description |
|----------|---------|-------------|
| [Job Search](job_search/) | 2 | Resume optimization, interview prep |
| [Text Processing](text/) | 6 | Writing, formatting, editing |
| [Math](math/) | 1 | LaTeX cleanup |
| [Social Media](social_media/) | 1 | Captions and posts |

## Browse by Use Case

### 📝 Writing & Editing

| Prompt | What It Does | Best For |
|--------|--------------|----------|
| [improve_article.md](text/improve_article.md) | Expand and polish content | Blog posts, documentation |
| [format_lists.md](text/format_lists.md) | Convert prose to structured lists | Notes, summaries |
| [simplify_vocabulary.md](text/simplify_vocabulary.md) | Replace jargon with plain language | Technical writing |
| [llm_giveaway_phrases.md](text/llm_giveaway_phrases.md) | Remove AI-sounding phrases | Any LLM-generated content |
| [generate_notes.md](text/generate_notes.md) | Create organized notes | Study guides, documentation |

### 💼 Career & Job Search

| Prompt | What It Does | Best For |
|--------|--------------|----------|
| [resume.md](job_search/resume.md) | Tailor resume to job descriptions | Job applications |
| [interview_questions.md](job_search/interview_questions.md) | Generate Q&A for interview prep | Interview preparation |

### 📐 Technical & Math

| Prompt | What It Does | Best For |
|--------|--------------|----------|
| [sanitize_latex.md](math/sanitize_latex.md) | Clean up LaTeX formatting | Academic papers, equations |

### 📱 Social Media

| Prompt | What It Does | Best For |
|--------|--------------|----------|
| [instagram.md](social_media/instagram.md) | Create engaging captions | Instagram posts |

## How to Use These Prompts

### Step 1: Choose a Prompt

Find the prompt that matches your task. Each file includes:
- Description of what it does
- Expected output format
- The actual prompt text
- Before/after examples

### Step 2: Customize

Replace placeholders with your content:

```text
# Original prompt
"Review my resume for the following job description: [JOB DESCRIPTION]"

# Your customized prompt
"Review my resume for the following job description: 
Senior Software Engineer at Acme Corp..."
```

### Step 3: Iterate

Most tasks benefit from iteration:

1. Run the initial prompt
2. Review the output
3. Refine with follow-up prompts
4. Repeat until satisfied

## Prompt Quality Guidelines

Every prompt in this library should:

- ✅ Have clear, specific instructions
- ✅ Include expected output format
- ✅ Provide before/after examples
- ✅ Work across multiple LLMs (GPT-4, Claude, etc.)
- ✅ Avoid unnecessary jargon

## Model Compatibility

These prompts are designed to work with:

| Model | Tested | Notes |
|-------|--------|-------|
| GPT-4 / GPT-4o | ✅ | Primary testing platform |
| Claude 3 | ✅ | Works well with XML-structured prompts |
| Llama 3 | ✅ | May need slightly more explicit instructions |
| Gemini Pro | ✅ | Compatible with most prompts |

## Tips for Better Results

1. **Be specific** — Vague prompts get vague outputs
2. **Show examples** — Add your own before/after examples
3. **Constrain output** — Specify format, length, and style
4. **Chain prompts** — Use one output as input to another
5. **Iterate** — First drafts are rarely final

## Directory Structure

```
prompts/
├── README.md           # This file
├── job_search/         
│   ├── resume.md       # Resume optimization
│   └── interview_questions.md  # Interview prep
├── text/
│   ├── improve_article.md    # Content expansion
│   ├── format_lists.md       # List formatting
│   ├── format_lists_pl.md    # Polish language lists
│   ├── generate_notes.md     # Note generation
│   ├── simplify_vocabulary.md # Jargon removal
│   └── llm_giveaway_phrases.md # AI phrase detection
├── math/
│   └── sanitize_latex.md     # LaTeX cleanup
└── social_media/
    └── instagram.md          # Instagram captions
```

## Contributing New Prompts

We welcome contributions! When adding a prompt:

1. Use the standard template (see below)
2. Include working examples
3. Test with at least 2 different LLMs
4. Add entries to this README and INDEX.md

### Prompt Template

```markdown
# Prompt Name

Brief description of what this prompt does.

## Expected Output

- Output format specifications
- Length expectations
- Style notes

## Prompt

\`\`\`text
Your prompt text here...
\`\`\`

## Example

**Before:**
> Input example

**After:**
> Output example

## Notes

- Model compatibility
- Variations
- Tips for customization
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more details.
