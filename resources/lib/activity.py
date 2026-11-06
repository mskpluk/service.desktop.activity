"""Report remote control input in Kodi to the desktop as user activity."""

import subprocess
import time

import xbmc

# Seconds between reports while input continues.
INTERVAL = 10
POLL = 0.5

CALL = ["gdbus", "call", "--session", "--dest", "org.freedesktop.ScreenSaver",
        "--object-path", "/ScreenSaver",
        "--method", "org.freedesktop.ScreenSaver.SimulateUserActivity"]


def log(msg, level=xbmc.LOGINFO):
    xbmc.log(f"[service.desktop.activity] {msg}", level)


def report():
    try:
        subprocess.run(CALL, capture_output=True, timeout=5, check=True)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"cannot report activity: {e}", xbmc.LOGWARNING)
        return False
    return True


class Player(xbmc.Player):
    """Play/pause from a phone app does not reset Kodi's idle time."""

    def __init__(self, service):
        super().__init__()
        self.service = service

    def onAVStarted(self):
        self.service.pending = True

    def onPlayBackResumed(self):
        self.service.pending = True


class Service(xbmc.Monitor):
    def __init__(self):
        super().__init__()
        self.player = Player(self)
        self.pending = False

    def run(self):
        if not report():
            log("no desktop screensaver service, service idle")
            return
        log("started")
        last = time.monotonic()
        while not self.waitForAbort(POLL):
            # Kodi resets its idle time on keys, CEC, mouse, EventServer and JSON-RPC input.
            input_seen = not xbmc.getCondVisibility("System.IdleTime(1)")
            if self.pending or (input_seen and time.monotonic() - last >= INTERVAL):
                self.pending = False
                report()
                last = time.monotonic()
