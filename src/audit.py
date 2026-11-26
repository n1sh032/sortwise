from pathlib import Path

from config import watch_folder
from classifier import classify_image
from doc_classifier import classify_document

image_extensions = [".jpg", ".jpeg", ".png"]
pdf_extensions = [".pdf"]

label_to_folder = {
    "a screenshot": "screenshots",
    "a meme": "memes",
    "a receipt": "receipts",
    "a photo of a person": "photos",
    "a document scan": "documents",
    "a nature or landscape photo": "photos"
}

doc_label_to_folder = {
    "a receipt": "receipts",
    "an important document": "important",
    "a resume": "important",
    "a manual or instructions": "documents",
    "an article or blog post": "documents",
    "a form to fill out": "important"
}

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