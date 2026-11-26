from transformers import pipeline
from pypdf import PdfReader

# this loads a text classification model, similar idea to clip but for words
# also only loads once since its at the top level, not inside a function
text_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
