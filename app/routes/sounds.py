from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.config import ALLOWED_EXT
from app.models import PlayRequest, DeleteRequest, RenameRequest
from app.services import sound_library as lib
from app.services.player import player

router = APIRouter(prefix="/api", tags=["sounds"])

_mic_target: str | None = None


def set_mic_target(target: str | None):
    global _mic_target
    _mic_target = target


@router.get("/sounds")
def list_sounds():
    return lib.list_sounds()


@router.post("/play")
def play(req: PlayRequest):
    path = lib.resolve(req.file)
    if not path:
        raise HTTPException(404, "not found")
    player.play(str(path), mic_target=_mic_target)
    return {"status": "playing", "file": req.file}


@router.post("/stop")
def stop():
    player.stop()
    return {"status": "stopped"}


@router.post("/upload")
async def upload(file: UploadFile = File(...), name: str = Form("")):
    if not file.filename:
        raise HTTPException(400, "empty filename")
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"format not supported: {ext}")
    data = await file.read()
    result = lib.add(file.filename, data, custom_name=name)
    return {"status": "uploaded", "file": result}


@router.post("/delete")
def delete(req: DeleteRequest):
    if not lib.delete(req.file):
        raise HTTPException(404, "not found")
    return {"status": "deleted"}


@router.post("/rename")
def rename(req: RenameRequest):
    if not req.name.strip():
        raise HTTPException(400, "empty name")
    result = lib.rename(req.file, req.name)
    if result is None:
        raise HTTPException(409, "name taken or not found")
    return {"status": "renamed", "file": result}
