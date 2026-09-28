import json
import logging
from pathlib import Path

log = logging.getLogger("soundpad")

# ⣰⣒⣦⣶⣮⢵⣾⡶⣼⣷⣾⣶⣧⣾⣴⡻⠷⣻⣱⢀⠀⠀⢦⢳⣜⣶⣽⣾⣷⣿
# ⣿⡿⢋⠉⠩⡑⢮⢿⣿⣿⣿⣿⣿⣿⣿⢈⢤⠀⠘⠨⠄⠐⠀⢏⣿⣿⣿⣿⣿⣿
# ⡟⣐⣅⣚⣄⠀⠆⢯⣿⣿⣿⣟⠿⠛⠛⠛⠀⡈⠄⠠⠐⢀⠂⢹⣼⣿⣿⣿⣿⣿
# ⣿⣾⣤⣿⣹⣷⢰⠈⠺⠟⠉⢀⠂⣁⠂⡐⠁⠀⠀⠀⠁⠂⠠⠘⠑⠿⣿⣿⣿⣿
# ⣿⣯⣿⣟⣟⢿⡜⣥⠂⠠⠈⡄⣢⣆⠒⡀⢀⠀⠀⠀⠀⠈⠀⠂⠄⡀⠈⡻⣿⣿
# ⣿⣯⣿⡽⣟⣻⣧⣇⣆⡁⢆⣹⠿⡱⢈⠐⠀⣈⣀⡀⠀⠀⠌⠐⠀⠀⠀⠰⠹⣿
# ⣿⡝⣾⣿⡵⡿⣺⢸⢽⢜⡠⠌⠡⢀⠡⢈⣞⠉⢻⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⣿
# ⣿⣏⠅⢟⡷⣣⠃⡛⠞⡠⠂⠌⠐⡀⠂⢸⣄⣀⣼⣿⣿⡆⠤⠈⢹⣷⡀⠀⠡⢸
# ⣿⣿⣌⢌⠙⢇⣀⠗⠈⠄⡁⠂⡁⠐⢈⠨⠙⠿⣿⠿⣋⠀⣦⣤⣾⣿⠔⠀⢁⢸
# ⣿⣿⣽⣮⡒⢃⠄⠀⢁⠂⠄⡁⠠⢈⠀⠀⠢⣼⣶⣿⣿⣷⠈⠙⠋⠉⠀⢀⠂⢸
# ⣿⣿⣿⣿⣿⣷⢠⠈⠄⡈⠄⠠⢁⠀⢂⠘⠀⠀⠙⠻⢿⣿⡇⡠⠀⠐⠈⡀⠄⣻
# ⣿⣿⣿⣿⣿⣿⣳⡀⠂⠄⠂⢁⠠⠈⡴⣾⡄⠀⢀⠀⠀⠈⢁⠁⠠⠈⡐⠠⢎⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣕⢬⡐⢀⢢⠉⡑⢫⢅⠳⢤⡤⠀⠈⠤⢘⢠⡁⢤⣵⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣥⣋⡔⠨⠐⡁⢂⠰⢀⠠⢀⡉⠔⣬⣪⣶⣿⣿⣿⣿
# ⣿⣿⣿⣿⠿⡟⢟⠛⢫⢏⢡⠃⠤⠡⡅⡐⠀⡀⠀⢀⡀⠄⡠⢄⣉⠛⣾⣻⢿⣿

BASE_DIR = Path(__file__).parent.parent
SOUNDS_DIR = BASE_DIR / "sounds"
STATIC_DIR = BASE_DIR / "static"
CONFIG_PATH = BASE_DIR / "config.json"
PID_FILE = BASE_DIR / ".soundpad.pid"
LOG_FILE = BASE_DIR / "soundpad.log"

ALLOWED_EXT = frozenset({".mp3", ".wav", ".ogg", ".flac", ".opus", ".m4a"})

DEFAULT_CONFIG: dict = {
    "volume": 0.8,
    "play_to_speakers": True,
    "mic_mode": False,
    "accent_color": "#39ff14",
    "hotkeys": {},
    "tray_mode": False,
}


def init_dirs():
    SOUNDS_DIR.mkdir(exist_ok=True)


def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                saved = json.load(f)
            return {**DEFAULT_CONFIG, **saved}
        except (json.JSONDecodeError, OSError) as e:
            log.warning("config corrupt, using defaults: %s", e)
    return dict(DEFAULT_CONFIG)


def save_config(cfg: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def init_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    save_config(cfg)
    return cfg


# singleton config — loaded once, mutated in place
state: dict = {}


def get() -> dict:
    if not state:
        state.update(load_config())
    return state


def update(patch: dict) -> dict:
    cfg = get()
    cfg.update(patch)
    save_config(cfg)
    return cfg
