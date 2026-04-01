from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat

app = FastAPI(
    title="MediAssist API",
    description="RAG-based healthcare knowledge assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mediassist-two.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Pre-load the embedding model at startup."""
    from app.services.embeddings import _model
    print(f"Embedding model ready: {_model}")

@app.get("/")
def root():
    return {"message": "MediAssist API is running"}