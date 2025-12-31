# Anthropic Prompt Engineering Course

A comprehensive course on crafting effective prompts for Claude and other LLMs, covering fundamentals through advanced techniques.

## Course Link

<https://github.com/anthropics/courses/blob/master/prompt_engineering_interactive_tutorial/README.md>

## Key Topics Covered

### Fundamentals

- **Clear Instructions**: Being specific about what you want the model to do
- **Role Assignment**: Using system prompts to establish Claude's persona and constraints
- **Output Formatting**: Specifying desired response structure (JSON, markdown, lists)

### Intermediate Techniques

- **Chain of Thought**: Encouraging step-by-step reasoning for complex problems
- **Few-Shot Examples**: Demonstrating desired behavior through examples in the prompt
- **XML Tags**: Using structured markup to organize complex prompts

### Advanced Patterns

- **Long Context Handling**: Strategies for working with large documents
- **Tool Use**: Enabling Claude to call external functions and APIs
- **Constitutional AI**: Understanding Anthropic's approach to AI safety

## Key Takeaways

1. **Be explicit**: Claude follows instructions literally—say exactly what you want
2. **Use structure**: XML tags and clear sections improve complex prompt handling
3. **Think step-by-step**: Adding "Let's think through this step by step" improves reasoning
4. **Iterate**: Start simple, test, then refine based on results
5. **Provide context**: More relevant context generally leads to better outputs

## Notable Examples from Course

### Basic Prompt Structure

```text
<instructions>
Your task is to analyze the customer feedback and categorize it.
</instructions>

<categories>
- Product Quality
- Customer Service
- Shipping
- Pricing
</categories>

<feedback>
{{USER_INPUT}}
</feedback>

Respond with only the category name, nothing else.
```

### Chain of Thought Pattern

```text
Please solve this problem step by step:
1. First, identify the key information
2. Then, determine the approach
3. Work through the solution
4. Verify your answer
5. Provide the final result
```

## Who Should Take This

- Developers building Claude-powered applications
- Anyone new to prompt engineering wanting structured learning
- Teams establishing prompt engineering best practices

## Time Investment

- **Estimated completion**: 2-4 hours
- **Format**: Interactive Jupyter notebooks
- **Prerequisites**: Basic programming knowledge helpful but not required

## Related Resources

- [Anthropic Documentation](https://docs.anthropic.com/)
- [Claude Prompt Library](https://docs.anthropic.com/en/prompt-library)
