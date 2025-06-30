from jinja2 import Template
from datetime import date
from agent import Agent
from typing import List

def format(agent:Agent):
    available_tools:List[str] = agent.tools_available
    available_tools_formatted = "\n".join(f"    {tool}" for tool in available_tools)
    general_instructions_template = get_template("prompts/general_instructions.md")
    general_instructions = general_instructions_template.render(tools_available=available_tools_formatted)

    if agent.type == 'worker':
        raise NotImplementedError
    
    elif agent.type == 'orchestrator':
        orchestrator_template = get_template("prompts/orchestrator_agent_prompt.md")
        orchestrator_prompt = orchestrator_template.render(current_date=str(date.today()),general_instructions=general_instructions)
        #print(orchestrator_prompt)

    elif agent.type == 'eval':
        raise NotImplementedError
    else:
        raise ValueError(f"Cannot format prompt as Incorrect Agent Type: {agent.type} was given.")

def get_template(filepath:str):
    with open(filepath,encoding="utf-8") as f:
        raw_md = f.read()
    template = Template(raw_md)
    return template

if __name__ == "__main__":
    format()