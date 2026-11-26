import time
import shutil
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from logger import log_decision

from config import watch_folder, sorting_rules
from classifier import classify_image

image_extensions = [".jpg", ".jpeg", ".png"]

# clip labels dont match folder names exactly, so we need this
label_to_folder = {
    "a screenshot": "screenshots",
    "a meme": "memes",
    "a receipt": "receipts",
    "a photo of a person": "photos",
    "a document scan": "documents",
    "a nature or landscape photo": "photos"
}

class SorterHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = Path(event.src_path)
        ext = filepath.suffix.lower()

        time.sleep(1)

        if ext in image_extensions:
            label = classify_image(filepath)
            folder_name = label_to_folder.get(label, "images")
        else:
            folder_name = sorting_rules.get(ext)

        if folder_name == None:
            print("no rule for", ext, "-", filepath.name)
            return

        dest = watch_folder / folder_name
        dest.mkdir(exist_ok=True)

        try:
            shutil.move(str(filepath), str(dest / filepath.name))
            print("moved", filepath.name, "->", folder_name)
        except Exception as e:
            print("failed to move", filepath.name, e)
        if ext in image_extensions:
            label = classify_image(filepath)
            folder_name = label_to_folder.get(label, "images")
            log_decision(filepath.name, "clip", label, folder_name)
        else:
            folder_name = sorting_rules.get(ext)
            log_decision(filepath.name, "rule", ext, folder_name)