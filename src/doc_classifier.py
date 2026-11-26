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

    for page in reader.pages:
        text += page.extract_text()

    return text

def classify_document(filepath):

    text = read_pdf_text(filepath)

    # only using the first 1000 characters, the model has a limit anyway
    # and the first chunk is usually enough to tell what it is
    text = text[:1000]

    if text.strip() == "":
        return "an important document"   # cant read it, play it safe

    result = text_classifier(text, doc_labels)
    best_label = result["labels"][0]

    return best_label