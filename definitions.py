from dataclasses import dataclass
from typing import Any
from enum import Enum

@dataclass
class Model:
    name: str
    context_window: int
    input_cost: float
    output_cost: float


class ModelType(Enum):
    MINI = Model(
        name="gpt-4.1-mini",
        context_window=1000000,
        input_cost=0.40,
        output_cost=1.60
    )

class AgentType(Enum):
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    EVALUATOR = "evaluator"

"""
gpt_4o = Model(
    name="gpt-4o",
    context_window=128000,
    input_cost=2.50,
    output_cost=10.0
)

gpt_41 = Model(
    name="gpt-4.1",
    context_window=1000000,
    input_cost=2.0,
    output_cost=8.0
)
reasoning_model = Model(
    name="o3",
    context_window=200000,
    input_cost=2.00,
    output_cost=8.00
)
gpt_41_nano = Model(
    name="gpt-4.1-nano",
    context_window=1000000,
    input_cost=0.10,
    output_cost=0.40
)
gpt_41_mini = Model(
    name="gpt-4.1-mini",
    context_window=1000000,
    input_cost=0.40,
    output_cost=1.60
)
"""