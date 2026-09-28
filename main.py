#!/usr/bin/env python3
"""
Soundpad — cross-platform soundboard with web UI.

  python main.py                # http://localhost:5000
  python main.py --port 8080    # custom port
  python main.py --mic          # mic mixing (Linux/PipeWire)
  python main.py --tray         # background mode (no console)
  python main.py --stop         # stop background process
  python main.py --status       # check status
  python main.py --dev          # verbose logging
  python main.py --init         # create config.json and directories
"""

import argparse
import logging
import platform
import signal
import sys

log = logging.getLogger("soundpad")

# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣛⡻⣿⣿⣿⣿⣿
# ⠋⡩⠌⣍⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣶⣿⣿⣷⠘⣿⣿⣿⣿
# ⠀⢈⡓⠴⣌⡀⢍⡻⢿⣿⡿⠟⡋⠉⣭⣭⣭⣭⣐⣫⣿⣿⣿⣿⠂⣿⣿⣿⣿
# ⠀⠢⠜⡡⠙⡽⣢⠈⣁⢀⢀⣡⡶⠿⢿⣿⣿⣿⣿⣿⣉⣉⠛⠻⠄⢽⣿⣿⣿
# ⡆⢰⡀⠃⠆⣥⢛⡤⢫⡜⠞⠋⣁⣤⣾⣿⠿⠭⠉⠉⠙⠻⢶⣶⣦⣎⠻⣿⣿
# ⣿⡌⢗⣌⡔⢠⠩⡜⠁⢰⣾⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⣿⣧⢹⣿
# ⣿⣿⣄⠋⠧⢌⠓⠀⢀⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠙⣦⢻
# ⣿⣿⣿⡀⠀⠀⠀⠀⣼⢣⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⡿⡌
# ⣿⣿⣿⣧⠀⠀⠀⠐⢬⠣⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢛⢡
# ⣿⣿⣿⣿⣧⠀⠀⠀⢎⡭⣹⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⢃⠏⣼
# ⣿⣿⣿⣿⣿⢠⢤⡘⣬⢖⣧⢫⠖⣡⠀⠄⡀⢀⠀⠀⠀⢀⢀⠂⢆⣉⢂⣴⣿
# ⣿⣿⣿⣿⢃⣾⣣⠟⣜⠾⣌⢧⡛⣤⢋⠖⡰⢂⡌⢄⠣⡐⢌⡘⢤⢂⣾⣿⣿
# ⣿⣿⣿⡏⣼⣟⡯⢶⡹⢶⡹⣌⡳⢍⠞⡰⢃⠌⡡⢘⠠⠡⣌⠱⣌⠸⣿⣿⣿
# ⣿⣿⣿⢠⣿⣞⡽⣳⢏⡷⣹⢮⡝⣎⡳⣍⠦⡩⢔⠣⢌⢣⡐⡹⣜⡆⣿⣿⣿
# ⣿⣿⡟⢸⣿⡾⣽⢧⣻⡼⣳⢧⡝⣮⢳⡱⢎⡱⢊⡕⣊⠦⣑⡳⣜⡇⢹⣿⣿
# ⣿⣿⡇⢽⡿⣽⢯⣟⡷⣽⣣⣟⣼⣡⢧⣙⢢⡱⣩⢒⢥⢚⡤⢓⡬⢿⣼⣿⣿

def setup_logging(dev: bool = False):
    level = logging.DEBUG if dev else logging.INFO
    fmt = "%(asctime)s [%(name)s] %(levelname)s: %(message)s" if dev else "[%(levelname)s] %(message)s"
    logging.basicConfig(level=level, format=fmt, stream=sys.stderr)
    if not dev:
        logging.getLogger("uvicorn").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def cmd_init():
    from app.config import init_config, init_dirs, SOUNDS_DIR, CONFIG_PATH
    init_dirs()
    cfg = init_config()
    print(f"[init] config  → {CONFIG_PATH}")
    print(f"[init] sounds  → {SOUNDS_DIR}/")
    print(f"[init] volume: {cfg['volume']}, accent: {cfg['accent_color']}")
    print("[init] done")


def cmd_status():
    from app.services.daemon import is_running
    running, pid = is_running()
    if running:
        print(f"[tray] running (pid {pid})")
    else:
        print("[tray] not running")


def cmd_stop():
    from app.services.daemon import stop_daemon
    stop_daemon()


def cmd_run(args):
    from app import config as cfg
    from app.config import init_dirs
    from app.server import create_app, add_cleanup
    from app.services.player import player
    from app.services.daemon import daemonize, write_pid, remove_pid

    init_dirs()
    conf = cfg.get()

    if args.mic:
        conf["mic_mode"] = True
        cfg.save_config(conf)

    use_tray = args.tray or conf.get("tray_mode", False)

    mic_mixer = None
    mic_target = None

    if conf["mic_mode"] and platform.system() == "Linux":
        try:
            from app.services.mic_mixer import MicMixer
            mic_mixer = MicMixer()
            mic_mixer.setup()
            mic_target = mic_mixer.sink_name
            log.info("mic mixer active, sink: %s", mic_target)
            if not use_tray:
                print("[MIC] microphone connected")
        except Exception as e:
            log.warning("mic mixer failed: %s", e)
            if not use_tray:
                print(f"[MIC] error: {e}")
    elif conf["mic_mode"]:
        log.warning("mic_mode is Linux-only (PipeWire), skipping")

    from app.routes.sounds import set_mic_target
    set_mic_target(mic_target)

    if mic_mixer:
        add_cleanup(mic_mixer.cleanup)

    def shutdown(_sig, _frame):
        if mic_mixer:
            mic_mixer.cleanup()
        player.stop()
        remove_pid()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    if use_tray:
        addr = f"http://{args.host}:{args.port}"
        print(f"[tray] Soundpad: {addr}")
        daemonize()
        write_pid()
    else:
        addr = f"http://{args.host}:{args.port}"
        print()
        print("  ╔══════════════════════════════════════╗")
        print("  ║         SOUNDPAD v3.0                ║")
        print(f"  ║  {addr:<34s}  ║")
        print(f"  ║  {platform.system():<10s} audio: {player.backend_name:<14s}  ║")
        print("  ╚══════════════════════════════════════╝")
        print()
        write_pid()

    app = create_app()

    import uvicorn
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="debug" if args.dev else ("error" if use_tray else "warning"),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Soundpad — cross-platform soundboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--port", type=int, default=5000, help="server port (default: 5000)")
    parser.add_argument("--host", default="0.0.0.0", help="bind address (default: 0.0.0.0)")
    parser.add_argument("--mic", action="store_true", help="enable mic mixing (Linux/PipeWire)")
    parser.add_argument("--tray", action="store_true", help="run in background (no console)")
    parser.add_argument("--stop", action="store_true", help="stop background process")
    parser.add_argument("--status", action="store_true", help="check if running")
    parser.add_argument("--dev", action="store_true", help="verbose logging")
    parser.add_argument("--init", action="store_true", help="create config.json and directories")
    args = parser.parse_args()

    setup_logging(dev=args.dev)

    if args.init:
        cmd_init()
        return
    if args.stop:
        cmd_stop()
        return
    if args.status:
        cmd_status()
        return

    cmd_run(args)


if __name__ == "__main__":
    main()
