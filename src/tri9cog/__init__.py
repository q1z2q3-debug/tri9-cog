"""tri9cog — Triadic Cognitive Space.

A formalized ternary cognitive coordinate system for literary structure:
3 elements (Time/Space/Causality) x 9 dimensions x 3 states = 3^9 = 19683 cells.
"""

__version__ = "0.1.0"

from .annotate import validate_coordinate, make_template
from .fingerprint import (
    encode,
    decode,
    dimension_frequencies,
    entropy,
    triad_entropy,
    fingerprint,
    load_nodes,
)
from .replicate import build_blueprint, verify_story

__all__ = [
    "encode",
    "decode",
    "dimension_frequencies",
    "entropy",
    "triad_entropy",
    "fingerprint",
    "load_nodes",
    "validate_coordinate",
    "make_template",
    "build_blueprint",
    "verify_story",
]