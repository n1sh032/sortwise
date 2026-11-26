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
        if action == "scan":
            files = sorted(
                p for p in self.folder.iterdir() if p.is_file() and not p.is_symlink()
            )
            return {
                "files": [
                    {"name": p.name, "bytes": p.stat().st_size} for p in files[:200]
                ],
                "total": len(files),
            }
        names = payload.get("names")
        if not isinstance(names, list) or not names or len(names) > 200:
            return {"error": "Select between 1 and 200 files."}
        paths = []
        for name in names:
            if not isinstance(name, str) or Path(name).name != name:
                return {
                    "error": "Only files directly inside the watch folder can be sorted."
                }
            path = self.folder / name
            if path.is_symlink() or path.resolve().parent != self.folder:
                return {"error": "Linked or external files cannot be sorted."}
            paths.append(path)
        outcomes = [sorter.sort_file(path) for path in paths]
        return {"outcomes": outcomes}


