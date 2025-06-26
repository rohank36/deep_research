from openai import OpenAI
import os
from dotenv import load_dotenv

def main():
    load_dotenv()  
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=openai_api_key)