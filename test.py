from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np


def get_embeddings(s:str,model:str,client):
    response = client.embeddings.create(
        input=s,
        model=model
    )
    return response.data[0].embedding # list of floats 

def similarity(emb1,emb2) -> float:
    # all openai embeddings are normalized so can just do dot product 
    return np.dot(emb1, emb2)

def get_embeddings_batch(texts: list[str], model: str, client) -> list[np.ndarray]:
    response = client.embeddings.create(
        input=texts,
        model=model
    )
    return [np.array(r.embedding) for r in response.data]


def main():
    load_dotenv()  
    openai_api_key = os.getenv("OPENAI_API_KEY") 
    openai_client = OpenAI(api_key=openai_api_key)
    t1 = [
        "The user wants a complete list of CTOs from Fortune 500 companies. I’ll begin by scraping the latest Fortune 500 company list from a reliable source like Fortune.com.",
        "Next, I’ll attempt to locate each company's leadership or executive directory page, focusing on roles with the title 'Chief Technology Officer' or equivalent.",
        "If a direct match isn’t found, I’ll extract alternative titles like 'Head of Engineering' or 'VP of Technology' and flag them for human validation."
    ]
    t2 = [
        "The goal is to find CTOs of Fortune 500 firms. I’ll start by querying each company name along with the term 'CTO' to surface reliable data sources like LinkedIn or press releases.",
        "I’ll summarize each search result, extract the most recent executive name and role, and validate the information using multiple sources when possible.",
        "In cases where a CTO isn't explicitly listed, I’ll fall back on related roles such as 'Chief Information Officer' or 'VP of Engineering'."
    ]
    t3 = [
        "Rather than directly searching for CTO names, I’ll start by identifying the typical org chart structure of Fortune 500 tech divisions to understand where CTO roles typically sit.",
        "I’ll then analyze recent SEC filings and executive bios to detect patterns in how companies report technology leadership in public documents.",
        "Based on this structural data, I’ll infer CTO equivalents for companies lacking explicit titles by analyzing reporting relationships to the CEO or CIO."
    ]
    model="text-embedding-3-large" 
    all_texts = t1 + t2 + t3
    all_embeddings = get_embeddings_batch(all_texts, model, openai_client)
    t1_emb = np.sum(all_embeddings[0:3], axis=0)
    t2_emb = np.sum(all_embeddings[3:6], axis=0)
    t3_emb = np.sum(all_embeddings[6:9], axis=0)

    t1_emb /= np.linalg.norm(t1_emb)
    t2_emb /= np.linalg.norm(t2_emb)
    t3_emb /= np.linalg.norm(t3_emb)

    print(f"Using model:{model}")
    print("t1 vs t2 similarity:", similarity(t1_emb, t2_emb))
    print("t1 vs t3 similarity:", similarity(t1_emb, t3_emb))
    print("t2 vs t3 similarity:", similarity(t2_emb, t3_emb))

    
        

    #sim = similarity(get_embeddings(s1,model,openai_client),get_embeddings(s2,model,openai_client))
    #print(sim)
    #sim = similarity(get_embeddings(s1,model,openai_client),get_embeddings(s3,model,openai_client))
    #print(sim)


    # set threshold as 0.65 or 0.8 - have to experiment and play around with this number

if __name__ == "__main__":
    main()