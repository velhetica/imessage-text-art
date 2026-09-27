# imessage-text-art

Text art that actually renders in iMessage. Not approximately. Exactly.

iMessage uses the proportional San Francisco font, so naive ASCII art comes out skewed, wrapped, or lopsided. This repo is the system I built to beat that: a pre-calibrated centering algorithm plus the rendering rules I learned by sending dozens of pieces to my own phone and screenshotting the results.

## The trick

Fullwidth characters (／ ＼ ｜ ＿ Ｏ ￣, the U+FF00 block) and the ideographic space (U+3000) all render at exactly 1em in iMessage. Together they form a true uniform grid, so real ascii art aligns perfectly. That part needs no measurement: 1em is definitional in CJK typography.

The only things that need measuring are the exceptions. Emoji are not 1em (🐄 is 1.29em, which is what kept breaking my layouts). Fractional spacers (en space, thin space, hair space) have platform-specific widths. Those live in `metrics/advances.json`, pre-calibrated by measuring actual CoreText advances on a Mac. You do not need to measure anything.

## The algorithm

1. Author art as plain text, one row per line, content only (no manual centering).
2. Every character's advance width is looked up: 1em for grid chars, table values for emoji and spacers. Unknown characters are rejected, not guessed.
3. Canvas width = the widest row. Each row's left indent = (canvas − row width) / 2, composed greedily from the spacer table, largest first.
4. Every row's visual center lands on canvas / 2 within ~1pt. Verified, not eyeballed.

```bash
python -m imessage_text_art check < examples/ufo-cow.txt   # validate: unknown chars, wrap risk
python -m imessage_text_art center < examples/ufo-cow.txt  # emit centered art, paste into iMessage
```

## Authoring rules

- Build from fullwidth forms (U+FF00-U+FFEF) plus U+3000 for spacing. That is the grid.
- Keep rows under ~19 cells wide or the bubble wraps mid-row.
- iMessage trims trailing whitespace, so never rely on it.
- Emoji go on the table in `metrics/advances.json` (one measured entry each). The cow is already there.
- Half-width ASCII (`/ \ |`) cannot be centered reliably next to grid chars. Use the fullwidth versions.

## The lanes

Three things survive iMessage rendering: one-liners (`o==|::::::::>`), small sketch art (max ~8 rows, charmingly janky), and emoji-square pixel art (⬜⬛, a true grid). The fullwidth grid in this repo is the fourth lane and the precise one.

## Recalibration

`metrics/measure.swift` re-measures every advance via CoreText on a Mac. Run it if Apple ever changes font rendering and the table needs refreshing:

```bash
swift metrics/measure.swift   # adv in points; divide by 17 for em values
```

## Gallery

`gallery/` holds the experiments that taught me all of this, including the barcode Buster Sword, the spacer shootouts, and every UFO iteration. `examples/ufo-cow.txt` is the flagship: the source the algorithm centers.
