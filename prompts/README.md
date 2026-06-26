# Prompts Library

A practical library of reusable prompt templates for writing, editing, job search, technical cleanup, and social media work. The prompts are designed to be copied, customized, and iterated with most modern LLMs.

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

### 🎯 Skills & Learning

| Prompt | What It Does | Best For |
|--------|--------------|----------|
| [prompt_debugging.md](../skills/prompt_debugging.md) | Diagnose and rewrite failing prompts | Prompt iteration |
| [context_engineering.md](../skills/context_engineering.md) | Structure, compress, retrieve, or omit context | Long-context tasks |
| [llm_evaluation.md](../skills/llm_evaluation.md) | Build rubrics, test cases, and regression checks | Prompt and model evaluation |
| [rag_quality_audit.md](../skills/rag_quality_audit.md) | Audit retrieval, grounding, and citations | RAG systems |
| [agent_tool_design.md](../skills/agent_tool_design.md) | Design tool schemas, guardrails, and failure handling | Agent workflows |
| [local_model_selection.md](../skills/local_model_selection.md) | Choose local, API, or hybrid model setups | Deployment decisions |

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

Find the prompt that matches your task. Each prompt file should explain:

- When to use the prompt
- What input to provide
- What output to expect
- The copy/paste prompt text
- Examples, review checks, or follow-up prompts

### Step 2: Customize

Replace bracketed placeholders with your content:

```text
# Original prompt
"Review my resume for the following job description: [JOB DESCRIPTION]"

# Your customized prompt
"Review my resume for the following job description: 
Senior Software Engineer at Acme Corp..."
```

### Step 3: Add Context

Better context usually produces better output. When relevant, include:

- Audience, channel, or reader skill level
- Tone and style requirements
- Length limits
- Examples of acceptable and unacceptable output
- Source material the model must preserve
- Constraints such as "do not invent facts" or "return only the revised text"

### Step 4: Iterate

Most tasks benefit from iteration:

1. Run the initial prompt
2. Review the output
3. Refine with follow-up prompts
4. Repeat until satisfied

## Prompt Quality Guidelines

Every prompt in this library should:

- State the role or task clearly
- Define the input the user must provide
- Specify output format, length, and tone
- Preserve factual accuracy and avoid unsupported claims
- Include examples, checks, or follow-up prompts where useful
- Work across multiple LLMs without relying on vendor-specific features
- Avoid unnecessary jargon and vague style instructions

## Model Compatibility

These prompts are designed to work with:

| Model | Tested | Notes |
|-------|--------|-------|
| GPT-4 / GPT-4o / GPT-4.1 | Compatible | Strong general performance |
| Claude 3 / Claude 3.5 | Compatible | Works well with structured prompts |
| Llama 3 / Llama 3.1 | Compatible | May need more explicit examples |
| Gemini | Compatible | Works best with clear output constraints |

## Tips for Better Results

1. **Be specific** - vague prompts produce vague outputs.
2. **Show examples** - add before/after samples when style matters.
3. **Constrain output** - specify format, length, tone, and exclusions.
4. **Protect facts** - tell the model to flag uncertainty instead of guessing.
5. **Chain prompts** - use one output as input to a review or refinement prompt.
6. **Iterate** - first drafts usually need at least one focused pass.

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

Brief description of what this prompt does and when to use it.

## Best for

- Use case 1
- Use case 2

## Required input

- Source text, topic, job description, or other required material
- Optional style, audience, length, or formatting constraints

## Expected Output

- Output format specifications
- Length expectations
- Style notes
- Accuracy and citation requirements, if relevant

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
- Follow-up prompts or review checklist
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more details.
