"""Process management — daemonize, PID file, tray mode.

Linux/macOS: double-fork daemon.
Windows: CREATE_NO_WINDOW subprocess (no fork).
"""

import logging
import os
import platform
import signal
import sys

from app.config import PID_FILE

log = logging.getLogger("soundpad.daemon")

SYSTEM = platform.system()


def write_pid():
    PID_FILE.write_text(str(os.getpid()))


def remove_pid():
    PID_FILE.unlink(missing_ok=True)


def is_running() -> tuple[bool, int | None]:
    if not PID_FILE.exists():
        return False, None
    try:
        pid = int(PID_FILE.read_text().strip())
    except (ValueError, OSError):
        PID_FILE.unlink(missing_ok=True)
        return False, None

    if SYSTEM == "Windows":
        import ctypes
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.OpenProcess(0x0400, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return True, pid
        PID_FILE.unlink(missing_ok=True)
        return False, None

    try:
        os.kill(pid, 0)
        return True, pid
    except OSError:
        PID_FILE.unlink(missing_ok=True)
        return False, None


def stop_daemon():
    running, pid = is_running()
    if not running or pid is None:
        print("[tray] not running")
        return

    if SYSTEM == "Windows":
        import ctypes
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.OpenProcess(1, False, pid)
        if handle:
            kernel32.TerminateProcess(handle, 0)
            kernel32.CloseHandle(handle)
    else:
        os.kill(pid, signal.SIGTERM)

    print(f"[tray] stopped (pid {pid})")
    PID_FILE.unlink(missing_ok=True)


def daemonize():
    if SYSTEM == "Windows":
        return

    sys.stdout.flush()
    sys.stderr.flush()
    if os.fork() > 0:
        os._exit(0)
    os.setsid()
    if os.fork() > 0:
        os._exit(0)
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, 0)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    os.close(devnull)
