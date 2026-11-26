import sys
import shutil
from pathlib import Path

from config import watch_folder
from logger import log_decision

def find_file(filename):

    # looks through all the subfolders inside watch_folder
    # since we dont know which folder clip put it in
    for folder in watch_folder.iterdir():
        if folder.is_dir():
            possible_path = folder / filename
            if possible_path.exists():
                return possible_path

    return None

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("usage: python correct.py filename correct_folder")
        sys.exit()

    filename = sys.argv[1]
    correct_folder = sys.argv[2]

    filepath = find_file(filename)

    if filepath == None:
        print("couldnt find", filename, "in any sorted folder")
        sys.exit()

    dest = watch_folder / correct_folder
    dest.mkdir(exist_ok=True)

    old_folder = filepath.parent.name

    shutil.move(str(filepath), str(dest / filename))

    log_decision(filename, "correction", old_folder, correct_folder)

    print("moved", filename, "from", old_folder, "to", correct_folder)