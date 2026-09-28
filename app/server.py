import logging
import os
import signal
import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR, SOUNDS_DIR
from app.routes import sounds, config_routes, tts_routes
from app.services.player import player
from app.services.daemon import remove_pid

log = logging.getLogger("soundpad.server")

_cleanup_hooks: list = []


def add_cleanup(fn):
    _cleanup_hooks.append(fn)


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    log.info("server starting")
    yield
    log.info("server shutting down")
    player.stop()
    for hook in _cleanup_hooks:
        try:
            hook()
        except Exception as e:
            log.warning("cleanup error: %s", e)
    remove_pid()


def create_app() -> FastAPI:
    app = FastAPI(title="Soundpad", lifespan=_lifespan)

    app.include_router(sounds.router)
    app.include_router(config_routes.router)
    app.include_router(tts_routes.router)

    @app.post("/api/shutdown")
    def shutdown():
        log.info("shutdown requested via API")
        threading.Thread(target=lambda: (os.kill(os.getpid(), signal.SIGTERM)), daemon=True).start()
        return {"status": "shutting down"}

    @app.get("/sounds/{filename:path}")
    def serve_sound(filename: str):
        path = SOUNDS_DIR / filename
        if not path.exists():
            from fastapi import HTTPException
            raise HTTPException(404)
        return FileResponse(path)

    if STATIC_DIR.exists() and (STATIC_DIR / "index.html").exists():
        assets_dir = STATIC_DIR / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        @app.get("/{full_path:path}")
        def serve_spa(full_path: str):
            file_path = STATIC_DIR / full_path
            if full_path and file_path.exists() and file_path.is_file():
                return FileResponse(file_path)
            return FileResponse(STATIC_DIR / "index.html")

    return app
