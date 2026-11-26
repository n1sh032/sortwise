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
