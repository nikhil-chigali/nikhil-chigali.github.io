# make_sampling_strip.py
# Regenerate with: python make_sampling_strip.py
# Visualizes sampling as one roll on a weighted strip: each token owns a slice as wide
# as its probability; a single random number in [0,1) picks the slice it lands in.
from svg_theme import svg_open

W, H = 720, 320
X0, STRIP_W = 48, 624          # strip spans probability 0..1
Y_TOP, BAR_H = 150, 54
Y_BOT = Y_TOP + BAR_H

# token, probability, fill, text color (slices sum to ~1)
TOKENS = [
    ("summer", 0.62, "#6366f1", "#ffffff"),
    ("winter", 0.27, "#818cf8", "#ffffff"),
    ("autumn", 0.10, "#a5b4fc", "#312e81"),
    ("tail",   0.01, "#e2e8f0", "#64748b"),
]
DRAW = 0.71                    # the random number we rolled (lands in winter)

def x_at(p):
    return X0 + p * STRIP_W

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="44" font-size="19" font-weight="600" class="ink">Sampling: one roll on a weighted strip</text>')
svg.append('<text x="36" y="66" font-size="13" class="mut">each token owns a slice as wide as its probability; one random number picks the slice</text>')

# segments
cum = 0.0
boundaries = []
for name, p, fill, txt in TOKENS:
    sx = x_at(cum)
    sw = p * STRIP_W
    svg.append(f'<rect x="{sx:.1f}" y="{Y_TOP}" width="{sw:.1f}" height="{BAR_H}" fill="{fill}"/>')
    if sw > 48:
        cx = sx + sw / 2
        svg.append(f'<text x="{cx:.1f}" y="{Y_TOP+26:.0f}" font-size="13.5" font-weight="600" fill="{txt}" text-anchor="middle">{name}</text>')
        svg.append(f'<text x="{cx:.1f}" y="{Y_TOP+44:.0f}" font-size="12" fill="{txt}" text-anchor="middle">{p:.2f}</text>')
    cum += p
    boundaries.append(cum)

# white separators between slices
for b in boundaries[:-1]:
    bx = x_at(b)
    svg.append(f'<line x1="{bx:.1f}" y1="{Y_TOP}" x2="{bx:.1f}" y2="{Y_BOT}" stroke="#ffffff" stroke-width="2"/>')

# scale ends
svg.append(f'<text x="{X0}" y="{Y_BOT+22}" font-size="12" class="mut" text-anchor="middle">0</text>')
svg.append(f'<text x="{x_at(1.0):.0f}" y="{Y_BOT+22}" font-size="12" class="mut" text-anchor="middle">1</text>')

# the roll: arrow dropping onto DRAW, landing marker, and result note
px = x_at(DRAW)
svg.append(f'<text x="{px:.1f}" y="104" font-size="13" font-weight="600" class="ink" text-anchor="middle">random number = {DRAW}</text>')
svg.append(f'<line x1="{px:.1f}" y1="114" x2="{px:.1f}" y2="{Y_TOP-3:.0f}" class="inks" stroke-width="1.5"/>')
svg.append(f'<path d="M {px-5:.1f} {Y_TOP-9:.0f} L {px+5:.1f} {Y_TOP-9:.0f} L {px:.1f} {Y_TOP-1:.0f} Z" class="ink"/>')
svg.append(f'<circle cx="{px:.1f}" cy="{Y_TOP+BAR_H/2:.0f}" r="5" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>')
svg.append(f'<text x="{px:.1f}" y="{Y_BOT+44:.0f}" font-size="13" class="body" text-anchor="middle">0.71 fell in winter&#8217;s slice, so <tspan font-weight="700" class="ink">winter</tspan> is drawn &#8212; not the top token</text>')

# caption
svg.append(f'<text x="360" y="{H-26}" font-size="13" font-style="italic" class="sub" text-anchor="middle">The widest slice wins most rolls, not every roll; the thin grey tail on the right still catches one now and then.</text>')

svg.append("</svg>")

with open("sampling-strip.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote sampling-strip.svg")
