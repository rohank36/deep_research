from typing import List,Tuple
import re
from definitions import Model
from client import get_openai_client

def llm_call(model:Model,messages:List[dict[str,str]]) -> Tuple[str,dict[str,int]]:
    openai_client = get_openai_client()
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

def check_llm_response(llm_res_d:dict[str,str]) -> Tuple[str,bool]:
    tags  = ["thinking","text","tool_use"]
    not_in_res = []
    for t in tags: 
        if t not in llm_res_d:
            not_in_res.append(t)
    
    if len(not_in_res) > 0:
        return f"You didn't include {not_in_res} tags in your response. Give your response again but use the proper formatting.", False

    return "",True 


def calculate_cost_of_inference(model:Model, prompt_tokens:int, completion_tokens:int) -> float:
    # $ cost per 1m tokens
    onem = 1000000
    input_cost = (prompt_tokens/onem) * model.input_cost
    completion_cost = (completion_tokens/onem) * model.output_cost
    total_cost = input_cost + completion_cost
    return total_cost

