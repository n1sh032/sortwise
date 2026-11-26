import argparse
from pathlib import Path

from sorter import classify, image_extensions, pdf_extensions


def audit_folder(folder_path):
    flagged = []
    for filepath in folder_path.iterdir():
        if not filepath.is_file() or filepath.suffix.lower() not in image_extensions + pdf_extensions:
            continue
        try:
            _, _, expected = classify(filepath)
        except Exception as exc:
            print("could not classify", filepath.name, "-", exc)
            continue
        if expected != folder_path.name:
            flagged.append((filepath.name, folder_path.name, expected))
    return flagged


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Review file classifications without moving anything")
    parser.add_argument("folder", type=Path)
    for name, current, expected in audit_folder(parser.parse_args().folder):
        print(f"{name}: {current} -> {expected}")
