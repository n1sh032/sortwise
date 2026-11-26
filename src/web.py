import argparse
from pathlib import Path

from web_runtime import serve


class SortwiseApplication:
    actions = {"scan", "sort"}

    def __init__(self, folder):
        self.folder = folder.resolve()
        if not self.folder.is_dir():
            raise ValueError("Choose an existing watch folder")

    def describe(self):
        return {"name": "Sortwise", "folder": str(self.folder)}

    def execute(self, action, payload):
        import sorter

        sorter.watch_folder = self.folder
