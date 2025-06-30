from typing import List,Any,Union,Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from definitions import AgentHealth, Model
from enum import Enum
from utils import agent_uid_hash

class AgentType(Enum):
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    EVALUATOR = "evaluator"

@dataclass
class Agent(ABC):
    type: AgentType 
    description: str
    datetime_created:str
    health: AgentHealth
    total_cost: float
    total_prompt_tokens: int
    total_completion_tokens: int
    model: Model
    num_tool_calls: int
    uid:str = agent_uid_hash()
    system_prompt: Union[str,None] = None #describe task here
    terminate: bool = False
    tools_available: dict[str,dict[str,Union[Callable,str]]] = field(default_factory=dict)
    messages:List[dict[str,str]] = field(default_factory=list) # ensures each instance has its own separate list

    @abstractmethod
    def run(self) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def terminate_agent(self):
        raise NotImplementedError

    def heartbeat(self) -> AgentHealth:
        return self.health
    
    def snapshot(self) -> dict[str,Any]:
        """ returns a logistics snapshot of the agent """
        ss = {
            "uid": self.uid,
            "type": self.type,
            "datetime_created": self.datetime_created,
            "model": self.model,
            "health": self.health,
            "total_cost": self.total_cost,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "num_tool_calls": self.num_tool_calls
        }
        return ss
    
    def update_health(self) -> None:
        self.health.health_score = self.total_prompt_tokens / self.model.context_window

    def update_total_cost(self):
        raise NotImplementedError
    
    def update_total_prompt_tokens(self):
        raise NotImplementedError
    
    def update_total_completion_tokens(self):
        raise NotImplementedError
    
    def update_total_tool_calls(self):
        raise NotImplementedError
    
    def update_snapshot(self) -> None:
        self.update_total_cost()
        self.update_total_prompt_tokens()
        self.update_total_completion_tokens()
        self.update_total_tool_calls()

