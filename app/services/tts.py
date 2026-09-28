import logging
import tempfile
from pathlib import Path

from gtts import gTTS

from app.config import BASE_DIR
from app.services.player import player

log = logging.getLogger("soundpad.tts")

TTS_DIR = BASE_DIR / ".tts_cache"


def speak(text: str, lang: str = "en"):
    TTS_DIR.mkdir(exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", dir=TTS_DIR, delete=False)
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(tmp.name)
        log.info("tts generated: %s chars, lang=%s", len(text), lang)
        player.play(tmp.name)
    except Exception as e:
        log.error("tts failed: %s", e)
        Path(tmp.name).unlink(missing_ok=True)
        raise
