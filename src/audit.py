import argparse
from pathlib import Path

from sorter import classify, image_extensions, pdf_extensions


def audit_folder(folder_path):

    current_folder_name = folder_path.name
    flagged = []

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