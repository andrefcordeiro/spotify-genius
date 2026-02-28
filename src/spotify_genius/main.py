import time
from spotify_genius.platforms import get_current_song
from spotify_genius.core import (
    normalize,
    replace_with_hyphen,
    remove_features,
    open_genius,
)


def run():
    previous = None

    while True:
        artist, title = get_current_song()

        if not artist or not title:
            time.sleep(2)
            continue

        artist = normalize(artist)
        title = normalize(title)

        current = (artist, title)

        if current != previous:
            previous = current

            artist_clean = replace_with_hyphen(artist)
            title_clean = replace_with_hyphen(remove_features(title))

            open_genius(artist_clean, title_clean)

        time.sleep(2)