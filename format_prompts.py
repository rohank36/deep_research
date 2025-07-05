from jinja2 import Template
from datetime import datetime
from agent import Agent, AgentType
from typing import List
from utils import get_datetime

def format(agent:Agent):
    available_tools:dict = agent.tools_available
    available_tools_formatted = "\n".join(f"    {available_tools[tool]["schema"]}" for tool in available_tools)
    general_instructions_template = get_template("prompts/general_instructions.md")
    general_instructions = general_instructions_template.render(tools_available=available_tools_formatted)

    if agent.type == AgentType.WORKER:
        worker_template = get_template("prompts/worker_agent.prompt.md")
        worker_prompt = worker_template.render(current_date=get_datetime(),general_instructions=general_instructions)
        return worker_prompt
    
    elif agent.type == AgentType.ORCHESTRATOR:
        orchestrator_template = get_template("prompts/orchestrator_agent_prompt.md")
        orchestrator_prompt = orchestrator_template.render(current_date=get_datetime(),general_instructions=general_instructions)
        #print(orchestrator_prompt)
        return orchestrator_prompt

    elif agent.type == AgentType.EVALUATOR:
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