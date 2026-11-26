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


    for filepath in folder_path.iterdir():

        if filepath.is_dir():
            continue

        ext = filepath.suffix.lower()

        if ext in image_extensions:
            print("checking", filepath.name, "...")
            label = classify_image(filepath)
            expected_folder = label_to_folder.get(label, "images")

        elif ext in pdf_extensions:
            print("checking", filepath.name, "(this can take a while)...")
            label = classify_document(filepath)
            expected_folder = doc_label_to_folder.get(label, "documents")

        else:
            continue

        if expected_folder != current_folder_name:
            flagged.append((filepath.name, current_folder_name, expected_folder))

    return flagged