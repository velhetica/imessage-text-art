"""Centering algorithm for iMessage text art.

Input: art authored as plain text, one row per line, content only.
Leading whitespace is stripped; every row gets a computed indent so all
rows share the same visual center. Indents are composed greedily from the
pre-calibrated spacer table, largest first.

Rules the algorithm enforces:
- Every content character must be a fullwidth form (U+FF00-U+FFEF), U+3000,
  U+2588, or an entry in the emoji table. Anything else is flagged by
  check_art instead of silently miscentered.
- Rows wider than ~19 grid cells will wrap in the iMessage bubble; check_art
  warns about those.
"""
from .metrics import advance_of, load_table

# iMessage bubble wraps rows wider than about 19-20 fullwidth cells.
WRAP_LIMIT_CELLS = 19


def graphemes(s):
    """Split into grapheme clusters (keeps ZWJ sequences, VS16, modifiers together)."""
    clusters = []
    cur = ""
    for ch in s:
        cp = ord(ch)
        combining = (
            cp == 0x200D
            or 0xFE00 <= cp <= 0xFE0F
            or 0x1F3FB <= cp <= 0x1F3FF
            or 0xE0020 <= cp <= 0xE007F
        )
        if cur and combining:
            cur += ch
        else:
            if cur:
                clusters.append(cur)
            cur = ch
    if cur:
        clusters.append(cur)
    return clusters


def _spacer_list(table):
    return [(sp["char"], sp["em"]) for sp in table["spacers"]]


def compose_indent(target_em, table):
    """Greedy compose target_em from spacers, largest first."""
    out = ""
    rem = target_em
    for ch, em in _spacer_list(table):
        while rem >= em - 1e-9:
            out += ch
            rem -= em
    return out, rem


def center_art(text, table=None):
    """Center every row of text. Returns the composed art string."""
    t = table or load_table()
    rows = []
    for line in text.split("\n"):
        content = graphemes(line.strip())
        unknown = [g for g in content if advance_of(g, t) is None]
        if unknown:
            raise ValueError(
                "unknown advance for %r; add it to metrics/advances.json or use check_art"
                % ("".join(unknown),)
            )
        rows.append(content)
    widths = [sum(advance_of(g, t) for g in r) for r in rows]
    canvas = max(widths) if widths else 0
    out = []
    for row, w in zip(rows, widths):
        indent, _rem = compose_indent((canvas - w) / 2, t)
        out.append(indent + "".join(row))
    return "\n".join(out)


def check_art(text, table=None):
    """Validate art: unknown chars, wrap-risk rows. Returns list of warnings."""
    t = table or load_table()
    warnings = []
    for i, line in enumerate(text.split("\n"), 1):
        content = graphemes(line.strip())
        if not content:
            continue
        unknown = [g for g in content if advance_of(g, t) is None]
        if unknown:
            warnings.append(
                "row %d: unknown advance for %r (half-width ASCII? use fullwidth forms)"
                % (i, "".join(unknown))
            )
            continue
        w = sum(advance_of(g, t) for g in content)
        if w > WRAP_LIMIT_CELLS:
            warnings.append(
                "row %d: %.1f cells wide, iMessage wraps past ~%d"
                % (i, w, WRAP_LIMIT_CELLS)
            )
    return warnings
