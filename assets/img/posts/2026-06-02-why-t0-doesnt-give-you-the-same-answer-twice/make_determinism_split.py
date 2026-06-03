# make_determinism_split.py
# Regenerate with: python make_determinism_split.py
# The post's thesis as one card: T=0 settles sampling (argmax given fixed logits),
# but says nothing about whether those logits are the same list across runs.
from svg_theme import svg_open

W, H = 720, 430
svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="44" font-size="19" font-weight="600" class="ink">Two kinds of determinism</text>')
svg.append('<text x="36" y="66" font-size="13" class="mut">T = 0 locks the choice given the scores — not the scores themselves</text>')

# top node: T=0 take the argmax
svg.append('<rect x="270" y="92" width="180" height="44" rx="10" class="filt" stroke-width="1.5"/>')
svg.append('<text x="360" y="119" font-size="14.5" font-weight="700" class="ink" text-anchor="middle">T = 0: take the argmax</text>')

# connectors fanning out to the two panels
svg.append('<path d="M 360 136 L 360 154 L 180 154 L 180 172" fill="none" class="axis" stroke-width="1.5"/>')
svg.append('<path d="M 360 136 L 360 154 L 540 154 L 540 172" fill="none" class="axis" stroke-width="1.5"/>')

# left panel: sampling determinism (settled / good)
lx = 36
svg.append(f'<rect x="{lx}" y="172" width="288" height="210" rx="12" class="good" stroke-width="1.5"/>')
svg.append(f'<circle cx="{lx+32}" cy="204" r="13" fill="#22c55e"/>')
svg.append(f'<text x="{lx+32}" y="209" font-size="15" font-weight="700" fill="#ffffff" text-anchor="middle">&#10003;</text>')
svg.append(f'<text x="{lx+54}" y="210" font-size="16.5" font-weight="700" class="ink">Sampling determinism</text>')
svg.append(f'<text x="{lx+24}" y="246" font-size="13.5" class="body">Given one fixed list of logits,</text>')
svg.append(f'<text x="{lx+24}" y="268" font-size="13.5" class="body">the argmax is a fixed fact.</text>')
svg.append(f'<text x="{lx+24}" y="302" font-size="13.5" class="body">Same scores in &#8594; same token out,</text>')
svg.append(f'<text x="{lx+24}" y="324" font-size="13.5" class="body">every single run.</text>')
svg.append(f'<text x="{lx+24}" y="360" font-size="13" font-style="italic" class="sub">Settled. This part really is deterministic.</text>')

# right panel: inference determinism (open / warn)
rx = 396
svg.append(f'<rect x="{rx}" y="172" width="288" height="210" rx="12" class="warn" stroke-width="1.5"/>')
svg.append(f'<circle cx="{rx+32}" cy="204" r="13" fill="#f59e0b"/>')
svg.append(f'<text x="{rx+32}" y="209" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">?</text>')
svg.append(f'<text x="{rx+54}" y="210" font-size="16.5" font-weight="700" class="ink">Inference determinism</text>')
svg.append(f'<text x="{rx+24}" y="246" font-size="13.5" class="body">Are the logits themselves the</text>')
svg.append(f'<text x="{rx+24}" y="268" font-size="13.5" class="body">same list on every run?</text>')
svg.append(f'<text x="{rx+24}" y="302" font-size="13.5" class="body">In production, not guaranteed —</text>')
svg.append(f'<text x="{rx+24}" y="324" font-size="13.5" class="body">the scores can wobble.</text>')
svg.append(f'<text x="{rx+24}" y="360" font-size="13" font-style="italic" class="sub">Here is where &#8220;same answer twice&#8221; breaks.</text>')

svg.append('<text x="360" y="410" font-size="13.5" font-style="italic" class="sub" text-anchor="middle">T = 0 fixes the draw, but says nothing about the scores it draws from.</text>')
svg.append("</svg>")

with open("determinism-split.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote determinism-split.svg")
