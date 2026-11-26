from transformers import pipeline
from pypdf import PdfReader

# this loads a text classification model, similar idea to clip but for words
# also only loads once since its at the top level, not inside a function
text_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

doc_labels = [
    "a receipt",
    "an important document",
    "a resume",
    "a manual or instructions",
    "an article or blog post",
    "a form to fill out"
]

def read_pdf_text(filepath):

    reader = PdfReader(filepath)
    text = ""

