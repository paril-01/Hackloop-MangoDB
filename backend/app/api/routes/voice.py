from fastapi import APIRouter

router = APIRouter(prefix="/api/voice", tags=["voice"])

@router.post("/transcribe")
async def transcribe_stub():
    # Placeholder for voice transcription endpoint
    return {"text": "transcription not implemented in scaffold"}
