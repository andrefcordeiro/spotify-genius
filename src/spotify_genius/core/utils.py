from unidecode import unidecode

import re

def normalize(text: str) -> str:
    return unidecode(text).lower()

def replace_with_hyphen(text: str) -> str:
    text = text.replace("&", "and")

    # Keep only letters, numbers, and spaces
    text = re.sub(r"[^\w\s-]", "", text)

    # Replace whitespace with hyphen
    text = re.sub(r"\s+", "-", text)

    # Collapse multiple hyphens
    text = re.sub(r"-+", "-", text)

    return text.strip("-")


def remove_features(title_song: str) -> str:
    lower = title_song.lower()

    if '(feat' in lower:
        return title_song[:lower.index('(feat')]

    if '(with' in lower:
        return title_song[:lower.index('(with')]

    return title_song