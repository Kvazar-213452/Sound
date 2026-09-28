"""PipeWire/PulseAudio mic mixing (Linux only).

Creates a virtual sink that mixes the real mic with soundpad output,
then redirects all apps to use it as their source.
"""

import json
import logging
import subprocess
import threading
import time

log = logging.getLogger("soundpad.mic")

SINK = "soundpad_sink"
VMIC = "soundpad_mic"


def _pactl(*args: str) -> str:
    return subprocess.run(
        ["pactl", *args], check=True, capture_output=True, text=True,
    ).stdout.strip()


def _pactl_json(*args: str) -> list:
    return json.loads(_pactl("-f", "json", *args) or "[]")


def _source_index(name: str) -> int | None:
    for s in _pactl_json("list", "sources"):
        if s["name"] == name:
            return s["index"]
    return None


class MicMixer:
    def __init__(self):
        self.real_mic = _pactl("get-default-source")
        self._modules: list[str] = []
        self._moved: set[int] = set()
        self._running = True
        self._loopback = ""
        self._real_idx: int | None = None

    @property
    def sink_name(self) -> str:
        return SINK

    def setup(self):
        log.info("setting up mic mixer, real mic: %s", self.real_mic)

        self._modules.append(
            _pactl("load-module", "module-null-sink", f"sink_name={SINK}",
                   "sink_properties=device.description=Soundpad_Mix")
        )
        self._loopback = _pactl(
            "load-module", "module-loopback", f"source={self.real_mic}",
            f"sink={SINK}", "latency_msec=20",
        )
        self._modules.append(self._loopback)
        self._modules.append(
            _pactl("load-module", "module-remap-source", f"master={SINK}.monitor",
                   f"source_name={VMIC}",
                   "source_properties=device.description=Soundpad_Mic")
        )
        _pactl("set-default-source", VMIC)
        self._real_idx = _source_index(self.real_mic)
        self._redirect()
        threading.Thread(target=self._watch, daemon=True).start()
        log.info("mic mixer ready")

    def _redirect(self):
        for so in _pactl_json("list", "source-outputs"):
            if so.get("source") != self._real_idx:
                continue
            if str(so.get("owner_module")) == self._loopback:
                continue
            try:
                _pactl("move-source-output", str(so["index"]), VMIC)
                self._moved.add(so["index"])
                log.debug("redirected source-output %d", so["index"])
            except subprocess.CalledProcessError:
                pass

    def _watch(self):
        while self._running:
            try:
                self._redirect()
            except Exception:
                pass
            time.sleep(1)

    def cleanup(self):
        log.info("cleaning up mic mixer")
        self._running = False
        for idx in self._moved:
            try:
                _pactl("move-source-output", str(idx), self.real_mic)
            except subprocess.CalledProcessError:
                pass
        try:
            _pactl("set-default-source", self.real_mic)
        except subprocess.CalledProcessError:
            pass
        for m in reversed(self._modules):
            try:
                _pactl("unload-module", m)
            except subprocess.CalledProcessError:
                pass
