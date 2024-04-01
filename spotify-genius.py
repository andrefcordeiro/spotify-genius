import win32gui
import win32process
import psutil
import ctypes
import os
from unidecode import unidecode

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

previous_artist_song_title = None

def get_process_id_by_name():
    spotify_pids = []
    process_name = "Spotify.exe"

    for proc in psutil.process_iter():
        if process_name in proc.name():
            spotify_pids.append(proc.pid)

    return spotify_pids

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        #if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds 

def get_window_title_by_handle(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def get_spotify_handle():
    pids = get_process_id_by_name()
    
    for i in pids:
        hwnds = get_hwnds_for_pid(i)
        for hwnd in hwnds:
            if IsWindowVisible(hwnd):
                return hwnd

def open_genius_website(artist, song_title):
    print(f'Song playing: {artist} - {song_title}\n')
    
    os.system(f"start \"\" https://genius.com/{artist}-{song_title}-lyrics")
    
    
def replace_with_hyphen(str):
    str = str.replace('(', '-').replace(')', '-').replace(' ', '-')
    
    print(str)
    return str

if __name__ == '__main__':
    while True:     
        spotify_handle = get_spotify_handle()
        window_title = get_window_title_by_handle(spotify_handle)
        
        window_title = unidecode(window_title)
        
        artist_song_title = window_title.split(' - ')
        
        try:    
            if artist_song_title != previous_artist_song_title:
                previous_artist_song_title = artist_song_title
                
                artist = replace_with_hyphen(artist_song_title[0])
                song_title = replace_with_hyphen(artist_song_title[1])

                open_genius_website(artist, song_title)
        except:
            print(f'Error when trying to open genius website for song: {artist_song_title}')