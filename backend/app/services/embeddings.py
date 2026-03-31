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
import hashlib
import math

def _hash_embed(text: str, dims: int = 384) -> list[float]:
    """
    Fast deterministic embedding using hash functions.
    Same text always produces same vector.
    """
    vec = []
    for i in range(dims):
        h = hashlib.sha256(f"{i}:{text}".encode()).digest()
        val = int.from_bytes(h[:4], 'big') / 0xFFFFFFFF
        vec.append(val * 2 - 1)
    norm = math.sqrt(sum(x*x for x in vec))
    return [x/norm for x in vec]

def embed_text(text: str) -> list[float]:
    return _hash_embed(text, dims=384)

def embed_batch(texts: list[str]) -> list[list[float]]:
    return [embed_text(t) for t in texts]