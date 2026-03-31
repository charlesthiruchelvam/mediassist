import os
import sys

# Add the backend folder to Python path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from supabase import create_client
from openai import OpenAI
from ingestion.chunker import load_documents, chunk_documents

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")  # Service key for write access
)
def embed_chunks(chunks: list) -> list[list[float]]:
    """Convert all chunks to vectors using HuggingFace free API."""
    import httpx
    embeddings = []
    for i, chunk in enumerate(chunks):
        response = httpx.post(
            "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
            json={"inputs": chunk.page_content, "options": {"wait_for_model": True}},
            timeout=30.0
        )
        result = response.json()
        if isinstance(result[0], list):
            embeddings.append(result[0])
        else:
            embeddings.append(result)
        print(f"  Embedded {i+1}/{len(chunks)} chunks...")
    return embeddings

#def embed_chunks(chunks: list) -> list[list[float]]:
    #"""Convert all chunks to vectors using free local model."""
    #from sentence_transformers import SentenceTransformer
    #model = SentenceTransformer("all-MiniLM-L6-v2")
    #texts = [chunk.page_content for chunk in chunks]
    #embeddings = model.encode(texts, show_progress_bar=True)
    #return embeddings.tolist()
#def embed_chunks(chunks: list) -> list[list[float]]:
    #"""Convert all chunks to vectors using OpenAI embeddings."""
    #texts = [chunk.page_content for chunk in chunks]
    #embeddings = []
    #batch_size = 100

    #for i in range(0, len(texts), batch_size):
        #batch = texts[i:i + batch_size]
        #response = openai_client.embeddings.create(
            #input=batch,
            #model="text-embedding-3-small"
        #)
        #embeddings.extend([e.embedding for e in response.data])
        #print(f"  Embedded {min(i + batch_size, len(texts))}/{len(texts)} chunks...")

    #return embeddings

def upsert_to_supabase(chunks: list, embeddings: list) -> None:
    """Store all chunks and their embeddings in Supabase."""
    rows = []
    for chunk, embedding in zip(chunks, embeddings):
        rows.append({
            "content": chunk.page_content,
            "metadata": chunk.metadata,
            "embedding": embedding
        })

    batch_size = 50
    for i in range(0, len(rows), batch_size):
        supabase.table("knowledge_chunks").upsert(
            rows[i:i + batch_size]
        ).execute()
        print(f"  Saved {min(i + batch_size, len(rows))}/{len(rows)} rows to Supabase...")

def run_ingestion():
    knowledge_base_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "knowledge_base"
    )

    print("=" * 50)
    print("MediAssist — Knowledge Base Ingestion")
    print("=" * 50)

    print("\n Step 1: Loading documents...")
    docs = load_documents(knowledge_base_path)

    if not docs:
        print("\n No documents found! Add .md or .pdf files to the knowledge_base folder first.")
        return

    print("\n Step 2: Chunking documents...")
    chunks = chunk_documents(docs)

    print("\n Step 3: Creating embeddings...")
    embeddings = embed_chunks(chunks)

    print("\n Step 4: Saving to Supabase...")
    upsert_to_supabase(chunks, embeddings)

    print("\n" + "=" * 50)
    print("Ingestion complete!")
    print(f"Total chunks stored: {len(chunks)}")
    print("=" * 50)

if __name__ == "__main__":
    run_ingestion()
