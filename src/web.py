import argparse
from pathlib import Path

from web_runtime import serve


class SortwiseApplication:
    actions = {"scan", "sort"}

