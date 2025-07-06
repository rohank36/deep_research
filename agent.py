from typing import List,Any,Union,Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from definitions import AgentHealth, Model
from enum import Enum
from utils import uid_hash, get_datetime
from llm_utils import calculate_cost_of_inference
from datetime import datetime

class AgentType(Enum):
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    EVALUATOR = "evaluator"

@dataclass
class Agent(ABC):
    type: AgentType 
    description: str
    health: AgentHealth
    total_cost: float
    total_prompt_tokens: int
    total_completion_tokens: int
    model: Model
    num_tool_calls: int
    datetime_created:str = field(default_factory=get_datetime)
    uid:str = field(default_factory=uid_hash)
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
        return self.health.health_score
    
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
    
    def _update_health(self) -> None:
        self.health.health_score = self.total_prompt_tokens / self.model.context_window

    def _update_total_cost(self,prompt_tokens:int,completion_tokens:int):
        input_cost, completion_cost, total_cost = calculate_cost_of_inference(self.model,prompt_tokens,completion_tokens)
        self.total_cost += total_cost
    
    def _update_total_prompt_tokens(self,prompt_tokens:int):
        self.total_prompt_tokens += prompt_tokens
    
    def _update_total_completion_tokens(self,completion_tokens:int):
        self.total_completion_tokens += completion_tokens
    
    def _update_total_tool_calls(self, tool_calls:int):
        self.num_tool_calls += tool_calls
    
    def update_snapshot(self,prompt_tokens_used,completion_tokens_used,tool_calls) -> None:
        self._update_total_prompt_tokens(prompt_tokens=prompt_tokens_used)
        self._update_total_completion_tokens(completion_tokens=completion_tokens_used)
        self._update_total_tool_calls(tool_calls=tool_calls)
        self._update_total_cost(prompt_tokens=prompt_tokens_used,completion_tokens=completion_tokens_used)
        self._update_health()

