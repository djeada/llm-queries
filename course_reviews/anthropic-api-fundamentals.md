# Anthropic API Fundamentals

A hands-on course covering the Claude API, from basic chat completions to advanced features like streaming and tool use.

## Course Link

<https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals>

## Key Topics Covered

### Getting Started

- **API Setup**: Obtaining API keys and configuring authentication
- **Basic Requests**: Making your first API call to Claude
- **Model Selection**: Choosing between Claude models (Opus, Sonnet, Haiku)

### Core API Features

- **Messages API**: The primary interface for Claude conversations
- **System Prompts**: Setting model behavior and persona
- **Temperature & Sampling**: Controlling output randomness

### Advanced Features

- **Streaming**: Receiving responses token-by-token for better UX
- **Tool Use (Function Calling)**: Enabling Claude to call external APIs
- **Vision**: Processing images alongside text
- **Long Context**: Working with Claude's extended context windows

### Production Considerations

- **Rate Limits**: Understanding and working within API limits
- **Error Handling**: Gracefully managing API errors
- **Cost Optimization**: Strategies for efficient API usage

## Key Takeaways

1. **Start with Haiku** for development, upgrade to Sonnet/Opus for production
2. **Use streaming** for any user-facing application
3. **Implement retries** with exponential backoff for reliability
4. **Monitor token usage** to control costs
5. **Cache responses** when appropriate to reduce API calls

## Code Examples

### Basic API Call

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Streaming Response

```python
with client.messages.stream(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Tool Use

```python
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    }
}]

message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)
```

## Who Should Take This

- Developers integrating Claude into applications
- Teams migrating from other LLM APIs
- Anyone wanting hands-on API experience

## Time Investment

- **Estimated completion**: 3-5 hours
- **Format**: Jupyter notebooks with exercises
- **Prerequisites**: Python programming basics

## Related Resources

- [Anthropic API Documentation](https://docs.anthropic.com/en/api)
- [Claude SDK on PyPI](https://pypi.org/project/anthropic/)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
