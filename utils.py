import tiktoken
from dataclasses import dataclass
from typing import List,Any,Tuple
import re

#### For testing LLM call, delete from here later
from openai import OpenAI
import os
from dotenv import load_dotenv
####

@dataclass
class Tool:
    signature:str # similar signatures ==> similar tool calls ==> similar action taken
                  # mabye use semantic hashing?
    name:str
    input:dict[str,Any]
    datetime:str

@dataclass
class Thinking:
    signature:str # have to think more about why Anthropic decided to use a signature instead of a raw ID.
                  # maybe to store in long term memory semanticly? 
    content:str
    datetime:str
    
@dataclass
class Text:
    id:str
    content:str
    datetime:str

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

def llm_call(openai_client,model:str,messages:List[dict[str,str]]) -> Tuple[str,dict[str:int]]:
    response = openai_client.chat.completions.create(
        model=model,
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

def create_tool_object(parsed_llm_res:dict[str,str]) -> Tool:
    content = parse_llm_response["tool_use"]
    raise NotImplementedError

def create_thinking_object(parsed_llm_res:dict[str,str]) -> Thinking:
    content = parse_llm_response["thinking"]
    raise NotImplementedError

def create_text_object(parsed_llm_res:dict[str,str]) -> Text:
    content = parse_llm_response["text"]
    raise NotImplementedError


if __name__ == "__main__":
    from prompts import system_prompt
    from openai import OpenAI
    messages = [
        {'role':"system","content":system_prompt},
        {'role':"user","content":"What tools do you have available to you?"}
    ]
    #print(count_tokens("gpt-4o",messages))


    load_dotenv()  
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    response, token_usage = llm_call(client,"gpt-4o",messages)

    print(f"\n{response}\n")

    print("")
    print("Prompt tokens:", token_usage["prompt_tokens"])
    print("Completion tokens:", token_usage["completion_tokens"])
    print("Total tokens:", token_usage["total_tokens"])
    print("")

    print(parse_llm_response(response))