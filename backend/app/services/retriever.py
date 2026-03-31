import os
from supabase import create_client
from dotenv import load_dotenv
from app.services.embeddings import embed_text

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> list[dict]:
    """
    Takes a user question, converts it to a vector,
    then finds the most similar chunks in the database.
    """
    query_embedding = embed_text(query)

    result = supabase.rpc("match_knowledge_chunks", {
        "query_embedding": query_embedding,
        "match_threshold": 0.0,
        "match_count": top_k
    }).execute()

    return result.data if result.data else []

def format_context(chunks: list[dict]) -> tuple[str, list[str]]:
    """
    Formats retrieved chunks into a readable context block.
    """
    if not chunks:
        return "No relevant information found.", []

    context_parts = []
    sources = []

    for i, chunk in enumerate(chunks, 1):
        metadata = chunk.get("metadata", {})
        source = metadata.get("source", "unknown")
        category = metadata.get("category", "general")
        similarity = chunk.get("similarity", 0)

        context_parts.append(
            f"[Source {i}: {category}/{source} — relevance: {similarity:.0%}]\n"
            f"{chunk['content']}"
        )
        sources.append(f"{category}/{source}")

    return "\n\n---\n\n".join(context_parts), sources