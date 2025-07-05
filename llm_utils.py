import tiktoken
from typing import List,Any,Tuple
import re
from definitions import Model


"""
# Can probably just use token count from OpenAI api res
def count_tokens(model:str,messages:List[dict[str,str]]) -> int:
    encoding = tiktoken.encoding_for_model(model) 

    token_count = 0
    for d in messages:
        tokens = encoding.encode(d["content"])
        token_count += len(tokens)

    return token_count
"""


def llm_call(model:Model,messages:List[dict[str,str]]) -> Tuple[str,dict[str,int]]:
    openai_client = model.client
    model_name = model.name
    response = openai_client.chat.completions.create(
        model=model_name,
        messages=messages
    )
    return response.choices[0].message.content, {"prompt_tokens":response.usage.prompt_tokens, "completion_tokens":response.usage.completion_tokens, "total_tokens":response.usage.total_tokens}

def parse_llm_response(llm_res:str) -> dict[str,str]:
    tags = ["thinking","text","tool_use"]
    results:dict[str,str] = {}

    for tag in tags:
        pattern = rf'<{tag}>(.*?)</{tag}>'
        match = re.search(pattern,llm_res,re.DOTALL)
        if match:
            results[tag] = match.group(1).strip()
    
    return results

def parse_tools(tool_use:str) -> List[dict]:
    #convert string json to dict using json.loads
    #
    raise NotImplementedError


def calculate_cost_of_inference(model:Model, prompt_tokens:int, completion_tokens:int) -> Tuple[int,int,int]:
    # $ cost per 1m tokens
    onem = 1000000
    input_cost = (prompt_tokens/onem) * model.input_cost
    completion_cost = (completion_tokens/onem) * model.output_cost
    total_cost = input_cost + completion_cost
    return input_cost,completion_cost,total_cost