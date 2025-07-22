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


if __name__ == "__main__":
    s = f"""
    <thinking>
    The search results include several links, some of which are relevant and contain references to 1990s school mergers involving girls' and boys' schools, with Latin names, in towns with a history dating back to the 19th century. Notably, there are links to archives and collections that might contain detailed records about such mergers. The second and fifth links are from the British Newspaper Archive, which could have newspaper reports about these mergers, including specific schools and towns. The first and third links seem to be more general or commercial and less directly relevant. The fourth link is about dictionary definitions and unlikely to contain specific case studies.

    Given the volume of newspaper articles (over 15,000 results in some searches), I should specifically check the most promising links—particularly the British Newspaper Archive links—that may mention the original girls' school involved in such a merger. These archives might list the schools' names, the town, and historical details.

    I'll start by examining the second British Newspaper Archive search result link, as it explicitly references 1990s mergers with specific search parameters for England, which is likely to include relevant cases.
    </thinking>

    <text>
    I will review the British Newspaper Archive results related to 1990s girls' and boys' school mergers with Latin names in towns with 19th-century histories. Focusing on newspaper reports can provide detailed, specific information about the schools involved and their histories.
    </text>
    <tool_use>
    {{
        "name": "fetch_content",
        "args": {{
            "url": "https://www.britishnewspaperarchive.co.uk/search/results/1950-01-01/1999-12-31?basicsearch=girls%20school%20merged%201990s%20into%20coeducational%20school%20with%20latin%20name%20town%20history%20half%2019th%20century&country=england"
        }}
    }}
    """
    res = parse_llm_response(s)
    if "tool_use" not in res: print("TRUE")