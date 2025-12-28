# Contributing to llm-queries

Thank you for your interest in contributing to llm-queries! This document provides guidelines and instructions for contributing to this repository.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Style Guidelines](#style-guidelines)
- [Pull Request Process](#pull-request-process)
- [Content Guidelines](#content-guidelines)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute?

### Reporting Issues

- Use the GitHub issue tracker to report bugs, suggest features, or request improvements
- Before creating an issue, please check if a similar issue already exists
- Provide clear and detailed information about your suggestion or problem

### Suggesting Enhancements

We welcome suggestions for:
- New prompts and prompt categories
- Additional LLM setup guides
- Course reviews and educational resources
- Improvements to existing documentation
- New slides or educational content

### Contributing Content

You can contribute by:
1. **Adding new prompts** - Share effective prompts for various use cases
2. **Writing guides** - Create setup guides for different LLM frameworks or platforms
3. **Reviewing courses** - Add reviews and summaries of LLM-related courses
4. **Creating slides** - Develop educational slide content about LLMs and AI
5. **Improving documentation** - Fix typos, clarify instructions, add examples

## Style Guidelines

### Markdown Formatting

- Use consistent heading hierarchy:
  - `#` for document title
  - `##` for main sections
  - `###` for subsections
- Add blank lines before and after headings
- Use fenced code blocks with language identifiers:
  ````markdown
  ```python
  # Your code here
  ```
  ````
- Use consistent list formatting (prefer `-` for unordered lists)
- Keep lines reasonably short (recommended max 120 characters)

### File Naming

- Use lowercase with hyphens (kebab-case): `my-new-guide.md`
- Use descriptive, clear names that indicate content
- Avoid special characters, spaces, or underscores in filenames

### Content Structure

Each document should include:
- **Clear title** - Descriptive and concise
- **Introduction** - Brief overview of the document's purpose
- **Table of contents** (for longer documents)
- **Main content** - Well-organized with appropriate headings
- **Examples** - Practical examples where applicable
- **References** - Links to sources and related resources

### Prompts

When adding prompts:
- Include a clear description of the prompt's purpose
- Provide example usage or expected outputs
- Note any specific LLM versions or models tested with
- Organize prompts into appropriate categories

### Setup Guides

Setup guides should include:
- Clear prerequisites and system requirements
- Step-by-step instructions
- Code blocks for commands (with proper syntax highlighting)
- Troubleshooting section for common issues
- Verification steps to confirm successful setup

## Pull Request Process

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/my-contribution
   ```

2. **Make your changes** following the style guidelines

3. **Test your changes**:
   - Verify all markdown renders correctly
   - Check that all links work
   - Ensure code examples are correct

4. **Commit your changes** with clear commit messages:
   ```bash
   git commit -m "Add guide for setting up Ollama on macOS"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/my-contribution
   ```

6. **Open a Pull Request**:
   - Provide a clear description of your changes
   - Reference any related issues
   - Explain the motivation for your changes
   - Include examples or screenshots if applicable

7. **Respond to feedback**:
   - Be open to suggestions and constructive criticism
   - Make requested changes promptly
   - Ask questions if something is unclear

### Pull Request Review Criteria

Your PR will be reviewed based on:
- **Relevance** - Does it align with the repository's purpose?
- **Quality** - Is the content accurate, well-written, and useful?
- **Formatting** - Does it follow the style guidelines?
- **Completeness** - Is the content thorough and well-documented?
- **Originality** - Is the content original or properly attributed?

## Content Guidelines

### Educational Content

- Ensure technical accuracy
- Cite sources and provide references
- Use clear, accessible language
- Include practical examples
- Consider your target audience

### Prompts

- Test prompts before submitting
- Provide context for when and how to use the prompt
- Avoid prompts that could be harmful or unethical
- Include variations or customization suggestions

### Attribution

- Always credit original sources
- Include links to referenced materials
- Respect copyright and licensing
- Don't plagiarize content

### Quality Standards

Content should be:
- **Accurate** - Factually correct and up-to-date
- **Clear** - Easy to understand and follow
- **Useful** - Provides value to users
- **Complete** - Sufficiently detailed
- **Well-formatted** - Following markdown and style guidelines

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Ask in your pull request
- Review existing issues and PRs for examples

Thank you for contributing to llm-queries! 🎉
