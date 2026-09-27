"""Advance-width lookup against the pre-calibrated table."""
import json
import os

_TABLE_PATH = os.path.join(os.path.dirname(__file__), "..", "metrics", "advances.json")

_table = None


def load_table(path=_TABLE_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _table():
    global _table
    if _table is None:
        _table = load_table()
    return _table


def _is_grid_char(ch):
    cp = ord(ch)
    # U+FF01-FF60 fullwidth ASCII (1em), U+FFE0-FFE6 fullwidth symbols (1em).
    # U+FF61-FFDC are HALFWIDTH katakana/hangul (0.5em): NOT grid chars.
    return (cp == 0x3000
            or 0xFF01 <= cp <= 0xFF60
            or 0xFFE0 <= cp <= 0xFFE6
            or cp == 0x2588)


def advance_of(cluster, table=None):
    """Advance width of one grapheme cluster, in em. None if unknown."""
    t = table or _table()
    if cluster in t["emoji"]:
        return t["emoji"][cluster]
    if len(cluster) == 1:
        for sp in t["spacers"]:
            if sp["char"] == cluster:
                return sp["em"]
        if _is_grid_char(cluster):
            return t["grid_em"]
    return None
