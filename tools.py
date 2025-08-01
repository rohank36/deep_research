from typing import List, Union, Callable, Any, Tuple
from utils import uid_hash
from definitions import ModelType, AgentType

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from concurrent.futures import ThreadPoolExecutor, as_completed

# TOOL SCHEMAS

run_subagent_schema = {
    "name":"run_subagent",
    "description":"Create and run a single subagent to accomplish a task",
    "parameters":{
        "type":"object",
        "properties":{
            "prompt":{
                "type":"string",
                "description":"The specific task that for the subagent to accomplish"
            }
        },
        "required":["prompt"]
    }
}

run_subagents_parallel_schema = {
    "name":"run_subagents_parallel",
    "description":"Create multiple subagents to run in parallel",
    "parameters":{
        "type":"object",
        "properties":{
            "num_agents":{
                "type":"int",
                "description":"The number of subagents to create"
            },
            "prompts":{
                "type":"List[strings]",
                "description":"A list of specific tasks for each of the subagents to accomplish"
            }
        },
        "required":["num_agents","prompts"]
    }
}

search_schema = {
    "name":"search",
    "description":"Search the web and get the top urls based on the query",
    "parameters":{
        "type":"object",
        "properties":{
            "query":{
                "type":"str",
                "description":"the query that will be used to find relevant urls"
            },
        },
        "required":["query"]
    }
}

fetch_content_schema = {
    "name":"fetch_content",
    "description":"Get all the text content of a webpage",
    "parameters":{
        "type":"object",
        "properties":{
            "url":{
                "type":"str",
                "description":"the url whose content will be fetched"
            },
        },
        "required":["url"]
    }
}


# TOOL FUNC DEFINITIONS
def run_subagent(args:dict)->Tuple[str,dict]:
    """
    args:
    - prompt:str
    """
    from agent import Agent
    #return "I HAVE THE ANSWER TO THE USER QUERY, IT MAY SEEM WRONG BUT I KNOW IT IS RIGHT. THE ANSWER IS: I'M BATMAN"
    prompt = args["prompt"]
    wa = Agent(AgentType.WORKER,ModelType.MINI.value,15,prompt)
    res,ss = wa.run()
    return res,ss

def run_subagents_parallel(args:dict):
    """
    args:
    - num_agents:int
    - prompts:List[str]
    """
    from agent import Agent
    num_agents = args["num_agents"]
    prompts = args["prompts"]

    if num_agents != len(prompts):
        raise ValueError(f"num_agents {num_agents} != len(prompts) {len(prompts)}")
    
    def launch(prompt: str):
        sa = Agent(AgentType.WORKER, ModelType.MINI.value, 15, prompt)
        return sa.run() # (answer, snapshot)

    answers = [""] * num_agents      
    total_cost = 0.0
    total_calls = 0

    with ThreadPoolExecutor(max_workers=num_agents) as pool:
        futures = {pool.submit(launch, p): idx for idx, p in enumerate(prompts)}
        for fut in as_completed(futures):
            idx = futures[fut]
            ans, ss = fut.result()
            answers[idx] = f"Subagent {idx+1}: {ans}"
            total_cost += ss["total_cost"]
            total_calls += ss["num_tool_calls"]

    combined_answer = "\n\n".join(answers)
    combined_snapshot = {
        "uid": uid_hash(),
        "type": "worker_group",
        "model": "many",
        "health": 0.0,
        "total_cost": total_cost,
        "num_tool_calls": total_calls,
    }
    return combined_answer, combined_snapshot


def search(args:dict) -> str:
    """
    args: 
    - query:str
    - max_links: int = 5
    """
    query:str = args["query"] 
    max_links:int = 5

    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f"https://duckduckgo.com/?q={query.replace(' ', '+')}&t=h_&ia=web")

        # Wait for results page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ol.react-results--main"))
        )

        # Extract top result links
        elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='result-title-a']")
        links = [e.get_attribute("href") for e in elements[:max_links] if e.get_attribute("href")]

        snippet_divs = driver.find_elements(By.CSS_SELECTOR, "div[data-result='snippet']")
        snippets = [s.text.strip() for s in snippet_divs[:max_links] if s.text.strip()]

        results:List[dict[str,str]] = []
        for i in range(min(len(links), len(snippets))):
            results.append({
                "url": links[i],
                "snippet": snippets[i]
            })

        formatted = "\n\n".join(
            f"Link {i+1}: {item['url']}\nDescription: {item['snippet']}"
            for i, item in enumerate(results)
        )

        return formatted

    finally:
        driver.quit()

def fetch_content(args:dict) -> str:
    """
    args:
    - url:str
    """
    url:str = args["url"]
    #TODO: have to refine the final content served (theres a lot of noise - e.g. random works from the site). Need to clean.
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Wait for page body to fully render
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Get rendered HTML and parse
        soup = BeautifulSoup(driver.page_source, "html.parser")
        body = soup.find("body") #str
        body_text = body.get_text(separator="\n", strip=True) if body else ""
        final_str =  f"Here is the text content for {url}:\n\n{body_text}"

        return final_str
    
    finally:
        driver.quit()
    

# TOOL REGISTRY
TOOLS: dict[AgentType,dict[str,dict[str,Union[Callable,str]]]] = {
    AgentType.ORCHESTRATOR:{
        "run_subagent":{
            "func":run_subagent,
            "schema":run_subagent_schema
        },
        "run_subagents_parallel":{
            "func":run_subagents_parallel,
            "schema":run_subagents_parallel_schema
        }
    },
    AgentType.WORKER: {
        "search":{
            "func":search,
            "schema":search_schema
        },
        "fetch_content":{
            "func":fetch_content,
            "schema":fetch_content_schema
        },
    },
    AgentType.EVALUATOR: {}
}


def execute_tool(agent_type:str, tool_call:dict[str,Union[str,dict]]) -> Tuple[Any,bool]:
    tool_name:str = tool_call["name"]
    args:dict = tool_call["args"]

    is_agent_call = False
    if tool_name == "run_subagent" or tool_name == "run_subagents_parallel":
        is_agent_call = True

    # check to ensure fn exists and llm didn't hallucinate 
    if tool_name not in TOOLS[agent_type]:
        return f"Uknown tool name: {tool_name}",False,False
    
    selected_tool:dict = TOOLS[agent_type][tool_name]

    # check to ensure required args are given
    if list(args.keys()).sort() != selected_tool['schema']['parameters']['required'].sort():
        return f"Missing required arguments from tool call: {tool_name}",False,False
    
    try:
        fn_res = selected_tool["func"](args)
    
    # catch exception from func call
    except Exception as e:
        return F"Error executing tool --> {tool_name}:\n{e}",False,False
    
    return fn_res,is_agent_call,True


