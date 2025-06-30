from agent import Agent
from typing import List,Any

class OrchestratorAgent(Agent):
    def __init__(self):
        name = "Orchestrator"
        description = "Generate plan to solve user query, assign tasks to worker agents, monitor agents, compile final answer."
        
        #super().__init__( # args ) # must call super init with required parameters as defined in agent abstract interface
        
        raise NotImplementedError
    
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
