# imessage-text-art

A skill for designing text/ASCII art that actually renders in iMessage.
Tested live over 6 sends on 2026-09-27.

## The short version

iMessage uses a proportional font and tall line spacing, so monospace
assumptions break. The one weird trick: **U+2800 BRAILLE PATTERN BLANK**
(⠀) is invisible *and* renders at the same advance width as █ (U+2588),
so centered, symmetric block art works. Regular spaces and periods
collapse to ~1/4 width; U+3000 ideographic space is too wide.

Three lanes that survive rendering:

1. **One-liners** (`o==|::::::::>`) — immune to everything.
2. **Small sketches** (≤8 rows, `/ \ | - +`) — charmingly janky.
3. **Emoji-square pixel art** (⬜⬛) — true grid alignment.

Never: space-based alignment, solid block fills taller than ~10 rows
(they render as barcodes), rows wider than ~30 chars.

## Use

```
python3 bin/render.py references/gallery/buster-sword.txt --caption "BUSTER SWORD - FFVII"
```

Grids use `#` for filled and `.` for empty. Example galleries live in
`references/gallery/`. See `SKILL.md` for the full rules and send workflow.
