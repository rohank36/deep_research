from typing import List, Union, Callable
from agent import AgentType, Agent

# TOOL SCHEMAS

# for reading and writing filepaths you should handle that
read_plan_schema = {
    "name":"read_plan",
    "description":"Get the contents of your current plan",
    "parameters":{
        "type":"object",
        "properties":{},
        "required":[]
    }
}

create_plan_schema = {
    "name":"create_plan",
    "description":"Create a plan",
    "parameters":{
        "type":"object",
        "properties":{
            "content":{
                "type":"string",
                "description":"The content of the plan"
            }
        },
        "required":["content"]
    }
}

edit_plan_schema = {}

# TOOL FUNC DEFINITIONS
def read_plan(agent:Agent) -> str:
    filepath = f"/agent_plans/{agent.uid}_plan.md"
    with open(filepath,encoding="utf-8") as f:
        raw_md = f.read()
    return raw_md

def create_plan(agent:Agent,content:str) -> None:
    filepath = f"/agent_plans/{agent.uid}_plan.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    

"""
Example:

TOOLS = [
    "read_file":{
        "func": read_file, # callable function defined in tools.
        "schema": read_file_schema
    }
]

"""

# TOOL REGISTRY

TOOLS: dict[AgentType,dict[str,dict[str,Union[Callable,str]]]] = {
    AgentType.ORCHESTRATOR:{
        "read_plan":{
            "func":read_plan,
            "schema":read_plan_schema
        },
        "create_plan":{
            "func":create_plan,
            "schema":create_plan_schema
        }
    },
    AgentType.WORKER: {},
    AgentType.EVALUATOR: {}
}

