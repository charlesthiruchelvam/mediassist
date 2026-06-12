cd ~/Desktop/mediassist
cat > README.md << 'EOF'
#  MediAssist — AI-Powered Healthcare Knowledge Assistant

A RAG-based healthcare assistant that answers patient and staff queries by retrieving answers from a curated medical knowledge base — covering drug information, symptom guides, hospital policies, and appointment workflows.

##  Live Demo
**[https://mediassist-two.vercel.app](https://mediassist-two.vercel.app)**

## ✨ Features
- **RAG Pipeline** — retrieves relevant knowledge before answering, preventing hallucination
- **20 Knowledge Base Documents** — drugs, symptoms, hospital policies, appointment workflows
- **Emergency Detection** — automatically detects emergency keywords and directs to emergency services
- **Streaming Responses** — real-time token-by-token response display
- **Source Citations** — every answer shows which document it came from with a relevance score
- **Hybrid Mode** — knowledge base first, general medical knowledge as fallback

##  Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16, TypeScript, Tailwind CSS |
| Backend | Python FastAPI, async streaming |
| AI Model | Groq API (Llama 3.1 8B Instant) |
| Vector DB | Supabase (PostgreSQL + pgvector) |
| Embeddings | N-gram semantic embeddings (384 dims) |
| Deployment | Vercel (frontend) + Railway (backend) |

##  Architecture
```
User Question
     ↓
Emergency Check → Emergency Response (if triggered)
     ↓
Query Embedding (n-gram vectorization)
     ↓
Supabase Vector Search (cosine similarity, top 5 chunks)
     ↓
Context Assembly (with source citations)
     ↓
Groq LLM Generation (streaming)
     ↓
Streamed Response to UI
```

##  Running Locally

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase account (free)
- Groq API key (free)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
uvicorn app.main:app --reload --port 8000
```

### Knowledge Base Ingestion
```bash
cd backend
python -m ingestion.ingest
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local  # Add NEXT_PUBLIC_API_URL
npm run dev
```

##  Project Structure
```
mediassist/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── routers/chat.py      # Chat endpoint
│   │   └── services/
│   │       ├── rag.py           # RAG pipeline
│   │       ├── embeddings.py    # Vector embeddings
│   │       └── retriever.py     # Supabase search
│   ├── ingestion/               # Document ingestion
│   └── knowledge_base/          # 20 medical documents
└── frontend/
    └── app/
        └── page.tsx             # Chat UI
```

##  License
MIT License — feel free to use and adapt for your own healthcare projects.

---
Built with ❤️ using FastAPI, Next.js, Groq, and Supabase.
EOF
