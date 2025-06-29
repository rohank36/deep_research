Multi agent systems work because they can use more tokens. More tokens used = more accuracy.

Performance variance factors:
- Token usage (80% of the variance)
- number of tool calls
- model choice 

multi agent systems are expensive. Only worth it to use for high value tasks. 

Orhcestrator-Worker pattern
- Lead agent coordinates the process while delegating to specialized sub agents that operate in parallel 

lead agent spawns subagents to explore different aspects simultaneously 
subagents act as intelligent filters by iteratively using search tools to gather information then return their findings to the lead agent

tool calling:
- tell the model what tools are available
- when the model wants to execute the tool, it tells you, you execute the tool and send the respones up
- tools
    - name
    - description to tell the model what the tool does, when to use it, when to not use it, what it returns etc
    - input schema that describes as a JSON schema, what inputs this tool expects and in which form
    - a function that executes the tool with the input the model sends to us and returns the result


Models

Good Models (Planning, orchestrating, tool selection, multi step reasoning)
- gpt-4o $2.50/$10 128k context
- gpt-4.1 $2/$8 1m context

Weak Models (Summarization, file parsing, classification, answering from known documents)
- gpt-4.1-nano $0.10/$0.40 1m context
- gpt-4o-mini $0.15/$0.60 128k context
- gpt-4.1-mini $0.4/$1.60 1m context

Good rule of thumb. 1 token ~= 0.75 words

