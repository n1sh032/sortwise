import time
from watchdog.observers import Observer

from config import watch_folder
from sorter import SorterHandler

def main():
    handler = SorterHandler()
    obs = Observer()
    obs.schedule(handler, str(watch_folder), recursive=False)
    obs.start()

