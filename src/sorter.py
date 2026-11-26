import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock
from watchdog.events import FileSystemEventHandler

from config import watch_folder, sorting_rules
from logger import log_decision

move_lock = Lock()

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
            stable = 1
            last_size = size
        time.sleep(interval)
    print("skipping", filepath.name, "- download did not finish before timeout")
    return False


def classify(filepath):
    ext = filepath.suffix.lower()
    if ext in image_extensions:
        from classifier import classify_image

        label = classify_image(filepath)
        return "clip", label, label_to_folder.get(label, "images")
    if ext in pdf_extensions:
        from doc_classifier import classify_document

        label = classify_document(filepath)
        return "doc_clip", label, doc_label_to_folder.get(label, "documents")
    return "rule", ext, sorting_rules.get(ext, "misc")


def sort_file(filepath):

    # skip temp/lock files that office apps create while a file is open
    if filepath.name.startswith("~$") or filepath.suffix.lower() in {
        ".part", ".crdownload", ".download", ".tmp",
    }:
        return
    try:
        if not wait_until_ready(filepath):
            return
        with move_lock:
            method, label, folder_name = classify(filepath)
            dest = watch_folder / folder_name
            dest.mkdir(exist_ok=True)
            destination = unique_destination(dest / filepath.name)
            shutil.move(str(filepath), str(destination))
            try:
                log_decision(destination.name, method, label, folder_name)
            except OSError as e:
                print("moved", destination, "but could not write the log:", e)
                return
        print("moved", filepath.name, "->", folder_name)
    except Exception as e:
        print("failed to classify or move", filepath.name, "-", e)


def unique_destination(destination):
    if not destination.exists():
        return destination
    index = 1
    while True:
        candidate = destination.with_name(f"{destination.stem} ({index}){destination.suffix}")
        if not candidate.exists():
            return candidate
        index += 1

class SorterHandler(FileSystemEventHandler):
    def __init__(self):
        self.workers = ThreadPoolExecutor(max_workers=4)
        self.pending = set()
        self.lock = Lock()

    def submit(self, path):
        with self.lock:
            if path in self.pending:
                return
            self.pending.add(path)
        self.workers.submit(self.process, path)

    def process(self, path):
        try:
            sort_file(path)
        finally:
            with self.lock:
                self.pending.discard(path)

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = Path(event.src_path)
        self.submit(filepath)

    def on_moved(self, event):
        path = Path(event.dest_path)
        if not event.is_directory and path.parent.resolve() == watch_folder.resolve():
            self.submit(path)
