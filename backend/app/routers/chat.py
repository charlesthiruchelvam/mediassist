from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.services.rag import stream_rag_response
import json

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Main chat endpoint. Returns a streaming response
    so the UI can show text as it's generated.
    """
    def generate():
        try:
            for chunk in stream_rag_response(
                request.message,
                [msg.dict() for msg in request.history]
            ):
                yield f"data: {json.dumps({'text': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"}
    )

@router.get("/health")
async def health():
    return {"status": "ok", "service": "MediAssist API"}