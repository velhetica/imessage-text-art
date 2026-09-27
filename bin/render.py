#!/usr/bin/env python3
"""Render a pixel grid as iMessage-safe text art.

Grid format: lines of '#' (filled) and '.' or ' ' (empty).

Default mode: '#' -> U+2588 FULL BLOCK, empty -> U+2800 BRAILLE PATTERN
BLANK (the invisible spacer that matches the block's advance width in
iMessage's proportional font). Trailing spacers are stripped per row.

--emoji mode: '#' -> white square, empty -> black square (two-tone pixel
art; emoji cells align in a true grid).

Validation: any row wider than 30 chars is an error (the iPhone bubble
wraps mid-row). More than ~10 rows of solid block fill warns, because
iMessage's tall line spacing turns tall fills into barcodes.
"""
import argparse
import sys

BLOCK = "█"          # U+2588
SPACER = "⠀"         # U+2800 BRAILLE PATTERN BLANK (invisible, block-width)
WHITE_SQ = "⬜"
BLACK_SQ = "⬛"
MAX_COLS = 30
WARN_ROWS = 10


def render(lines, emoji=False):
    out = []
    for line in lines:
        cells = []
        for ch in line:
            if ch == "#":
                cells.append(WHITE_SQ if emoji else BLOCK)
            elif ch in (".", " "):
                cells.append(BLACK_SQ if emoji else SPACER)
            else:
                sys.exit(f"error: unexpected character {ch!r} in grid "
                         f"(use '#' and '.' only)")
        bg = BLACK_SQ if emoji else SPACER
        while cells and cells[-1] == bg:
            cells.pop()
        out.append("".join(cells))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("grid", help="grid file: '#' filled, '.' or space empty")
    ap.add_argument("--emoji", action="store_true",
                    help="render as two-tone emoji pixel art")
    ap.add_argument("--caption", default="",
                    help="text appended after a blank line")
    args = ap.parse_args()

    with open(args.grid) as f:
        lines = [ln.rstrip("\n") for ln in f]
    lines = [ln for ln in lines if ln.strip(" .") != ""]

    art = render(lines, emoji=args.emoji)

    width = max((len(r) for r in art), default=0)
    if width > MAX_COLS:
        sys.exit(f"error: widest row is {width} chars "
                 f"(limit {MAX_COLS}, the bubble would wrap)")
    if len(art) > WARN_ROWS and not args.emoji:
        print(f"warning: {len(art)} rows of block fill — tall stacks read "
              f"as barcodes in iMessage; consider a shorter design",
              file=sys.stderr)

    msg = "\n".join(art)
    if args.caption:
        msg += "\n\n" + args.caption
    print(msg)


if __name__ == "__main__":
    main()
