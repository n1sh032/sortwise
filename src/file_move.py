import os


def move_without_overwrite(source, destination):
    """Move a regular file inside Downloads without replacing another file."""
    if source.is_symlink() or not source.is_file():
        raise ValueError("Only regular files can be moved")
    os.link(source, destination)
    try:
        source.unlink()
    except OSError:
        destination.unlink()
