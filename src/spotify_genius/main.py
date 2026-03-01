import time
from spotify_genius.platforms import get_current_song
from spotify_genius.core import open_genius

def run():
    print('Waiting for tracks...')
    previous = None

    while True:
        artist, title = get_current_song()

        if not artist or not title:
            time.sleep(2)
            continue

        current = (artist, title)

        if current != previous:
            previous = current
            print(f'\nNow playing: {artist} - {title}')

            open_genius(artist, title)

        time.sleep(2)

if __name__ == "__main__":
    run()