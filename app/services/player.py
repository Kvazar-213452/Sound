"""Cross-platform audio playback.

Picks the best available backend:
  Linux:   pw-play (PipeWire) → paplay (PulseAudio) → ffplay
  macOS:   afplay → ffplay
  Windows: powershell (Media.SoundPlayer) → ffplay
"""

import abc
import logging
import platform
import shutil
import subprocess
import threading

from app import config as cfg

log = logging.getLogger("soundpad.player")

SYSTEM = platform.system()

# ⠀⠀⠀⠀⠀⠀⣀⣀⣤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⣀⡴⠛⠁⢀⡴⢚⣩⠭⠟⠛⠋⠉⠉⠉⠉⠉⠛⠲⢤⡀⠀⠀⠀⠀⠀⠀
# ⠀⠀⡼⠋⠀⠀⢀⡿⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣦⠀⠀⠀⠀⠀
# ⠀⣸⠧⠤⣄⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀
# ⠘⠷⢶⡚⢹⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀
# ⠀⠀⠀⢳⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⣀⣀⣤
# ⠀⠀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣭⣿⣿
# ⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⢉⠥⠐
# ⢀⣀⣠⣤⣴⣾⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠘⢲⣐
# ⣿⣿⣿⣾⡿⠿⠿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣦⡀⠀⠀⠀⣸⠛⠋⠉⠁
# ⠉⡩⠒⠒⠈⢉⡆⠙⣦⠀⠀⠀⠀⠀⢠⠴⠞⠛⠛⠉⠉⢳⣤⡤⠶⡏⠀⠀⠀⠀
# ⠀⠙⣒⣒⣬⡭⠴⠖⠚⢳⡄⠀⢀⣀⡼⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠙⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

class Backend(abc.ABC):
    name: str

    @abc.abstractmethod
    def spawn(self, path: str, volume: float, target: str | None = None) -> subprocess.Popen:
        ...

    def supports_target(self) -> bool:
        return False


class PwPlayBackend(Backend):
    name = "pw-play"

    def spawn(self, path: str, volume: float, target: str | None = None) -> subprocess.Popen:
        cmd = ["pw-play", "--volume", str(volume), path]
        if target:
            cmd = ["pw-play", "--target", target, "--volume", str(volume), path]
        log.debug("exec: %s", cmd)
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def supports_target(self) -> bool:
        return True


class PaplayBackend(Backend):
    name = "paplay"

    def spawn(self, path: str, volume: float, target: str | None = None) -> subprocess.Popen:
        vol_pa = str(int(volume * 65536))
        cmd = ["paplay", f"--volume={vol_pa}", path]
        log.debug("exec: %s", cmd)
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class AfplayBackend(Backend):
    name = "afplay"

    def spawn(self, path: str, volume: float, target: str | None = None) -> subprocess.Popen:
        cmd = ["afplay", "-v", str(volume), path]
        log.debug("exec: %s", cmd)
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class FfplayBackend(Backend):
    name = "ffplay"

    def spawn(self, path: str, volume: float, target: str | None = None) -> subprocess.Popen:
        cmd = ["ffplay", "-nodisp", "-autoexit", "-volume", str(int(volume * 100)), path]
        log.debug("exec: %s", cmd)
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class PowerShellBackend(Backend):
    name = "powershell"

    def spawn(self, path: str, volume: float, target: str | None = None) -> subprocess.Popen:
        ps = f'(New-Object Media.SoundPlayer "{path}").PlaySync()'
        cmd = ["powershell", "-Command", ps]
        log.debug("exec: %s", cmd)
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _detect_backend() -> Backend:
    candidates: list[tuple[str, type[Backend]]] = []

    if SYSTEM == "Linux":
        candidates = [("pw-play", PwPlayBackend), ("paplay", PaplayBackend), ("ffplay", FfplayBackend)]
    elif SYSTEM == "Darwin":
        candidates = [("afplay", AfplayBackend), ("ffplay", FfplayBackend)]
    elif SYSTEM == "Windows":
        candidates = [("powershell", PowerShellBackend), ("ffplay", FfplayBackend)]
    else:
        candidates = [("ffplay", FfplayBackend)]

    for binary, cls in candidates:
        if shutil.which(binary):
            log.info("audio backend: %s", cls.name)
            return cls()

    raise RuntimeError(f"no audio backend found for {SYSTEM}; install pw-play, ffplay, or paplay")


class Player:
    def __init__(self):
        self._backend = _detect_backend()
        self._procs: list[subprocess.Popen] = []
        self._lock = threading.Lock()

    @property
    def backend_name(self) -> str:
        return self._backend.name

    def play(self, path: str, mic_target: str | None = None):
        conf = cfg.get()
        vol = conf["volume"]
        with self._lock:
            self._kill()
            if mic_target and self._backend.supports_target():
                self._procs.append(self._backend.spawn(path, vol, target=mic_target))
            if conf["play_to_speakers"] or not mic_target or not self._backend.supports_target():
                self._procs.append(self._backend.spawn(path, vol))

    def stop(self):
        with self._lock:
            self._kill()

    def _kill(self):
        for p in self._procs:
            if p.poll() is None:
                p.terminate()
        self._procs.clear()


player = Player()
