import csv
from pathlib import Path
from datetime import datetime

log_file = Path("sort_log.csv")

def log_decision(filename, method, label, folder):

    file_exists = log_file.exists()

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["time", "filename", "method", "label", "folder"])

        writer.writerow([datetime.now(), filename, method, label, folder])