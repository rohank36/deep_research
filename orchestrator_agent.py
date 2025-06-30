from agent import Agent
from typing import List,Any
from datetime import datetime
from definitions import AgentHealth, Model
from format_prompts import format

class OrchestratorAgent(Agent):
    def __init__(self,model:Model):

        super().__init__(
            type = "orchestrator",
            description = "Generate plan to solve user query, assign tasks to worker agents, monitor agents, compile final answer.",
            datetime_created = str(datetime.today()),
            health = AgentHealth(0.0),
            total_cost = 0.0,
            total_prompt_tokens = 0,
            total_completion_tokens = 0,
            model = model,
            num_tool_calls = 0
        )
        # have to define the tools available to the agent before you initialize the prompt
        self.system_prompt = format(self)

        # must call super init with required parameters as defined in agent abstract interface
        
    
    def run(self) -> str:
        """
        read user input 
        init dag 
        while true:
            check if plan exists, if yes:
                update plan # llm call
            else:
                generate plan # llm call
            save plan to memory
            extract subtasks from plan
            WORKER_AGENTS = []
            for each subtask:
                worker_agent = create_worker_agent()
                WORKER_AGENTS.append(worker_agent)
            Parallel process tasks 
            Start health monitor thread.
            wait for all tasks to be complete
            stop heath monitor thread
            assess agent results # llm call
            if good: break 
            check orchestrator agent health. if > 0.8 break
        
        generate final answer in good format based on information found
        return answer to user
            
        """
        raise NotImplementedError
    
    def monitor_worker_agent_thinking_trajectories():
        raise NotImplementedError
    
    def monitor_worker_agent_health(self):
        """
        
        """
        raise NotImplementedError

    def terminate_worker_agent():
        # force return agent's last answer 
        # break out of agent's run loop
        # honestly the above should be a Agent function.
        # stop that agent's thread 
        # remove agent from WORKER_AGENTS

        raise NotImplementedError
    
    def complete_task():
        raise NotImplementedError
