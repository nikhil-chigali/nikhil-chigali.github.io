# make_topk_vs_topp.py
# Regenerate with: python make_topk_vs_topp.py
# A 2x2 card: a confident step and an uncertain step, each filtered by top-k and top-p.
# Each row names its input sequence; each cell shows the surviving tokens as chips with
# their probabilities (indigo = useful, grey = junk, outline = overflow).
from svg_theme import svg_open

W, H = 720, 540

COL1_X, COL2_X, CELL_W = 36, 368, 316
COL1_C, COL2_C = COL1_X + CELL_W / 2, COL2_X + CELL_W / 2

ROWS = [
    dict(
        model="Confident model", seq="the United States of ___",
        strip_y=116, cell_y=160,
        topk=dict(x=COL1_X, tint="warn", keep="keeps 40",
                  chips=[("America", "0.95", "good"), ("lamp", "0.0006", "junk"), ("+38", None, "more")],
                  caption="1 useful word, 39 junk"),
        topp=dict(x=COL2_X, tint="good", keep="keeps 1",
                  chips=[("America", "0.95", "good")],
                  caption="just the word that fit"),
    ),
    dict(
        model="Uncertain model", seq="I spent the weekend ___",
        strip_y=322, cell_y=366,
        topk=dict(x=COL1_X, tint="warn", keep="keeps 40",
                  chips=[("reading", "0.04", "good"), ("hiking", "0.04", "good"), ("+38", None, "more")],
                  caption="fixed 40 — 160 good ones cut"),
        topp=dict(x=COL2_X, tint="good", keep="keeps ~140",
                  chips=[("reading", "0.04", "good"), ("hiking", "0.04", "good"), ("+138", None, "more")],
                  caption="matches the real spread"),
    ),
]

TINT = {
    "warn": dict(cls="warn", icon="#f59e0b", glyph="!"),
    "good": dict(cls="good", icon="#22c55e", glyph="&#10003;"),
}
CELL_H, PAD = 142, 22

def chip_width(label):
    return len(label) * 7 + 20

def draw_cell(c):
    x, y = c["x"], c["cell_y"]
    t = TINT[c["tint"]]
    out = [f'<rect x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" rx="12" class="{t["cls"]}" stroke-width="1.5"/>']
    out.append(f'<circle cx="{x+30}" cy="{y+30}" r="12" fill="{t["icon"]}"/>')
    out.append(f'<text x="{x+30}" y="{y+35}" font-size="15" font-weight="700" fill="#ffffff" text-anchor="middle">{t["glyph"]}</text>')
    out.append(f'<text x="{x+50}" y="{y+36}" font-size="19" font-weight="700" class="ink">{c["keep"]}</text>')
    cx = x + PAD
    chip_y = y + 58
    for word, prob, kind in c["chips"]:
        label = f"{word} {prob}" if prob else word
        w = chip_width(label)
        if kind == "good":
            out.append(f'<rect x="{cx}" y="{chip_y}" width="{w}" height="24" rx="12" fill="#6366f1"/>')
            out.append(f'<text x="{cx + w/2:.1f}" y="{chip_y+16}" font-size="12.5" fill="#ffffff" text-anchor="middle">{word} <tspan fill="#c7d2fe">{prob}</tspan></text>')
        elif kind == "junk":
            out.append(f'<rect x="{cx}" y="{chip_y}" width="{w}" height="24" rx="12" class="cjunk"/>')
            out.append(f'<text x="{cx + w/2:.1f}" y="{chip_y+16}" font-size="12.5" class="cjunktx" text-anchor="middle">{word} <tspan fill="#94a3b8">{prob}</tspan></text>')
        else:  # more
            out.append(f'<rect x="{cx}" y="{chip_y}" width="{w}" height="24" rx="12" class="cmore" stroke-width="1"/>')
            out.append(f'<text x="{cx + w/2:.1f}" y="{chip_y+16}" font-size="12.5" class="cmoretx" text-anchor="middle">{word}</text>')
        cx += w + 8
    out.append(f'<text x="{x+PAD}" y="{y+116}" font-size="13" class="body">{c["caption"]}</text>')
    return out

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="42" font-size="19" font-weight="600" class="ink">Same two steps, two cutoffs</text>')
svg.append('<text x="36" y="64" font-size="13" class="mut">a confident step and an uncertain one, filtered by top-k and by top-p</text>')

# column header pills, color-coded to the cells below
hdr_y, hdr_h, hdr_w = 78, 30, 184
for cx, label, pill, txt in [
    (COL1_C, "top-k&#160;&#160;&#183;&#160;&#160;k = 40", "pillw", "pillwtx"),
    (COL2_C, "top-p&#160;&#160;&#183;&#160;&#160;p = 0.9", "pillg", "pillgtx"),
]:
    svg.append(f'<rect x="{cx-hdr_w/2:.0f}" y="{hdr_y}" width="{hdr_w}" height="{hdr_h}" rx="15" class="{pill}"/>')
    svg.append(f'<text x="{cx:.0f}" y="{hdr_y+20}" font-size="15" font-weight="700" class="{txt}" text-anchor="middle">{label}</text>')

for row in ROWS:
    sy = row["strip_y"]
    svg.append(f'<rect x="36" y="{sy}" width="648" height="36" rx="10" class="panel bdr" stroke-width="1"/>')
    svg.append(
        f'<text x="52" y="{sy+23}" font-size="13.5" class="sub">'
        f'<tspan font-weight="700" class="ink">{row["model"]}</tspan>'
        f'&#160;&#160;&#183;&#160;&#160;next word after&#160;&#160;'
        f'<tspan font-style="italic" class="ink">&#8220;{row["seq"]}&#8221;</tspan></text>'
    )
    for key in ("topk", "topp"):
        cell = dict(row[key])
        cell["cell_y"] = row["cell_y"]
        svg += draw_cell(cell)

svg.append('<text x="360" y="524" font-size="13.5" font-style="italic" class="sub" text-anchor="middle">The top-k column never moves; the top-p column tracks the model&#8217;s confidence.</text>')
svg.append("</svg>")

with open("topk-vs-topp.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote topk-vs-topp.svg")
