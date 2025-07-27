# Multi Agent System for Deep Research

<i>"What I cannot build. I do not understand." - Richard Feynman</i>

Inspired by: https://www.anthropic.com/engineering/built-multi-agent-research-system.

My writing: https://rohankanti.substack.com/p/ai-agent-system-from-scratch

The system follows a orchestrator-worker design.

Note that this system isn't production ready. I implemented it to better understand agentic systems.

To make production ready:
- the search() and fetch_content() tools would need to be improved
- a citations agent would need to be implemented
- ui/ux would need to be improved, it's in dev mode right now
- rigorious system evals would need to be implemented

.env setup
```
OPENAI_API_KEY=
```

To run
```
>>> git clone repo 
# activate venv
>>> pip install -r requirements.txt
# change query in system.py
>>> python main.py
```

Key files/dirs
- prompts # dir that stores the system prompts
- agent.py # agent code
- tools.py # tool code

