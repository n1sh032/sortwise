from pathlib import Path
import os

project_root = Path(__file__).resolve().parents[1]
watch_folder = Path(os.getenv("SORTWISE_FOLDER", str(Path.home() / "Downloads"))).expanduser()

sorting_rules = {
    ".jpg": "images", ".jpeg": "images", ".png": "images", ".webp": "images", ".gif": "images",

    ".mp4": "videos", ".webm": "videos",

    ".mp3": "audio",

    ".pdf": "documents", ".docx": "documents", ".doc": "documents",
    ".pptx": "documents", ".pptm": "documents", ".xlsx": "documents",
    ".csv": "documents", ".html": "documents",

    ".py": "code", ".c": "code",

    ".zip": "archives", ".rar": "archives", ".jar": "archives",

    ".exe": "installers", ".msi": "installers", ".msix": "installers",

    ".srt": "subtitles", ".vtt": "subtitles", ".lrc": "subtitles",

    ".schem": "minecraft", ".schematic": "minecraft", ".litematic": "minecraft",
}