# Prompts Library

Ready-to-use prompts organized by category, with a bias toward concise, reusable templates.

## Categories

- **Job search**: resume and interview prompts in `prompts/job_search/`
- **Text**: rewriting, formatting, and summarization in `prompts/text/`
- **Math**: cleanup utilities in `prompts/math/`
- **Social media**: short-form publishing prompts in `prompts/social_media/`

## Quick picks

- Tighten prose: `prompts/text/improve_article.md`
- Clean lists: `prompts/text/format_lists.md`
- Simplify language: `prompts/text/simplify_vocabulary.md`
- Resume editing: `prompts/job_search/resume.md`
- Interview prep: `prompts/job_search/interview_questions.md`

## How to use

1. Open a prompt file and paste it into your model interface.
2. Replace bracketed fields or placeholders with your context.
3. Iterate by adjusting constraints and examples.

## Expected outputs

- Prompt files include an "Expected output" section describing the output shape
- If a file lacks it, treat the example output as the target format

## Contributing new prompts

- Keep prompts short and specific
- Add example inputs and expected output shape when possible
- Note any model assumptions (token limits, system prompt usage)
