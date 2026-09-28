from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.tts import speak

router = APIRouter(prefix="/api", tags=["tts"])


class TtsRequest(BaseModel):
    text: str
    lang: str = "en"


@router.post("/tts")
def tts(req: TtsRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(400, "empty text")
    if len(text) > 5000:
        raise HTTPException(400, "text too long (max 5000 chars)")
    try:
        speak(text, req.lang)
    except Exception as e:
        raise HTTPException(500, f"TTS error: {e}")
    return {"status": "speaking"}
