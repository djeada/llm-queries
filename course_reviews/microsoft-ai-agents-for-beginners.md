# Microsoft AI Agents for Beginners

A beginner-friendly course introducing AI agent concepts and implementation using Microsoft's Azure and semantic kernel frameworks.

## Course Link

<https://github.com/microsoft/ai-agents-for-beginners>

## Key Topics Covered

### Agent Foundations

- **What are AI Agents**: Autonomous systems that perceive, reason, and act
- **Agent Types**: Simple reflex, goal-based, utility-based, learning agents
- **LLMs as Agent Brains**: Using language models for reasoning

### Core Concepts

- **Perception**: How agents gather information
- **Reasoning**: Decision-making with LLMs
- **Action**: Executing tasks and using tools
- **Memory**: Short-term and long-term agent memory

### Implementation

- **Semantic Kernel**: Microsoft's LLM orchestration framework
- **AutoGen**: Multi-agent conversation framework
- **Tool Integration**: Connecting agents to external services
- **Azure OpenAI**: Using Azure-hosted models

### Practical Projects

- **Conversational Agents**: Building chat-based assistants
- **Task Automation**: Agents that complete multi-step tasks
- **Research Agents**: Gathering and synthesizing information
- **Code Agents**: Agents that write and execute code

## Key Takeaways

1. **Agents are LLMs in a loop** — the key is the observe-reason-act cycle
2. **Start with single agents** before building multi-agent systems
3. **Tool descriptions are prompts** — write them carefully
4. **Memory enables context** — agents need state to handle complex tasks
5. **Safety is critical** — agents can take real actions, so add guardrails

## Code Examples (Semantic Kernel)

### Basic Agent Setup

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

kernel = sk.Kernel()
kernel.add_service(
    AzureChatCompletion(
        deployment_name="gpt-4",
        endpoint="https://your-endpoint.openai.azure.com",
        api_key="your-key"
    )
)
```

### Adding a Plugin (Tool)

```python
from semantic_kernel.functions import kernel_function

class WeatherPlugin:
    @kernel_function(description="Get weather for a city")
    def get_weather(self, city: str) -> str:
        return f"Weather in {city}: Sunny, 22°C"

kernel.add_plugin(WeatherPlugin(), "weather")
```

### Agent with Planning

```python
from semantic_kernel.planners import ActionPlanner

planner = ActionPlanner(kernel)

goal = "Find the weather in Paris and send an email about it"
plan = await planner.create_plan(goal)
result = await plan.invoke()
```

### AutoGen Multi-Agent

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"}
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding"}
)

user_proxy.initiate_chat(
    assistant,
    message="Write a Python function to calculate factorial"
)
```

## Who Should Take This

- Developers new to AI agents
- Teams using Azure and Microsoft ecosystem
- Anyone wanting structured agent learning path

## Time Investment

- **Estimated completion**: 8-12 hours
- **Format**: Markdown lessons with code examples
- **Prerequisites**: Basic Python, Azure account helpful

## Related Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Azure OpenAI Service](https://azure.microsoft.com/products/ai-services/openai-service)
