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

        folder_name = sorting_rules.get(ext)
        if folder_name == None:
            print("no rule for", ext, "-", filepath.name)
            return

        dest = watch_folder / folder_name
        dest.mkdir(exist_ok=True)

        time.sleep(1)   # wait a bit so the file finishes downloading first

        try:
            shutil.move(str(filepath), str(dest / filepath.name))
            print("moved", filepath.name, "->", folder_name)
        except Exception as e:
            print("failed to move", filepath.name, e)