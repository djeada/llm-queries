# Hugging Face Agents Course

A practical course on building AI agents using the Hugging Face ecosystem, covering tool use, planning, and multi-agent systems.

## Course Link

<https://huggingface.co/learn/agents-course/unit0/introduction>

## Key Topics Covered

### Agent Fundamentals

- **What are Agents**: LLMs that can take actions and use tools
- **ReAct Pattern**: Reasoning and Acting in alternating steps
- **Tool Calling**: Enabling models to invoke external functions

### Building Agents

- **Tool Definition**: Creating tools agents can use
- **Agent Loops**: Implementing the observe-think-act cycle
- **Memory**: Giving agents context across interactions

### Advanced Patterns

- **Planning**: Breaking complex tasks into subtasks
- **Multi-Agent Systems**: Multiple agents collaborating
- **Agent Evaluation**: Measuring agent performance

### Hugging Face Tools

- **Transformers Agents**: Built-in agent framework
- **smolagents**: Lightweight agent library
- **Hub Integration**: Using and sharing agent components

## Key Takeaways

1. **Agents = LLM + Tools + Loop** — Start with this mental model
2. **Tool descriptions matter** — Clear descriptions help the agent choose correctly
3. **Start simple** — Single agent with few tools before complex setups
4. **Observe failures** — Agent mistakes reveal prompt and tool design issues
5. **Limit iterations** — Set maximum steps to prevent runaway agents

## Code Examples

### Simple Agent with Tools

```python
from smolagents import CodeAgent, HfApiModel, tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # Implementation here
    return f"The weather in {city} is sunny, 22°C"

agent = CodeAgent(
    tools=[get_weather],
    model=HfApiModel()
)

result = agent.run("What's the weather like in Paris?")
```

### ReAct-Style Agent

```python
from transformers import ReactAgent

agent = ReactAgent(
    model="meta-llama/Llama-2-70b-chat-hf",
    tools=["web_search", "calculator"],
    max_iterations=5
)

response = agent.chat("How many days until the next solar eclipse?")
```

### Multi-Agent Setup

```python
from smolagents import CodeAgent, ManagedAgent

# Specialist agents
web_agent = CodeAgent(tools=[web_search], model=model)
code_agent = CodeAgent(tools=[python_interpreter], model=model)

# Manager coordinates specialists
managed_web = ManagedAgent(agent=web_agent, name="web_researcher")
managed_code = ManagedAgent(agent=code_agent, name="programmer")

manager = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_web, managed_code]
)
```

## Who Should Take This

- Developers building agentic AI applications
- Teams implementing tool-use in their products
- Anyone curious about AI agents beyond simple chat

## Time Investment

- **Estimated completion**: 6-10 hours
- **Format**: Interactive tutorials with hands-on exercises
- **Prerequisites**: Python, basic LLM familiarity

## Related Resources

- [smolagents Documentation](https://huggingface.co/docs/smolagents)
- [Transformers Agents Guide](https://huggingface.co/docs/transformers/agents)
- [Agent Examples on Hub](https://huggingface.co/spaces?filter=agents)
