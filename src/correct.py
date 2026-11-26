import sys
import shutil
from pathlib import Path

from config import watch_folder
from logger import log_decision

def find_file(filename):
    selected = Path(filename)
    if len(selected.parts) == 2 and not selected.anchor and ".." not in selected.parts:
        path = watch_folder / selected
        return path if path.is_file() and path.resolve().is_relative_to(watch_folder.resolve()) else None
    if len(selected.parts) != 1 or selected.anchor or selected.name in {"", ".."}:
        return None

    # looks through all the subfolders inside watch_folder
    # since we dont know which folder clip put it in
    matches = []
    for folder in watch_folder.iterdir():
        if folder.is_dir():
            possible_path = folder / filename
            if possible_path.exists():
                matches.append(possible_path)

    if len(matches) > 1:
        print("ambiguous filename; found:")
        for match in matches:
            print(" -", match.relative_to(watch_folder))
        return None
    return matches[0] if matches else None

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
