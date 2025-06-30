from typing import List, Union, Callable
from agent import AgentType


# TOOL SCHEMAS

general_tool_schema = {
    "name":str,
    "description":str,
    "parameters":{
        "type":"object",
        "properties":{
            "property1":{
                "type":"str,etc",
                "description":str
            }
        },
        "required":[""] #list of required properties
    }
}

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
def read_plan():
    raise NotImplementedError

def create_plan():
    raise NotImplementedError

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

