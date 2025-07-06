from agent import Agent, AgentType
from typing import List,Any, Union, Callable, override
from definitions import AgentHealth, Model, Thinking, Tool
from format_prompts import format
from tools import TOOLS, execute_tool
from llm_utils import llm_call,parse_llm_response, check_llm_response
import re
import json
import time
from memory import MEM

class OrchestratorAgent(Agent):
    def __init__(self,model:Model,query:str):

        # must call super init with required parameters as defined in agent abstract interface
        super().__init__(
            type = AgentType.ORCHESTRATOR,
            description = "Generate plan to solve user query, assign tasks to worker agents, monitor agents, compile final answer.",
            health = AgentHealth(0.0),
            total_cost = 0.0,
            total_prompt_tokens = 0,
            total_completion_tokens = 0,
            model = model,
            num_tool_calls = 0
        )
        self.query:str = query
        # have to define the tools available to the agent before you initialize the prompt
        self.tools_available.update(TOOLS[self.type])
        self.system_prompt = format(self)
        self.messages += [
            {"role":"system","content":self.system_prompt},
            {"role":"user","content":self.query}
        ]

    @override
    def run(self) -> str:
        max_step_limit = 5
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

            # if you need to start using memory later
            # thinking_obj = Thinking(llm_results["thinking"])
            # MEM.add_memory(self.uid,thinking_obj)
            # MEM.save_memory()
        
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


    
                
    
    @staticmethod
    def parse_tasks(tasks_xml:str) -> List[dict]:
        """
        pattern = r"<description>(.*?)</description>"
        return [{"uid":uid_hash(),"description":match.strip()} for match in re.findall(pattern, tasks_xml, re.DOTALL)]
        """
        if "<tasks>" not in tasks_xml or "</tasks>" not in tasks_xml:
            return []

        # Extract the content within <tasks>...</tasks>
        start = tasks_xml.index("<tasks>")
        end = tasks_xml.index("</tasks>") + len("</tasks>")
        tasks_section = tasks_xml[start:end]

        pattern = r"<description>(.*?)</description>"
        return [{"uid": "placeholder", "description": match.strip()}
                for match in re.findall(pattern, tasks_section, re.DOTALL)]
    
    def monitor_worker_agent_thinking_trajectories():
        raise NotImplementedError
    
    def monitor_worker_agent_health(self):
        raise NotImplementedError

    def terminate_worker_agent():
        # force return agent's last answer 
        # break out of agent's run loop
        # honestly the above should be a Agent function.
        # stop that agent's thread 
        # remove agent from WORKER_AGENTS

        raise NotImplementedError
    
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
    xml_input = """
    <text>
        <tasks>
            <task>
                <description>Task 1 description</description>
            </task>
            <task>
                <description>Task 2 description</description>
            </task>
        </tasks>
    </text>
    """
    print(OrchestratorAgent.parse_tasks(xml_input))