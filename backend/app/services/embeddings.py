#import os
#from openai import OpenAI
##from dotenv import load_dotenv

##load_dotenv()

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#def embed_text(text: str) -> list[float]:
    #"""Convert any text into a vector using OpenAI embeddings."""
    #response = client.embeddings.create(
        #input=text,
        #model="text-embedding-3-small"
    #)
    #return response.data[0].embedding

#def embed_batch(texts: list[str]) -> list[list[float]]:
    #"""Convert multiple texts into vectors in one API call."""
    #response = client.embeddings.create(
        #input=texts,
        #model="text-embedding-3-small"
    #)
    #return [item.embedding for item in response.data]

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

def embed_text(text: str) -> list[float]:
    """Use Hugging Face free inference API for embeddings."""
    response = httpx.post(
        "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
        json={"inputs": text, "options": {"wait_for_model": True}},
        timeout=30.0
    )
    result = response.json()
    if isinstance(result[0], list):
        return result[0]
    return result

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts."""
    return [embed_text(text) for text in texts]