"""Fingerprint computation: encoding, distribution, entropy, turning points.

The framework maps every plot node / character state into a unique ternary
code in the 3^9 = 19683 state space.

  code = T1*3^8 + T2*3^7 + T3*3^6
       + S1*3^5 + S2*3^4 + S3*3^3
       + C1*3^2 + C2*3^1 + C3*3^0
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .annotate import DIM_ORDER, to_digits, from_digits

# 3^9 total cells; code range 0 .. 19682
TOTAL_CELLS = 3 ** 9

TRIADS = {
    "T": DIM_ORDER[0:3],
    "S": DIM_ORDER[3:6],
    "C": DIM_ORDER[6:9],
}


def encode(coordinate: str) -> int:
    """Encode '221-221-220' -> 18924 (ternary weighted sum)."""
    digits = to_digits(coordinate)
    code = 0
    for exp, v in enumerate(reversed(digits)):
        code += v * (3 ** exp)
    return code


def decode(code: int) -> str:
    """Decode 18924 -> '221-221-220'."""
    if not (0 <= code < TOTAL_CELLS):
        raise ValueError(f"code out of range [0,{TOTAL_CELLS}): {code}")
    digits = []
    n = code
    for _ in range(9):
        digits.append(n % 3)
        n //= 3
    return from_digits(reversed(digits))


def load_nodes(path: str) -> List[dict]:
    """Load a node table CSV.

    Required columns: `node` or `chapter`(id), `coordinate`.
    Optional: `title`.
    """
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            coord = (r.get("coordinate") or "").strip()
            if not coord:
                continue
            node = r.get("node") or r.get("chapter") or r.get("id") or str(len(rows) + 1)
            rows.append({"node": node.strip(), "coordinate": coord, "title": (r.get("title") or "").strip()})
    return rows


def dimension_frequencies(rows: Sequence[dict]) -> Dict[str, List[int]]:
    """Per-dimension frequency of states 0/1/2 across all nodes."""
    freq = {dim: [0, 0, 0] for dim in DIM_ORDER}
    for row in rows:
        digits = to_digits(row["coordinate"])
        for dim, v in zip(DIM_ORDER, digits):
            freq[dim][v] += 1
    return freq


def entropy(counts: Sequence[int]) -> float:
    """Shannon entropy in bits over a multiset of discrete values."""
    total = sum(counts)
    if total == 0:
        return 0.0
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h


def triad_entropy(freq: Dict[str, List[int]], triad: str) -> float:
    """Entropy over the pooled 0/1/2 counts of the three dimensions of a triad."""
    pooled = [0, 0, 0]
    for dim in TRIADS[triad]:
        for i in range(3):
            pooled[i] += freq[dim][i]
    return entropy(pooled)


def fingerprint(
    rows: Sequence[dict],
    *,
    top_turns: int = 10,
) -> dict:
    """Compute the full structural fingerprint of a node sequence.

    Result fields:
      nodes, unique_codes, code_range, entropy_total,
      entropy_triad {T,S,C}, mode_per_dim, triad_center {T,S,C},
      turning_points (list of {interval, dims_changed, code_delta, from, to}),
      path (per-node code sequence, optional when `include_path=True`).
    """
    coords = [r["coordinate"] for r in rows]
    codes = [encode(c) for c in coords]
    freq = dimension_frequencies(rows)

    overall = [0, 0, 0]
    for dim in DIM_ORDER:
        for i in range(3):
            overall[i] += freq[dim][i]

    triad_centers = {}
    for t in "TSC":
        pooled = [0, 0, 0]
        for dim in TRIADS[t]:
            for i in range(3):
                pooled[i] += freq[dim][i]
        triad_centers[t] = int(max(range(3), key=lambda i: pooled[i]))

    # turning points: adjacent nodes, count dimensions changed and |Δcode|
    turns = []
    for i in range(1, len(codes)):
        a = to_digits(coords[i - 1])
        b = to_digits(coords[i])
        changed = sum(1 for x, y in zip(a, b) if x != y)
        turns.append(
            {
                "interval": f"{rows[i-1]['node']}→{rows[i]['node']}",
                "dims_changed": changed,
                "code_delta": abs(codes[i] - codes[i - 1]),
            }
        )
    turns.sort(key=lambda t: (t["dims_changed"], t["code_delta"]), reverse=True)

    return {
        "nodes": len(rows),
        "unique_codes": len(set(codes)),
        "code_range": [min(codes), max(codes)],
        "entropy_total": round(entropy(overall), 4),
        "entropy_triad": {t: round(triad_entropy(freq, t), 4) for t in "TSC"},
        "mode_per_dim": {d: int(max(range(3), key=lambda i: freq[d][i])) for d in DIM_ORDER},
        "triad_center": triad_centers,
        "turning_points": turns[:top_turns],
        "path": codes,
    }


def fingerprint_from_csv(path: str, **kwargs) -> dict:
    """Convenience: compute fingerprint directly from a CSV node table."""
    return fingerprint(load_nodes(path), **kwargs)


def save_json(obj: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)