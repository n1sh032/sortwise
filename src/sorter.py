import time
import shutil
from pathlib import Path
from watchdog.events import FileSystemEventHandler

from config import watch_folder, sorting_rules
from classifier import classify_image
from doc_classifier import classify_document
from logger import log_decision

image_extensions = [".jpg", ".jpeg", ".png"]
pdf_extensions = [".pdf"]

label_to_folder = {
    "a screenshot": "screenshots",
    "a meme": "memes",
    "a receipt": "receipts",
    "a photo of a person": "photos",
    "a document scan": "documents",
    "a nature or landscape photo": "photos"
}

doc_label_to_folder = {
    "a receipt": "receipts",
    "an important document": "important",
    "a resume": "important",
    "a manual or instructions": "documents",
    "an article or blog post": "documents",
    "a form to fill out": "important"
}

def sort_file(filepath):

    # skip temp/lock files that office apps create while a file is open
    if filepath.name.startswith("~$"):
        return

    ext = filepath.suffix.lower()

    if ext in image_extensions:
        label = classify_image(filepath)
        folder_name = label_to_folder.get(label, "images")
        log_decision(filepath.name, "clip", label, folder_name)

    elif ext in pdf_extensions:
        label = classify_document(filepath)
        folder_name = doc_label_to_folder.get(label, "documents")
        log_decision(filepath.name, "doc_clip", label, folder_name)

    else:
        # anything not covered by a rule goes into misc instead of
        # just getting skipped forever
        folder_name = sorting_rules.get(ext, "misc")
        log_decision(filepath.name, "rule", ext, folder_name)

    dest = watch_folder / folder_name
    dest.mkdir(exist_ok=True)

    try:
        shutil.move(str(filepath), str(dest / filepath.name))
        print("moved", filepath.name, "->", folder_name)
    except Exception as e:
        print("failed to move", filepath.name, e)

class SorterHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = Path(event.src_path)
        time.sleep(1)
        sort_file(filepath)