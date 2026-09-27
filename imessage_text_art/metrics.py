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
    return cp == 0x3000 or 0xFF00 <= cp <= 0xFFEF or cp == 0x2588


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
