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
    os.system(f"start \"\" https://genius.com/{artist}-{song_title}-lyrics")
    
    
def replace_all(str, strs_to_replace, replacement):
    for old_value in strs_to_replace:
        str = str.replace(old_value, replacement)
    return str

    
def replace_with_hyphen(str):
    rep_with_hyphen = ['(', ')', ' ', '--']
    rep_with_empty = [',', '\'', '\"', '*', '\\', '/', '?', ':', '.', '$', '!']

    str = replace_all(str, rep_with_empty, '')
    str = replace_all(str, rep_with_hyphen, '-')
    str = str.replace('&', 'and')
    
    str = str.rstrip('-').lstrip('-')
    
    return str


def remove_features(title_song):
    if '(feat' in title_song:
        return title_song.split('(feat')[0]
    
    if '(with' in title_song:
        return title_song.split('(with')[0]
    return title_song


if __name__ == '__main__':
    while True:     
        spotify_handle = get_spotify_handle()
        window_title = get_window_title_by_handle(spotify_handle)
        
        window_title = unidecode(window_title).lower()
        
        artist_song_title = window_title.split(' - ')

        if len(artist_song_title) != 2:
            continue
        try:    
            if artist_song_title != previous_artist_song_title:
                print(f'Song playing: {artist_song_title[0]} - {artist_song_title[1]}\n')
                previous_artist_song_title = artist_song_title
                
                artist = replace_with_hyphen(artist_song_title[0])
                song_title = remove_features(artist_song_title[1])
                song_title = replace_with_hyphen(song_title)

                open_genius_website(artist, song_title)
        except Exception as error:
            print(f'Error when trying to open genius website for song: {artist_song_title}')
            print(f'{error}\n')