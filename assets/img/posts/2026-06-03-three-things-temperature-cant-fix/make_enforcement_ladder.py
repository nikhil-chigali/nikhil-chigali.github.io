# make_enforcement_ladder.py
# Regenerate with: python make_enforcement_ladder.py
# A weak-to-strong ladder for getting a fixed output format. Bottom rungs only
# ask for the format; the top rungs enforce it. Rendered strongest-at-top, with
# an opened-up whitespace band at the enforcement boundary for the divider label.
from svg_theme import svg_open

W, H = 720, 496

# (label, detail, tier) ordered weakest -> strongest
RUNGS = [
    ("Prompt instruction", "“Return only JSON.” The sampler can still pick any token.", "ask"),
    ("Few-shot examples", "Show the shape; the model imitates it, but is not bound to it.", "ask"),
    ("Validate &amp; retry", "Let it answer, check the output, ask again on failure.", "check"),
    ("JSON mode", "The decoder guarantees syntactically valid JSON.", "enforce"),
    ("Constrained decoding", "Invalid tokens are masked. The model cannot break the schema.", "enforce"),
]
TIER = {"ask": "#9aa3b5", "check": "#f59e0b", "enforce": "#6366f1"}

row_h, gap, top = 64, 10, 92
div_extra, div_after = 30, 2     # extra whitespace band; divider sits before visual index 2 (from top)
n = len(RUNGS)

def yof(vis):
    # visual index 0 = top (strongest); rows at/after div_after get pushed down by the band
    return top + vis * (row_h + gap) + (div_extra if vis >= div_after else 0)

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="44" font-size="19" font-weight="600" class="ink">From asking to enforcing</text>')
svg.append('<text x="36" y="66" font-size="13" class="mut">five ways to get a fixed format, weakest at the bottom</text>')

# vertical axis arrow on the left: asks (bottom) -> enforces (top)
ax = 56
axis_bottom = yof(n - 1) + row_h
svg.append(f'<line x1="{ax}" y1="{axis_bottom}" x2="{ax}" y2="{top+6}" class="axis" stroke-width="1.5"/>')
svg.append(f'<path d="M {ax-5} {top+12} L {ax+5} {top+12} L {ax} {top+2} Z" class="mut"/>')

# rungs: strongest at top -> index reversed
for vis, (label, detail, tier) in enumerate(reversed(RUNGS)):
    y = yof(vis)
    c = TIER[tier]
    svg.append(f'<rect x="84" y="{y}" width="600" height="{row_h}" rx="10" class="panel bdr" stroke-width="1"/>')
    svg.append(f'<rect x="84" y="{y}" width="7" height="{row_h}" rx="3" fill="{c}"/>')
    svg.append(f'<rect x="108" y="{y+19}" width="74" height="26" rx="13" fill="{c}"/>')
    svg.append(f'<text x="145" y="{y+37}" font-size="11.5" font-weight="700" fill="#ffffff" text-anchor="middle" letter-spacing="0.5">{tier.upper()}</text>')
    svg.append(f'<text x="198" y="{y+30}" font-size="15.5" font-weight="700" class="ink">{label}</text>')
    svg.append(f'<text x="198" y="{y+50}" font-size="12.5" class="body">{detail}</text>')

# divider centered in the whitespace band; only the top two rungs guarantee the format
band_top = yof(div_after - 1) + row_h     # bottom of last "above" rung (JSON mode)
band_bot = yof(div_after)                  # top of first "below" rung (Validate & retry)
div_y = (band_top + band_bot) / 2
svg.append(f'<line x1="84" y1="{div_y:.0f}" x2="684" y2="{div_y:.0f}" class="axis" stroke-width="1.5" stroke-dasharray="5 4"/>')
svg.append(f'<text x="684" y="{div_y-9:.0f}" font-size="12" font-style="italic" class="sub" text-anchor="end">above: the format is guaranteed &#183; below: it can still break</text>')

svg.append("</svg>")

with open("enforcement-ladder.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote enforcement-ladder.svg")
