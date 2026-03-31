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

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> list[float]:
    embedding = model.encode([text])
    return embedding[0].tolist()

def embed_batch(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(texts)
    return embeddings.tolist()