# make_repetition_penalties.py
# Regenerate with: python make_repetition_penalties.py
# Two penalties on the same two tokens: frequency scales the cut with the count,
# presence applies one flat cut for any prior appearance. Each red bar grows
# rightward along a "larger penalty" axis; its length is how much the penalty
# subtracts from that word's logit (its score).
from svg_theme import svg_open

W, H = 720, 438

# (token, times already appeared) — one heavily repeated, one used once
TOKENS = [("moonlight", 3), ("silver", 1)]
UNIT = 38  # px of penalty bar per "unit" of score subtracted

def panel(x, title, sub, penalty_of):
    bx = x + 24                            # bar origin (axis zero)
    out = [f'<rect x="{x}" y="120" width="312" height="244" rx="12" class="panel bdr" stroke-width="1.5"/>']
    out.append(f'<text x="{x+24}" y="154" font-size="16.5" font-weight="700" class="ink">{title}</text>')
    out.append(f'<text x="{x+24}" y="176" font-size="12.5" class="sub">{sub}</text>')
    yy = 212
    for name, n in TOKENS:
        out.append(f'<text x="{bx}" y="{yy}" font-size="13.5" class="ink">{name}</text>')
        out.append(f'<text x="{x+288}" y="{yy}" font-size="12" class="mut" text-anchor="end">appeared {n}&#215;</text>')
        pw = penalty_of(n)
        out.append(f'<rect x="{bx}" y="{yy+8}" width="{pw}" height="18" rx="5" fill="#ef4444"/>')
        yy += 60
    # x-axis: penalty magnitude grows rightward from the shared origin
    ay = 326
    out.append(f'<line x1="{bx}" y1="{ay}" x2="{bx+186}" y2="{ay}" class="axis" stroke-width="1.3"/>')
    out.append(f'<line x1="{bx}" y1="{ay-4}" x2="{bx}" y2="{ay+4}" class="axis" stroke-width="1.3"/>')
    out.append(f'<path d="M {bx+186} {ay-4} L {bx+186} {ay+4} L {bx+196} {ay} Z" class="mut"/>')
    out.append(f'<text x="{bx}" y="{ay+19}" font-size="11.5" class="mut">larger penalty (more subtracted from score) &#8594;</text>')
    return out

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="46" font-size="19" font-weight="600" class="ink">Two ways to penalize repetition</text>')
svg.append('<text x="36" y="74" font-size="12.5" class="body">Each red bar is how much the penalty subtracts from a word&#8217;s score, making it less likely to be picked again.</text>')

svg += panel(36, "Frequency penalty", "scales with how many times it appeared", lambda n: UNIT * n)
svg += panel(384, "Presence penalty", "one flat cut if it appeared at all", lambda n: int(UNIT * 1.5))

svg.append('<text x="360" y="404" font-size="13.5" font-style="italic" class="sub" text-anchor="middle">Frequency hits the 3&#215; word three times as hard; presence treats 3&#215; and 1&#215; exactly the same.</text>')
svg.append("</svg>")

with open("repetition-penalties.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote repetition-penalties.svg")
