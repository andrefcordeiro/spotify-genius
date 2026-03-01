# Spotify/Genius Automation

This python script works as a listener to the music that is being played on the user's Spotify Desktop App for Windows.

The program gets the information of the currently playing song (artist and title) and automatically opens its respective page on Genius website, so the user can keep track of the song lyrics, besides taking advantage of other tools available on the website.

## Install as pip package

```
pip install spotify-genius
```

## How to download

Go to [releases](https://github.com/andrefcordeiro/spotify-genius-automation/releases) and download the latest version.

## Hot to run by yourself

### Requirements

- Python >=3.10

### Steps

1. Install dependencies

```
pip install .
```

2. Run

```
spotify-genius
```

## How to generate the windows .exe

### Requirements

- Python >=3.10

### Steps

1. Install [PyInstaller](https://pyinstaller.org/en/stable/).

```
pip install pyinstaller
```

2. In the root folder of the project, run

```
pyinstaller --onefile --icon=assets/spotify-genius.ico --name spotify-genius-win spotify-genius.py
```

The binary `spotify-genius.exe` will be created in `dist`.

## How to generate linux executable

### Requirements

- Python >=3.10

### Steps

1. Install [PyInstaller](https://pyinstaller.org/en/stable/).

```
pip install pyinstaller
```

2. In the root folder of the project, run

```
pyinstaller --onefile --name spotify-genius-linux src/spotify_genius/main.py
```
