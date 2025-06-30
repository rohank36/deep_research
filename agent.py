from typing import List,Any,Union,Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from definitions import AgentHealth, Model
from enum import Enum

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
    system_prompt: Union[str,None] = None #describe task here
    terminate: bool = False
    tools_available: dict[str,dict[str,Union[Callable,str]]] = field(default_factory=dict)
    messages:List[dict[str,str]] = field(default_factory=list) # ensures each instance has its own separate list

    @abstractmethod
    def run(self) -> Any:
        raise NotImplementedError
    
    def terminate_agent(self) -> dict[str,Any]:
        self.terminate = True
        raise NotImplementedError

    def heartbeat(self) -> AgentHealth:
        return self.health
    
    def update_health(self) -> None:
        self.health.health_score = self.total_prompt_tokens / self.model.context_window

