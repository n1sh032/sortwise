import csv
from pathlib import Path
from datetime import datetime

log_file = Path("sort_log.csv")

def log_decision(filename, method, label, folder):

    file_exists = log_file.exists()
