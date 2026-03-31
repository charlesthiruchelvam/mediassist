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
from dotenv import load_dotenv

load_dotenv()

_model = None

def get_model():
    global _model
    if _model is None:
        from fastembed import TextEmbedding
        _model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def embed_text(text: str) -> list[float]:
    model = get_model()
    embeddings = list(model.embed([text]))
    return embeddings[0].tolist()

def embed_batch(texts: list[str]) -> list[list[float]]:
    model = get_model()
    embeddings = list(model.embed(texts))
    return [e.tolist() for e in embeddings]