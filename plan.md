Multi agent systems work because they can use more tokens. More tokens used = more accuracy.

Performance variance factors:
- Token usage (80% of the variance)
- number of tool calls
- model choice 

multi agent systems are expensive. Only worth it to use for high value tasks. 

Domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi agent systems today.

Multi agent systems excel at valuable tasks that involve heavy parallelization, information that exceeds single context windows and interfacing with numerous complex tools. 

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

General Idea for Agent:
- main.py
    - Functions:
        - main
        - NewAgent factory methods, returns Agent type

- Agent.py
    - Functions:
        - run
            - heartbeat of the program. User input -> add to conversation -> llm call -> add llm respones to conversation -> User input ...
        - llm_call
        - execute_tool


- ToolDefinition.py
    - @dataclass 


Models

Good Models (Planning, orchestrating, tool selection, multi step reasoning)
- gpt-4o $2.50/$10 
- gpt-4.1 $2/$8

Weak Models (Summarization, file parsing, classification, answering from known documents)
- gpt-4.1-nano $0.10/$0.40
- gpt-4o-mini $0.15/$0.60
- gpt-4.1-mini $0.4/$1.60