import json
from typing import List,Union
from datetime import datetime
from definitions import MemoryNode,Thinking,Tool,Model

"""
Memory structure
{
    "agent_id":[MemoryNode_1, MemoryNode_2, MemoryNode_3,...,MemoryNode_N],
}

"""

def get_datetime_filename_safe() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

class Memory:
    def __init__(self):
        self.FILEPATH = f"memory_archive/memory_{get_datetime_filename_safe()}.md"
        self.MEMORY: dict[str, List[MemoryNode]] = {}

    def add_memory(self,agent_uid:str,content:Union[Thinking,Tool]) -> None:
        mem_node = MemoryNode(agent_uid,content)
        if agent_uid != mem_node.agent_uid: 
            raise ValueError("agent.uid != agent.uid in MemoryNode")
        mem = self.MEMORY
        if agent_uid not in mem:
            mem[agent_uid] = []
        mem[agent_uid].append(mem_node)

    def get_all_agent_memory(self,agent_uid:str) -> List[MemoryNode]:
        return self.MEMORY[agent_uid]

    def get_memory(self,agent_id:str,mem_id:str) -> MemoryNode:
        agent_mem = self.MEMORY[agent_id]
        for mem in agent_mem:
            if mem.memory_uid == mem_id:
                return mem
        raise ValueError(f"mem_id: {mem_id} not found.")

    def get_latest_agent_memory(self,agent_uid:str) -> MemoryNode:
        mem = self.MEMORY
        agent_mem = mem[agent_uid]
        return agent_mem[-1]

    def get_all_memory(self) -> dict[str, List[MemoryNode]]: 
        return self.MEMORY

    def save_memory(self) -> None:
        with open(self.FILEPATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.MEMORY, default=lambda o: o.__dict__))


MEM = Memory() # to be used across system


class Trajectories:
    """ Store the trajectories??? Do we need this, have to think about it more. """
    pass

if __name__ == "__main__":
    from utils import uid_hash
    from orchestrator_agent import OrchestratorAgent
    import time

    th1 = Thinking(uid_hash(),"th1")
    th2 = Thinking(uid_hash(),"th2")
    t1 = Tool(uid_hash(),"fn1",{"arg1":1}) 
    t2 = Tool(uid_hash(),"fn2",{"arg2":2}) 

    model = Model(
        name="gpt-4o",
        client=None,
        context_window=128000,
        description=None,
        input_cost=2.50,
        output_cost=10.0
    )

    oa1 = OrchestratorAgent(model=model)
    oa2 = OrchestratorAgent(model=model)
    #print(oa1.uid,oa2.uid)

    mem1 = MemoryNode(oa1.uid,th1)
    mem2 = MemoryNode(oa1.uid,th2)
    mem3 = MemoryNode(oa2.uid,t1)

    mem = Memory()
    mem.add_memory(oa1.uid,mem1)
    mem.add_memory(oa1.uid,mem2)
    mem.add_memory(oa2.uid,mem3)
    print("\nFull Memory:\n")
    print(mem.MEMORY)
    print("\nGet All Agent Memory:\n")
    print(mem.get_all_agent_memory(oa2.uid))
    print("\nGet Latest Agent Memory:\n")
    latest_mem = mem.get_latest_agent_memory(oa1.uid)
    print(latest_mem)
    print("\nGet specific Agent Memory:\n")
    print(mem.get_memory(oa1.uid,latest_mem.memory_uid))
    print("")
    #mem.clear()
    #mem.save_memory()
    #print(mem.read())
