import os
from functools import lru_cache
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()    

@lru_cache(maxsize=1)  # memoises the result – next calls return the same object
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

