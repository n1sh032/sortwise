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

