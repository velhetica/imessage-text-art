---
name: "imessage-text-art"
description: "Design text/ASCII art that actually renders in iMessage. Use when Matt wants text art sent over iMessage, or asks about text-art rendering."
---

# iMessage Text Art

## Purpose
Create text art that survives iMessage rendering (proportional San Francisco font, tall line spacing). Ships with a renderer that converts pixel grids into correctly-spaced block art.

## The rules (empirically tested over 6 live sends, 2026-09-27)
- iMessage uses a **proportional** font: every character has its own width. There is no monospace grid.
- The invisible spacer is **U+2800 BRAILLE PATTERN BLANK** (⠀). It renders at the same advance width as █ (U+2588 FULL BLOCK) and is fully invisible. NEVER use regular spaces or periods for alignment: both render ~1/4 width and collapse the design (periods also show as visible dots). U+3000 ideographic space is wider than █ and splits rows into visible segments.
- Line spacing is taller than the glyphs, so stacked rows never touch. Solid fills taller than ~10 rows read as barcodes, not shapes. Keep block art compact with a clear silhouette.
- Every row must stay under ~30 chars or the bubble wraps mid-row.
- Three lanes that work:
  1. **One-liners** (`o==|::::::::>`) — immune to every rendering quirk, always land.
  2. **Small sketch art**, max ~8 rows, using `/ \ | - +` only — proportional skew is tolerable at small sizes, reads as charmingly janky.
  3. **Emoji-square pixel art** (⬜⬛) — emoji cells align in a true grid, the cleanest option for pixel designs. On blue outgoing bubbles, light squares (⬜) read best.

## Workflow
1. Pick a lane and draw the design as a grid: `#` = filled, `.` = empty (spaces also treated as empty).
2. Render it: `python3 bin/render.py <grid-file> [--emoji] [--caption "text"]`. Maps `#`→█ and empty→⠀, strips trailing spacers, enforces the width limit. `--emoji` renders two-tone ⬜/⬛ pixel art instead.
3. Send from this machine via the work-Mac bridge: `~/workspace/tailscale-mac/send-imessage.sh "<+1-handle>" "<message>"`. 1:1 sends need Matt's approval of the exact text first; the handle must be the +1 form.
4. Verify delivery in chat.db: the message row must show `is_sent=1 AND is_delivered=1`.

## Output contract
- The renderer prints the final message text to stdout, ready to paste into the send command.
- Checked-in example grids live in `references/gallery/`.

## Operating rules
- Never hand-space alignment with `" "` or `"."` — always go through the renderer.
- Don't exceed ~10 rows of solid block fill; redesign as outline/sketch instead.
- When trying an unproven design, send it to Matt's own thread first before sending it to anyone else.
