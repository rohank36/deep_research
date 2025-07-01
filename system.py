from openai import OpenAI
import os
from dotenv import load_dotenv
from orchestrator_agent import OrchestratorAgent
from definitions import Model

"""
Answer to user query: Convent of Our Lady of Mercy
"""

def run_system():
    load_dotenv()  
    openai_api_key = os.getenv("OPENAI_API_KEY") 
    openai_client = OpenAI(api_key=openai_api_key) # have to really think about how this will be shared among agents. Is it safe doing so for multi threaded processes? 

    model = Model(
        name="gpt-4o",
        client=openai_client,
        context_window=128000,
        description=None,
        input_cost=2.50,
        output_cost=10.0
    )
    reasoning_model = Model(
        name="o3",
        client=openai_client,
        context_window=200000,
        description=None,
        input_cost=2.00,
        output_cost=8.00
    )
    oa = OrchestratorAgent(model=model)
    oa.run()
    

def print_oa_init(oa:OrchestratorAgent):
    print(f"UID ({type(oa.uid)}): {oa.uid}\n\n")
    print(f"Type ({type(oa.type)}): {oa.type}\n\n")
    print(f"Description ({type(oa.description)}): {oa.description}\n\n")
    print(f"Datetime Created ({type(oa.datetime_created)}): {oa.datetime_created}\n\n")
    print(f"Health ({type(oa.health)}): {oa.health}\n\n")
    print(f"Total Cost ({type(oa.total_cost)}): {oa.total_cost}\n\n")
    print(f"Total Prompt Tokens ({type(oa.total_prompt_tokens)}): {oa.total_prompt_tokens}\n\n")
    print(f"Total Completion Tokens ({type(oa.total_completion_tokens)}): {oa.total_completion_tokens}\n\n")
    print(f"Model ({type(oa.model)}): {oa.model}\n\n")
    print(f"Num Tool Calls ({type(oa.num_tool_calls)}): {oa.num_tool_calls}\n\n")
    print(f"System Prompt ({type(oa.system_prompt)}): {oa.system_prompt}\n\n")
    print(f"Terminate ({type(oa.terminate)}): {oa.terminate}\n\n")
    print(f"Messages ({type(oa.messages)}): {oa.messages}\n\n")
    print(f"Tools Available ({type(oa.tools_available)}): {oa.tools_available}\n\n")
