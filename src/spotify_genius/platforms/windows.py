import ctypes
import win32gui
import win32process
import psutil


GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible


def _get_spotify_pids():
    spotify_pids = []

    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] and "Spotify.exe" in proc.info["name"]:
                spotify_pids.append(proc.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return spotify_pids


def _get_hwnds_for_pid(pid):
    hwnds = []

    def callback(hwnd, _):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            hwnds.append(hwnd)
        return True

    win32gui.EnumWindows(callback, None)
    return hwnds


def _get_window_title(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value


def get_current_song():
    """
    Returns (artist, title) if Spotify is playing.
    Returns (None, None) otherwise.
    """

    pids = _get_spotify_pids()

    for pid in pids:
        hwnds = _get_hwnds_for_pid(pid)

        for hwnd in hwnds:
            if IsWindowVisible(hwnd):
                title = _get_window_title(hwnd)

                if " - " not in title:
                    continue

                parts = title.split(" - ")

                if len(parts) != 2:
                    continue

                artist, song = parts
                return artist.strip(), song.strip()

    return None, None