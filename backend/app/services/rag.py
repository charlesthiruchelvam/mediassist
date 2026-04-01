import os
from groq import Groq
from dotenv import load_dotenv
from app.services.retriever import retrieve_relevant_chunks, format_context
from typing import Generator

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are MediAssist, a helpful healthcare knowledge assistant 
for patients and hospital staff.

HOW TO ANSWER:
1. If the knowledge base context below contains relevant information, 
   use it to answer and cite the source.
2. If the context is not relevant or empty, use your general medical 
   knowledge to give a helpful, accurate answer.
3. Always clarify when you are answering from general knowledge vs 
   the hospital knowledge base.
4. Never diagnose medical conditions definitively.
5. Always recommend professional consultation for serious symptoms.
6. For ANY emergency symptoms — chest pain, difficulty breathing, 
   loss of consciousness — immediately say:
   This sounds like a medical emergency. Call 1990 immediately.
7. Be clear, empathetic, and concise."""

EMERGENCY_KEYWORDS = [
    "chest pain", "can't breathe", "cannot breathe", "difficulty breathing",
    "unconscious", "not breathing", "heart attack", "stroke", "overdose",
    "severe bleeding", "suicide", "poisoning", "seizure"
]

def check_emergency(query: str) -> str | None:
    """Check if query contains emergency keywords."""
    query_lower = query.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in query_lower:
            return (
                "⚠️ This sounds like a medical emergency.\n\n"
                "Call 1990 immediately or go to the nearest "
                "emergency room. Do not wait for an online response.\n\n"
                "If you are in Sri Lanka: Accident Service — 011 269 1111"
            )
    return None

def stream_rag_response(
    query: str,
    history: list[dict]
) -> Generator[str, None, None]:
    """
    Full RAG pipeline using Groq (free):
    1. Check for emergencies first
    2. Retrieve relevant chunks from vector DB
    3. Build augmented prompt
    4. Stream Groq's response
    """

    # Step 1: Emergency check
    emergency = check_emergency(query)
    if emergency:
        yield emergency
        return

    # Step 2: Retrieve relevant chunks
    chunks = retrieve_relevant_chunks(query, top_k=5)
    context, sources = format_context(chunks)

    # Step 3: Build augmented prompt
    augmented_message = f"""Hospital knowledge base context (use this first if relevant):
{context}

---

User question: {query}

If the context above is relevant, use it and cite the source.
If not relevant, answer from your general medical knowledge and 
say 'Based on general medical knowledge:'"""

    # Step 4: Build messages with history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-6:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    messages.append({"role": "user", "content": augmented_message})

    # Step 5: Stream from Groq (using Llama 3 — free and powerful)
    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=1024,
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta