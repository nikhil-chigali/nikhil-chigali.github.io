# make_pipeline_flow.py
# Regenerate with: python make_pipeline_flow.py
# A vertical flowchart of the decoding pipeline, in the card style. The top-k/top-p
# stage is drawn as one "and / or" group, since the two rarely both fire.
from svg_theme import svg_open

W, H = 720, 612
CX, BOX_W = 360, 320
BOX_X = CX - BOX_W / 2

def box(y, h, title, sub, box_cls, tcls, scls):
    out = [f'<rect x="{BOX_X:.0f}" y="{y}" width="{BOX_W}" height="{h}" rx="12" class="{box_cls}" stroke-width="1.5"/>']
    out.append(f'<text x="{CX}" y="{y+23}" font-size="15.5" font-weight="700" class="{tcls}" text-anchor="middle">{title}</text>')
    out.append(f'<text x="{CX}" y="{y+41}" font-size="12" class="{scls}" text-anchor="middle">{sub}</text>')
    return out

def arrow(y1, y2):
    return [
        f'<line x1="{CX}" y1="{y1}" x2="{CX}" y2="{y2-8:.0f}" stroke="#94a3b8" stroke-width="2"/>',
        f'<path d="M {CX-6} {y2-9:.0f} L {CX+6} {y2-9:.0f} L {CX} {y2-1:.0f} Z" fill="#94a3b8"/>',
    ]

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="44" font-size="19" font-weight="600" class="ink">The decoding pipeline</text>')
svg.append('<text x="36" y="66" font-size="13" class="mut">from one set of raw scores to a single sampled token</text>')

NEUTRAL = ("panel bdr", "ink", "sub")

svg += box(90, 52, "raw logits", "one score per vocab token", *NEUTRAL)
svg += arrow(142, 168)
svg += box(168, 52, "&#247; temperature&#160;&#160;(T)", "reshape: sharpen or flatten", "heat", "heattx", "heatsub")
svg += arrow(220, 246)
svg += box(246, 52, "softmax", "scores &#8594; probabilities", *NEUTRAL)
svg += arrow(298, 324)

# filter group: top-k and/or top-p
gy = 324
svg.append(f'<rect x="{BOX_X:.0f}" y="{gy}" width="{BOX_W}" height="72" rx="12" class="filt" stroke-width="1.5"/>')
for px, label in [(300, "top-k"), (420, "top-p")]:
    svg.append(f'<rect x="{px-32}" y="{gy+14}" width="64" height="26" rx="13" fill="#6366f1"/>')
    svg.append(f'<text x="{px}" y="{gy+31}" font-size="13.5" font-weight="700" fill="#ffffff" text-anchor="middle">{label}</text>')
svg.append(f'<text x="{CX}" y="{gy+32}" font-size="12.5" font-style="italic" fill="#6366f1" text-anchor="middle">and / or</text>')
svg.append(f'<text x="{CX}" y="{gy+59}" font-size="12" class="body" text-anchor="middle">trim the unlikely tail &#183; often only one</text>')
svg += arrow(396, 422)

svg += box(422, 52, "renormalize", "rescale survivors to sum to 1", *NEUTRAL)
svg += arrow(474, 500)
# box 6: sample (climax, solid indigo) — literal accent, reads on both themes
svg.append(f'<rect x="{BOX_X:.0f}" y="500" width="{BOX_W}" height="52" rx="12" fill="#6366f1"/>')
svg.append(f'<text x="{CX}" y="523" font-size="15.5" font-weight="700" fill="#ffffff" text-anchor="middle">sample</text>')
svg.append(f'<text x="{CX}" y="541" font-size="12" fill="#c7d2fe" text-anchor="middle">one weighted roll on the strip</text>')
svg += arrow(552, 576)
svg.append(f'<text x="{CX}" y="596" font-size="13.5" font-weight="600" class="ink" text-anchor="middle">the next word you read</text>')

svg.append("</svg>")
with open("pipeline-flow.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote pipeline-flow.svg")
