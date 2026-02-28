import re
from unidecode import unidecode

import webbrowser


def remove_features(title_song: str) -> str:
    return re.sub(
        r"\s*\((feat|ft|with)[^)]*\)",
        "",
        title_song,
        flags=re.IGNORECASE
    ).strip()


def generate_genius_slug(artist: str, title: str) -> str:
    title = remove_features(title)

    text = f"{artist} {title}"
    
    text = text.replace("'", "")

    text = text.replace('"', "")
    
    text = text.replace("&", "and")

    text = unidecode(text)

    # Replace non-alphanumeric with hyphen
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text)

    # Collapse multiple hyphens
    text = re.sub(r"-+", "-", text)

    return text.strip("-") + "-lyrics"


def open_genius(artist: str, title: str):
    url = f"https://genius.com/{generate_genius_slug(artist, title)}"
    print(f'Opening {url}')
    webbrowser.open(url)