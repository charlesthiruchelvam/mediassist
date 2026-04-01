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
import hashlib
import math
from dotenv import load_dotenv

load_dotenv()

def embed_text(text: str) -> list[float]:
    """
    TF-IDF inspired deterministic embedding.
    Better than pure hash — uses character n-grams for semantic similarity.
    """
    text = text.lower().strip()
    dims = 384
    vec = [0.0] * dims
    
    # Character n-grams (captures semantic meaning better than pure hash)
    for n in [2, 3, 4]:
        for i in range(len(text) - n + 1):
            ngram = text[i:i+n]
            h = int(hashlib.md5(ngram.encode()).hexdigest(), 16)
            idx = h % dims
            vec[idx] += 1.0 / (n * n)
    
    # Word unigrams and bigrams
    words = text.split()
    for i, word in enumerate(words):
        h = int(hashlib.md5(word.encode()).hexdigest(), 16)
        idx = h % dims
        vec[idx] += 2.0
        if i < len(words) - 1:
            bigram = word + " " + words[i+1]
            h2 = int(hashlib.md5(bigram.encode()).hexdigest(), 16)
            idx2 = h2 % dims
            vec[idx2] += 1.5
    
    # Normalize
    norm = math.sqrt(sum(x*x for x in vec))
    if norm > 0:
        vec = [x/norm for x in vec]
    
    return vec

def embed_batch(texts: list[str]) -> list[list[float]]:
    return [embed_text(text) for text in texts]