from pathlib import Path

from config import watch_folder
from classifier import classify_image
from doc_classifier import classify_document

image_extensions = [".jpg", ".jpeg", ".png"]
pdf_extensions = [".pdf"]

