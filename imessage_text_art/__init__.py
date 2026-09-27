"""iMessage text art centering engine.

Pre-calibrated: advance widths ship in metrics/advances.json, measured once
via CoreText. The algorithm itself is pure arithmetic, no platform calls.
"""
from .center import center_art, check_art
from .metrics import load_table, advance_of

__all__ = ["center_art", "check_art", "load_table", "advance_of"]
