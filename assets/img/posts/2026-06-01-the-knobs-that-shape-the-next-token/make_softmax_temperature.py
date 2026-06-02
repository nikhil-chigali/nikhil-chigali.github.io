# make_softmax_temperature.py
# Regenerate with: python make_softmax_temperature.py
# Computes softmax at three temperatures and writes a clean, card-styled SVG.
# Color encodes heat: cool blue at low T, warm orange at high T.
import numpy as np
from svg_theme import svg_open

tokens = ["the", "a", "cat", "river", "xylophone"]
logits = np.array([2.0, 1.0, 0.5, 0.0, -1.0])

def softmax(z, T):
    z = z / T
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()

temps = [0.3, 1.0, 1.8]
colors = ["#2563eb", "#7c3aed", "#ea580c"]   # cool -> warm with rising T
probs = [softmax(logits, T) for T in temps]

W, H = 720, 470
pad_l, pad_r, pad_t, pad_b = 64, 28, 92, 64
plot_w = W - pad_l - pad_r
plot_h = H - pad_t - pad_b
y0 = pad_t + plot_h

n_groups = len(tokens)
group_w = plot_w / n_groups
bar_w = 26
gap = 6
cluster_w = 3 * bar_w + 2 * gap

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="44" font-size="19" font-weight="600" class="ink">Same logits, three temperatures</text>')
svg.append('<text x="36" y="66" font-size="13" class="mut">how temperature reshapes one fixed set of scores</text>')

for t in np.arange(0, 1.01, 0.2):
    yy = y0 - t * plot_h
    svg.append(f'<line x1="{pad_l}" y1="{yy:.1f}" x2="{W-pad_r}" y2="{yy:.1f}" class="grid" stroke-width="1"/>')
    svg.append(f'<text x="{pad_l-10}" y="{yy+4:.1f}" font-size="12" class="mut" text-anchor="end">{t:.1f}</text>')

for gi, tok in enumerate(tokens):
    gx = pad_l + gi * group_w + (group_w - cluster_w) / 2
    for bi in range(3):
        p = probs[bi][gi]
        bh = p * plot_h
        bx = gx + bi * (bar_w + gap)
        by = y0 - bh
        svg.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" height="{bh:.1f}" rx="4" fill="{colors[bi]}"/>')
    cx = gx + cluster_w / 2
    svg.append(f'<text x="{cx:.1f}" y="{y0+22:.0f}" font-size="13" class="ink" text-anchor="middle">{esc(tok)}</text>')

svg.append(f'<line x1="{pad_l}" y1="{y0}" x2="{W-pad_r}" y2="{y0}" class="axis" stroke-width="1.5"/>')

swatch_y = 40
legend_left = W - pad_r - 3 * 92
for bi, T in enumerate(temps):
    bx = legend_left + bi * 92
    svg.append(f'<rect x="{bx}" y="{swatch_y-11}" width="14" height="14" rx="3" fill="{colors[bi]}"/>')
    svg.append(f'<text x="{bx+20}" y="{swatch_y+1}" font-size="13" class="body">T = {T}</text>')

svg.append("</svg>")

with open("softmax-temperature.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote softmax-temperature.svg")
