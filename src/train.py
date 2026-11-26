import csv
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression

from config import watch_folder
from classifier import get_embedding

log_file = Path("sort_log.csv")
