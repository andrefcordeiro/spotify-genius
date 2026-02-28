import dbus


def get_current_song():
    try:
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object(
            "org.mpris.MediaPlayer2.spotify",
            "/org/mpris/MediaPlayer2"
        )

        interface = dbus.Interface(
            spotify_bus,
            "org.freedesktop.DBus.Properties"
        )

        metadata = interface.Get(
            "org.mpris.MediaPlayer2.Player",
            "Metadata"
        )

        artist = str(metadata["xesam:artist"][0])
        title = str(metadata["xesam:title"])

        return artist, title

    except Exception:
        return None, None