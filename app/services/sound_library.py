import logging
import uuid
from pathlib import Path

from app.config import SOUNDS_DIR, ALLOWED_EXT

log = logging.getLogger("soundpad.library")


def list_sounds() -> list[dict]:
    result = []
    for f in sorted(SOUNDS_DIR.iterdir()):
        if f.suffix.lower() in ALLOWED_EXT:
            result.append({
                "id": f.stem,
                "name": f.stem,
                "file": f.name,
                "ext": f.suffix.lower(),
            })
    return result


def resolve(filename: str) -> Path | None:
    path = SOUNDS_DIR / filename
    if path.exists() and path.is_file() and path.resolve().parent == SOUNDS_DIR.resolve():
        return path
    return None


def safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_ " else "_" for c in name)


def add(filename: str, data: bytes, custom_name: str = "") -> str:
    ext = Path(filename).suffix.lower()
    stem = custom_name.strip() or Path(filename).stem
    name = safe_name(stem)
    dest = SOUNDS_DIR / f"{name}{ext}"
    if dest.exists():
        name = f"{name}_{uuid.uuid4().hex[:6]}"
        dest = SOUNDS_DIR / f"{name}{ext}"
    dest.write_bytes(data)
    log.info("added sound: %s", dest.name)
    return dest.name


def delete(filename: str) -> bool:
    path = resolve(filename)
    if not path:
        return False
    path.unlink()
    log.info("deleted sound: %s", filename)
    return True


def rename(filename: str, new_name: str) -> str | None:
    path = resolve(filename)
    if not path:
        return None
    sname = safe_name(new_name.strip())
    new_path = SOUNDS_DIR / f"{sname}{path.suffix}"
    if new_path.exists() and new_path != path:
        return None
    path.rename(new_path)
    log.info("renamed %s → %s", filename, new_path.name)
    return new_path.name
