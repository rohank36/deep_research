from agent import Agent, AgentType
from typing import List,Any,override
from definitions import Model, AgentHealth
from tools import TOOLS,execute_tool
from format_prompts import format
from llm_utils import llm_call,parse_llm_response, check_llm_response
import json
import time

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
        max_step_limit = 15
        for step in range(max_step_limit):
 
            if step == max_step_limit - 1 or self.heartbeat() > 0.6 or self.terminate:
                # last step or bad health or orchestrator terminated agent so just give an answer 
                final_ans = self.terminate_agent()
                print(f"Agent {self.uid} terminated....")
                return final_ans
                
            res,tokens = llm_call(self.model,self.messages)
            print(f"\n\nLLM RESULT:\n{res}\n\n")
            llm_results = parse_llm_response(res)
            llm_check_res,ok = check_llm_response(llm_results)

            if not ok:
                self.update_snapshot(tokens["prompt_tokens"],tokens["completion_tokens"],0)
                print(f"\n\nLLM CHECK RESULT:\n{llm_check_res}\n\n")
                self.messages += [
                    {"role":"user","content":llm_check_res}
                ]
                continue 

            thinking_and_tool = f"{llm_results["thinking"]}\n\n{llm_results["tool_use"]}" 

            # only add thinking and tool use to context to optimize prompt token usage. 
            self.messages += [
                {"role":"assistant","content": thinking_and_tool}
            ]

            tools_called = json.loads(llm_results["tool_use"])
            if tools_called == {}:
                self.update_snapshot(tokens["prompt_tokens"],tokens["completion_tokens"],0)
                return llm_results['text']
            
            tool_call_res,ok = execute_tool(self,tools_called)
            print(f"\n\nTOOL CALL RES:\n{tool_call_res}\n\n")

            self.messages += [
                {"role":"user","content":str(tool_call_res)}
            ]

            self.update_snapshot(tokens["prompt_tokens"],tokens["completion_tokens"],1)

            time.sleep(5) # for openai api rate limiting

        return "None"
            

    @override
    def terminate_agent(self) -> str:
        self.messages += [
            {"role":"user","content":"You have run out of time. Based on your research, give your final answer:\n"}
        ]
        res,tokens = llm_call(self.model,self.messages)
        self.update_snapshot(tokens["prompt_tokens"],tokens["completion_tokens"],0)
        llm_results = parse_llm_response(res)
       
        llm_check_res,ok = check_llm_response(llm_results)
        if not ok:
            return res # if a tag is missing something just return the whole answer.
        
        return llm_results['text']
    

if __name__ == "__main__":
    """
    Sample prompt from orchestrator agent:
    "Research school mergers in the 1990s that involved combining a girls' and a boys' school to form a coeducational school, given a Latin name, in a town with a history reaching back to the second half of the 19th century. Specifically, identify the name of the original girls' school that was part of this merger."
    """