from config import watch_folder
from sorter import sort_file

if __name__ == "__main__":

    files = [f for f in watch_folder.iterdir() if f.is_file()]

    print("found", len(files), "files to sort")

    for filepath in files:
        sort_file(filepath)