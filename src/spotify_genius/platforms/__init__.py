import platform

if platform.system() == "Windows":
    from .windows import get_current_song
elif platform.system() == "Linux":
    from .linux import get_current_song
else:
    raise RuntimeError("Unsupported operating system")

__all__ = ["get_current_song"]