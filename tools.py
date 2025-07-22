from typing import List, Union, Callable, Any, Tuple
from utils import uid_hash
from definitions import ModelType, AgentType

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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
    temp_ss = {
            "uid": 12341234,
            "type": "worker",
            "model": "ur mom",
            "health": 0.1,
            "total_cost": 0,
            "num_tool_calls": 0
        }
    return "I HAVE THE ANSWER TO THE USER QUERY, IT MAY SEEM WRONG BUT I KNOW IT IS RIGHT. THE ANSWER IS: I'M BATMAN",temp_ss
    #raise NotImplementedError


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

        ############ Just for observability during testing
        with open(f"site_content/{uid_hash()}.txt","w",encoding="utf-8") as f:
            f.write(final_str)
        ############

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
        return f"Uknown tool name: {tool_name}", False
    
    selected_tool:dict = TOOLS[agent_type][tool_name]

    # check to ensure required args are given
    if list(args.keys()).sort() != selected_tool['schema']['parameters']['required'].sort():
        return f"Missing required arguments from tool call: {tool_name}", False
    
    try:
        fn_res = selected_tool["func"](args)
    
    # catch exception from func call
    except Exception as e:
        return F"Error executing tool --> {tool_name}:\n{e}", False
    
    return fn_res,is_agent_call,True


if __name__ == "__main__":
    #results = search("how transformers work in deep learning")
    #print(results)
    url_results = [{'url': 'https://www.datacamp.com/tutorial/how-transformers-work', 'snippet': 'Jan 9, 2024The deep learning field has been experiencing a seismic shift, thanks to the emergence and rapid evolution of Transformer models. These groundbreaking architectures have not just redefined the standards in Natural Language Processing (NLP) but have broadened their horizons to revolutionize numerous facets of artificial intelligence. Characterized by their unique attention mechanisms and ...'}, {'url': 'https://www.geeksforgeeks.org/deep-learning/architecture-and-working-of-transformers-in-deep-learning-/', 'snippet': 'May 29, 2025Transformers are a type of deep learning model that utilizes self-attention mechanisms to process and generate sequences of data efficiently. They capture long-range dependencies and contextual relationships making them highly effective for tasks like language modeling, machine translation and text generation.'}, {'url': 'https://theaisummer.com/transformer/', 'snippet': 'An intuitive understanding on Transformers and how they are used in Machine Translation. After analyzing all subcomponents one by one such as self-attention and positional encodings , we explain the principles behind the Encoder and Decoder and why Transformers work so well'}, {'url': 'https://www.turing.com/kb/brief-introduction-to-transformers-and-their-power', 'snippet': 'Transformers are neural networks that learn context & understanding through sequential data analysis. Know more about its powers in deep learning, NLP, & more.'}, {'url': 'https://towardsdatascience.com/transformers-explained-visually-part-1-overview-of-functionality-95a6dd460452/', 'snippet': 'The article visually explains the functionality of transformers in deep learning, covering their key components and how they work.'}]
    """
    for d in url_results:
        print(f"url:{d["url"]}")
        print(f"description:{d["snippet"]}")
        print("\n\n")
    """
    #body = fetch_content(url_results[0]["url"])
    args = {"url":url_results[0]["url"]}
    fetch_content(args)
    #print(body)

