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
                    labels.append(correct_folder)
                else:
                    print("skipping", filename, "- file not found anymore")

    return embeddings, labels

if __name__ == "__main__":

    X, y = load_corrections()

    print("found", len(X), "correction examples")

    if len(X) < 5:
        print("not enough data yet, keep using correct.py when clip gets things wrong")
    else:
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X, y)

        joblib.dump(clf, "my_classifier.pkl")
        print("model saved to my_classifier.pkl")