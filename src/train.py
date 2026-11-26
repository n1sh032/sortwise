import csv
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression

from config import watch_folder
from classifier import get_embedding

log_file = Path("sort_log.csv")

def load_corrections():

    embeddings = []
    labels = []

    with open(log_file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["method"] == "correction":

                filename = row["filename"]
                correct_folder = row["folder"]

                # need to find the file again since it moved after the correction
                filepath = watch_folder / correct_folder / filename

                if filepath.exists():
                    emb = get_embedding(filepath)
                    embeddings.append(emb)
