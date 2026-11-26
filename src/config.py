from pathlib import Path

watch_folder = Path.home() / "Downloads"  # folder to watch

sorting_rules = {
    ".jpg": "images",
    ".jpeg":"images",
      ".png": "images",
    ".pdf": "documents",
    ".docx" : "documents",
    ".zip": "archives",
    ".exe": "installers",
    ".msi":"installers"
}