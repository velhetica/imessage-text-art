"""Epic Buster Sword generator: silhouette + gradient shading + dither + materia slots.
Output is content rows (no manual centering); pipe through the library to center."""
Z='\u3000'; UL='\uff3f'; MC='\uffe3'; SL='\uff0f'; BS='\uff3c'; VB='\uff5c'; OO='\uff2f'
DARK_A='\uff20'; DARK_B='\uff03'; MID='\uff0a'   # ＠ ＃ ＊

# silhouette: (start_col, end_col) per row, 15-col grid
sil = []
for i in range(5):            # tip: widen from center col 7
    sil.append((7-i, 7+i))
for _ in range(5, 15):        # blade body: cols 2-12
    sil.append((2, 12))

rows = []
for r, (a, b) in enumerate(sil):
    line = []
    widening = r < 5
    for c in range(a, b+1):
        if c == a:
            line.append(SL if widening else VB)
        elif c == b:
            line.append(BS if widening else VB)
        else:
            # interior shading: dark left -> light right, dithered
            t = (c - a) / (b - a)
            if r == 0:
                line.append(Z)
            elif t < 0.35:
                line.append(DARK_A if (r+c) % 2 == 0 else DARK_B)
            elif t < 0.7:
                line.append(MID if (r+c) % 2 == 0 else Z)
            else:
                line.append(Z)
    rows.append(''.join(line))

A = 2  # blade rows start at grid col 2; string index = col - A
# fuller: dark groove line left of center, rows 6-10 and 12
for r in list(range(6, 11)) + [12]:
    lst = list(rows[r]); lst[4-A] = DARK_B; rows[r] = ''.join(lst)
# materia slots (symmetric about col 7)
for c in (5, 9):
    lst = list(rows[11]); lst[c-A] = OO; rows[11] = ''.join(lst)

rows.append(Z + UL*13)            # guard
for _ in range(4):
    rows.append(Z*6 + VB + DARK_B + VB)   # wrapped grip
rows.append(Z*6 + BS + OO + SL)  # pommel

open('/tmp/itarepo/examples/buster-sword-epic.txt','w').write('\n'.join(rows))
print('\n'.join(rows))
