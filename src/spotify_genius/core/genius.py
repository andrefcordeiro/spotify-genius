import webbrowser


def open_genius(artist: str, title: str):
    url = f"https://genius.com/{artist}-{title}-lyrics"
    webbrowser.open(url)