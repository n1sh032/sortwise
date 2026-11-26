from pathlib import Path

watch_folder = Path.home() / "Downloads"  # folder to watch

sorting_rules = {
    ".jpg": "images", ".jpeg": "images", ".png": "images", ".webp": "images", ".gif": "images",

    ".mp4": "videos", ".webm": "videos",

    ".mp3": "audio",

    ".exe": "installers",
    ".msi":"installers"
}