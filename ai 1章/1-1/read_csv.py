from types import FunctionType
from typing import Any, List
import csv


def read(path: str, types: Any = float) -> List[List[int]]:
    with open(path) as f:
        reader = csv.reader(f)
        l = [[types(r) for r in row] for row in reader]

    return l
