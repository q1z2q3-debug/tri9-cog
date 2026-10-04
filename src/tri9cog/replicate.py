"""Replication: blueprint generation (isomorphic / mirror / variation)
and verify (self-check a new story against a target blueprint)."""

from __future__ import annotations

import json
import random
from typing import Dict, List, Optional, Sequence

from .annotate import DIM_ORDER, to_digits, from_digits
from .fingerprint import encode, decode, fingerprint, load_nodes

STRATEGIES = ("isomorphic", "mirror", "variation")

# Fake randomness is fine for blueprint generation; pin the seed for tests.
_rng = random.Random(19683)


def _transform(coordinate: str, strategy: str, vary_dims: Optional[Sequence[str]] = None) -> str:
    digits = to_digits(coordinate)
    if strategy == "mirror":
        # 0<->2, 1 stays 1 (mirror flip on each ternary axis)
        digits = [2 - v for v in digits]
    elif strategy == "variation":
        dims = set(vary_dims or ("S1", "S2", "S3", "C1", "C2", "C3"))
        digits = [(_rng.choice((0, 1, 2)) if DIM_ORDER[i] in dims else v) for i, v in enumerate(digits)]
    # isomorphic: keep as-is
    return from_digits(digits)


def build_blueprint(
    fingerprint_: dict,
    strategy: str = "isomorphic",
    nodes: Optional[int] = None,
    vary_dims: Optional[Sequence[str]] = None,
    seed: int = 19683,
) -> List[dict]:
    """Generate a target node-coordinate blueprint from a source fingerprint.

    - isomorphic: copy the source path coordinates verbatim;
    - mirror: flip every coordinate 0<->2;
    - variation: keep primary dims (T by default) and vary the others stochastically.

    When `nodes` is given, the path is resampled (with wrap) to that length.
    """
    global _rng
    _rng = random.Random(seed)
    if strategy not in STRATEGIES:
        raise ValueError(f"strategy must be one of {STRATEGIES}")

    src_coords = [decode(c) for c in fingerprint_.get("path", [])]
    if not src_coords:
        raise ValueError("fingerprint has no path (node coordinate sequence) — re-run fingerprint with path")

    if nodes is None:
        nodes = len(src_coords)

    blueprint = []
    for i in range(nodes):
        base = src_coords[i % len(src_coords)]
        blueprint.append(
            {
                "node": f"new_{i + 1}",
                "coordinate": _transform(base, strategy, vary_dims),
            }
        )
    return blueprint


def verify_story(
    story_rows: Sequence[dict],
    blueprint: Sequence[dict],
) -> dict:
    """Compare a new story's node coordinates against a target blueprint.

    Reports per-node hamming distance, plus aggregate entropy / mode deltas.
    """
    if len(story_rows) != len(blueprint):
        raise ValueError(
            f"story has {len(story_rows)} nodes but blueprint has {len(blueprint)}"
        )

    per_node = []
    hamming_sum = 0
    for r, b in zip(story_rows, blueprint):
        d = to_digits(r["coordinate"])
        t = to_digits(b["coordinate"])
        h = sum(1 for x, y in zip(d, t) if x != y)
        hamming_sum += h
        per_node.append(
            {
                "node": r["node"],
                "story_coord": r["coordinate"],
                "target_coord": b["coordinate"],
                "hamming": h,
                "match": h == 0,
            }
        )

    story_fp = fingerprint(story_rows, top_turns=0)
    target_fp = fingerprint(blueprint, top_turns=0)

    return {
        "nodes": len(story_rows),
        "matched": sum(1 for p in per_node if p["match"]),
        "mean_hamming": round(hamming_sum / len(per_node), 3),
        "entropy_story": story_fp["entropy_total"],
        "entropy_target": target_fp["entropy_total"],
        "entropy_delta": round(story_fp["entropy_total"] - target_fp["entropy_total"], 4),
        "mode_story": story_fp["mode_per_dim"],
        "mode_target": target_fp["mode_per_dim"],
        "turning_hits": _turning_hits(story_rows, blueprint),
        "detail": per_node,
    }


def _turning_hits(story_rows: Sequence[dict], blueprint: Sequence[dict]) -> dict:
    """Count how many of the blueprint's top turning intervals are preserved."""

    def top_k(rows: Sequence[dict], k: int = 3) -> List[tuple]:
        out = []
        prev_digits: Optional[List[int]] = None
        for r in rows:
            d = to_digits(r["coordinate"])
            if prev_digits is not None:
                out.append(
                    (
                        sum(1 for x, y in zip(d, prev_digits) if x != y),
                        abs(encode(from_digits(d)) - encode(from_digits(prev_digits))),
                    )
                )
            prev_digits = d
        out.sort(reverse=True)
        return out[:k]

    return {"story_top": top_k(story_rows), "target_top": top_k(blueprint)}


def load_blueprint(path: str) -> List[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)