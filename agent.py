from typing import Any,Tuple
from definitions import Model,AgentType
from utils import uid_hash
from llm_utils import llm_call,parse_llm_response,check_llm_response, calculate_cost_of_inference
import time
import json
from tools import TOOLS, execute_tool
from format_prompts import format

class Agent:
    def __init__(self, type:AgentType, model:Model, max_steps:int, task:str):
        self.uid = uid_hash()
        self.type = type
        self.model = model
        self.max_steps = max_steps
        self.task = task

        self.total_cost = 0.0
        self.health = 0.0
        self.tools_available = {}
        self.tools_available.update(TOOLS[self.type])
        self.should_terminate = False
        self.sys_prompt = format(self.tools_available,self.type)
        self.num_tool_calls = 0
        self.messages = [
            {"role":"system","content":self.sys_prompt},
            {"role":"user","content":self.task}
        ]

    def run(self) -> Tuple[str,dict]:
        """ return agent response and final snapshot"""
        for step in range(self.max_steps):
 
            if step == self.max_steps - 1 or self.health > 0.6 or self.should_terminate:
                # last step or bad health or orchestrator terminated agent so just give an answer 
                final_ans = self.terminate()
                print(f"Agent {self.uid} terminated....")
                return final_ans,self.snapshot()
                
            res,tokens = llm_call(self.model,self.messages)
            print(f"\n\nLLM RESULT ({self.type}):\n{res}\n\n")
            llm_results = parse_llm_response(res)
            llm_check_res,ok = check_llm_response(llm_results)

            if not ok:
                self.update_cost_and_health(tokens["prompt_tokens"],tokens["completion_tokens"])
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
                self.update_cost_and_health(tokens["prompt_tokens"],tokens["completion_tokens"])
                return llm_results['text'],self.snapshot()
            
            tool_call_res,is_agent_call,_= execute_tool(self.type,tools_called)
            if is_agent_call:
                #tool_call_res: Tuple[str,dict]
                # this agent called a subagent so we aggregate subagents work as part of this agents work
                ss = tool_call_res[1]
                self.total_cost += ss["total_cost"]
                self.update_tool_calls(ss["num_tool_calls"])
                
            print(f"\n\nTOOL CALL RES:\n{tool_call_res}\n\n")

            self.messages += [
                {"role":"user","content":str(tool_call_res)}
            ]

            self.update_cost_and_health(tokens["prompt_tokens"],tokens["completion_tokens"])
            self.update_tool_calls(1)

            # can deterministically save to memory here if needed 

            time.sleep(5) # for openai api rate limiting

        return "None",self.snapshot()

    def terminate(self) -> str:
        self.messages += [
            {"role":"user","content":"You have run out of time. Based on your research, give your final answer:\n"}
        ]
        res,tokens = llm_call(self.model,self.messages)
        self.update_cost_and_health(tokens["prompt_tokens"],tokens["completion_tokens"])
        llm_results = parse_llm_response(res)
       
        llm_check_res,ok = check_llm_response(llm_results)
        if not ok:
            return res # if a tag is missing something just return the whole answer.
        return llm_results['text']
    
    def update_cost_and_health(self,prompt_tokens:int,completion_tokens:int) -> None:
        self.update_cost(prompt_tokens,completion_tokens)
        self.update_health(prompt_tokens)

    def update_cost(self,prompt_tokens:int,completion_tokens:int) -> None:
        self.total_cost += calculate_cost_of_inference(self.model,prompt_tokens,completion_tokens)
        
    def update_health(self,prompt_tokens:int) -> None:
        self.health = prompt_tokens/self.model.context_window    

    def update_tool_calls(self, n:int) -> None:
        self.num_tool_calls += n
    
    def snapshot(self) -> dict[str,Any]:
        """ returns a logistics snapshot of the agent """
        ss = {
            "uid": self.uid,
            "type": self.type,
            "model": self.model.name,
            "health": self.health,
            "total_cost": self.total_cost,
            "num_tool_calls": self.num_tool_calls
        }
        return ss
    

