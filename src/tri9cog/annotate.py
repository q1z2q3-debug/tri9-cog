"""Annotation helpers: coordinate validation and empty template generation."""

from __future__ import annotations

import csv
import re
from typing import Iterable, List

DIM_ORDER = ["T1", "T2", "T3", "S1", "S2", "S3", "C1", "C2", "C3"]

_COORD_RE = re.compile(r"^[012]{3}-[012]{3}-[012]{3}$")


def validate_coordinate(coordinate: str) -> bool:
    """Return True if the coordinate is a valid 9-digit ternary triple.

    Accepts both '221-221-220' and '221221220' forms.
    """
    if not isinstance(coordinate, str):
        return False
    c = coordinate.strip()
    if _COORD_RE.match(c):
        return True
    c_flat = c.replace("-", "")
    return bool(re.fullmatch(r"[012]{9}", c_flat))


def to_digits(coordinate: str) -> List[int]:
    """Convert '221-221-220' -> [2,2,1,2,2,1,2,2,0]."""
    c = coordinate.strip().replace("-", "")
    return [int(ch) for ch in c]


def from_digits(digits: Iterable[int]) -> str:
    """Convert [2,2,1,2,2,1,2,2,0] -> '221-221-220'."""
    d = list(digits)
    if len(d) != 9 or any(v not in (0, 1, 2) for v in d):
        raise ValueError(f"invalid 9 ternary digits: {digits}")
    return f"{d[0]}{d[1]}{d[2]}-{d[3]}{d[4]}{d[5]}-{d[6]}{d[7]}{d[8]}"


def make_template(
    node_ids: Iterable[str], path: str | None = None
) -> List[dict]:
    """Generate an empty annotation template.

    Each row: node, coordinate (empty), plus 9 per-dimension columns.

    If `path` is given the template is also written as CSV (UTF-8).
    """
    rows = []
    for nid in node_ids:
        row = {"node": str(nid), "coordinate": ""}
        for dim in DIM_ORDER:
            row[dim] = ""
        rows.append(row)
    if path:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["node", "coordinate"] + DIM_ORDER)
            writer.writeheader()
            writer.writerows(rows)
    return rows