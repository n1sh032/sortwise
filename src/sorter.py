import time
import shutil
from pathlib import Path
from watchdog.events import FileSystemEventHandler

from config import watch_folder, sorting_rules

class SorterHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = Path(event.src_path)
        ext = filepath.suffix.lower()
