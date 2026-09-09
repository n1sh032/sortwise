import time
from watchdog.observers import Observer

from config import watch_folder
from sorter import SorterHandler

def main():
    handler = SorterHandler()
    obs = Observer()
    obs.schedule(handler, str(watch_folder), recursive=False)
    obs.start()

    print("watching", watch_folder)
    print("press ctrl+c to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("stopping...")
        obs.stop()

    obs.join()

if __name__=="__main__":
    main()