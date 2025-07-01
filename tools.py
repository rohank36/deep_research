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

complete_task_schema = {
    "name":"complete_task",
    "description":"After the research has been done call this function to output the final answer",
    "parameters":{
        "type":"object",
        "properties":{
            "content":{
                "type":"string",
                "description":"The final report answering the usery query"
            }
        },
        "required":["content"]
    }
}

run_blocking_subagent_schema = {
    "name":"run_blocking_subagent",
    "description":"Create and run a single worker subagent",
    "parameters":{
        "type":"object",
        "properties":{
            "prompt":{
                "type":"string",
                "description":"The specific task that for the subagent to accomplish"
            }
        },
        "required":["prompt"]
    }
}

run_blocking_subagents_parallel_schema = {
    "name":"run_blocking_subagents_parallel",
    "description":"Create multiple worker subagents to run in parallel",
    "parameters":{
        "type":"object",
        "properties":{
            "num_agents":{
                "type":"int",
                "description":"The number of subagents to create"
            },
            "prompts":{
                "type":"List[strings]",
                "description":"A list of specific tasks for each of the subagents to accomplish"
            }
        },
        "required":["num_agents","prompts"]
    }
}


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

def complete_task():
    raise NotImplementedError

def run_blocking_subagent(prompt:str):
    raise NotImplementedError

def run_blocking_subagents_parallel(num_agents:int, prompts:List[str]):
    raise NotImplementedError
    

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
        },
        "complete_task":{
            "func":complete_task,
            "schema":complete_task_schema
        },
        "run_blocking_subagent":{
            "func":run_blocking_subagent,
            "schema":run_blocking_subagent_schema
        },
        "run_blocking_subagents_parallel":{
            "func":run_blocking_subagents_parallel,
            "schema":run_blocking_subagents_parallel_schema
        }
    },
    AgentType.WORKER: {},
    AgentType.EVALUATOR: {}
}

