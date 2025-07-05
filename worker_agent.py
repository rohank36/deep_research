from agent import Agent, AgentType
from typing import List,Any,override
from definitions import Model, AgentHealth
from tools import TOOLS
from format_prompts import format
from llm_utils import llm_call,parse_llm_response

class WorkerAgent(Agent):
    def __init__(self, model:Model, task:str):
        super().__init__(
            type = AgentType.WORKER,
            description = "Search the web to find a reasonable answer based on the task assigned",
            health = AgentHealth(0.0),
            total_cost = 0.0,
            total_prompt_tokens = 0,
            total_completion_tokens = 0,
            model = model,
            num_tool_calls = 0
        )
        self.task: str = task
        self.tools_available.update(TOOLS[self.type])
        self.system_prompt = format(self)
        self.messages += [
            {"role":"system","content":self.system_prompt},
            {"role":"user","content":self.task}
        ]
        #super().__init__( # args ) # must call super init with required parameters as defined in agent abstract interface    

    @override
    def run(self) -> str:
        max_step_limit = 20
        for _ in range(max_step_limit):
            res,tokens = llm_call(self.model.client,self.model.name,self.messages)
            print(f"\n\nLLM RESULT:\n{res}\n\n")
            llm_results = parse_llm_response(res)
            thinking_and_tool = f"{llm_results["thinking"]}\n\n{llm_results["tool_use"]}" 
            # only add thinking and tool use to context to optimize prompt token usage. 
            self.messages += [
                {"role":"assistant","content": thinking_and_tool}
            ]
            
            self.update_snapshot(tokens["prompt_tokens"],tokens["completion_tokens"],1)

            if llm_results["tool_use"] == {}:
                return llm_results['text']
            
            # execute tool use here

            break # temp 
            

    @override
    def terminate_agent(self):
        return NotImplementedError

if __name__ == "__main__":
    """
    Sample prompt from orchestrator agent:
    "Research school mergers in the 1990s that involved combining a girls' and a boys' school to form a coeducational school, given a Latin name, in a town with a history reaching back to the second half of the 19th century. Specifically, identify the name of the original girls' school that was part of this merger."
    """