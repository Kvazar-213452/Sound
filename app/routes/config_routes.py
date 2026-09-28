from fastapi import APIRouter

from app import config as cfg
from app.models import ConfigUpdate

router = APIRouter(prefix="/api", tags=["config"])

# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠐⢚⣿⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣷⣻⡑⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠚⣾⣿⣾⣧⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣷⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠘⣹⣷⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣷⣿⡿⣿⡿⡚⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⢳⣿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣤⣶⣶⣶⣶⣦⣶⣶⣶⣶⣦⣿⣿⣻⣿⣿⣿⣷⣇⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠸⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠿⠟⠿⢿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣟⡁⠀⡀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠁⢀⠀⠀⠀⢹⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⢀⠀⠀⠀⠀⠀⢼⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣮⣀⣤⣠⣀⡤⢾⣿⣿⣿⣿⣿⣿⣿⡿⢀⣔⣀⣀⣠⣴⣾⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠠⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠠⣿⣿⢿⡯⣜⠻⣿⣿⣿⣿⣿⣿⡟⠙⢿⠿⢿⡟⠋⠙⣹⣿⣿⣿⣿⣿⣿⢣⠕⡾⢿⡧⣗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⢻⣯⡝⣙⡊⠵⢛⣿⣿⣿⣿⣿⣿⣦⡀⠁⠀⠀⣤⣾⣿⣿⣿⣿⣿⣯⡜⢃⣞⣑⠻⣇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⣨⣿⣿⡷⣍⣉⢺⣿⣿⣿⣿⣿⣿⣿⠷⡄⢀⠾⢿⢿⢿⢿⢿⡿⠾⡜⣓⣊⢤⡤⢿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⣀⣤⣼⣿⣿⣿⣿⣿⣿⣦⢰⡱⠲⠞⠡⠼⡉⠒⠁⠀⠒⠈⠎⠢⠊⠑⣋⠋⢀⢅⣴⣟⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⢀⣤⣿⣿⣿⣿⣿⣿⣿⣼⡻⢿⣿⢿⡀⠜⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⡘⢼⠿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣅⢫⢉⡀⠀⠀⠠⠀⠠⠠⡀⢠⡀⠀⠀⠀⠀⠀⢈⡸⣮⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣯⢷⣢⢆⡀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⡠⢐⢮⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡀⠀⠀⠀⠀⠀⠀
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣤⡰⣀⠀⠀⠀⠀⠀⡀⢀⣄⣡⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠀⠀⠀⠀

@router.get("/config")
def get_config():
    return cfg.get()


@router.post("/config")
def set_config(update: ConfigUpdate):
    conf = cfg.get()
    if update.volume is not None:
        conf["volume"] = max(0.0, min(2.0, update.volume))
    if update.play_to_speakers is not None:
        conf["play_to_speakers"] = update.play_to_speakers
    if update.mic_mode is not None:
        conf["mic_mode"] = update.mic_mode
    if update.accent_color is not None:
        c = update.accent_color.strip()
        if c.startswith("#") and len(c) in (4, 7):
            conf["accent_color"] = c
    if update.hotkeys is not None:
        conf["hotkeys"] = update.hotkeys
    if update.tray_mode is not None:
        conf["tray_mode"] = update.tray_mode
    cfg.save_config(conf)
    return conf
