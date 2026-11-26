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

def wait_until_ready(filepath, timeout=60, stable_checks=3, interval=1):
    """Wait until a download exists and its size stays unchanged."""
    deadline = time.monotonic() + timeout
    last_size = None
    stable = 0
    while time.monotonic() < deadline:
        try:
            size = filepath.stat().st_size
        except FileNotFoundError:
            return False
        if size == last_size:
            stable += 1
            if stable >= stable_checks:
                return True
        else:
            stable = 0
            last_size = size
        time.sleep(interval)
    print("skipping", filepath.name, "- download did not finish before timeout")
    return False


def sort_file(filepath):

    # skip temp/lock files that office apps create while a file is open
    if filepath.name.startswith("~$"):
        return

    try:
        ext = filepath.suffix.lower()
        if ext in image_extensions:
            label = classify_image(filepath)
            folder_name = label_to_folder.get(label, "images")
            method = "clip"
        elif ext in pdf_extensions:
            label = classify_document(filepath)
            folder_name = doc_label_to_folder.get(label, "documents")
            method = "doc_clip"
        else:
            label = ext
            folder_name = sorting_rules.get(ext, "misc")
            method = "rule"

        dest = watch_folder / folder_name
        dest.mkdir(exist_ok=True)
        destination = unique_destination(dest / filepath.name)
        shutil.move(str(filepath), str(destination))
        log_decision(destination.name, method, label, folder_name)
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