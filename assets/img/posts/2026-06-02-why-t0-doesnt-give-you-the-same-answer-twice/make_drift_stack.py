# make_drift_stack.py
# Regenerate with: python make_drift_stack.py
# Three layers between a prompt and its logits; each can change the bits, so two
# identical requests need not produce the same scores.
from svg_theme import svg_open

W, H = 720, 506

LAYERS = [
    dict(tag="HARDWARE", color="#6366f1",
         cause="GPU floating-point isn't associative",
         detail="Parallel reductions sum in different orders; your batch neighbors change the kernel path."),
    dict(tag="MODEL", color="#8b5cf6",
         cause="The model under the endpoint shifts",
         detail="Providers update versions silently; Mixture-of-Experts routes tokens differently per batch."),
    dict(tag="INPUT", color="#a855f7",
         cause="Hidden context you didn't type",
         detail="Injected timestamps, user metadata, or an updated system prompt all move the logits."),
]

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="44" font-size="19" font-weight="600" class="ink">Where the logits drift</text>')
svg.append('<text x="36" y="66" font-size="13" class="mut">three layers between your prompt and the scores — each can change the bits</text>')

row_y, row_h, gap = 96, 116, 16
for i, L in enumerate(LAYERS):
    y = row_y + i * (row_h + gap)
    svg.append(f'<rect x="36" y="{y}" width="648" height="{row_h}" rx="12" class="panel bdr" stroke-width="1"/>')
    svg.append(f'<rect x="36" y="{y}" width="6" height="{row_h}" rx="3" fill="{L["color"]}"/>')
    svg.append(f'<rect x="62" y="{y+22}" width="120" height="26" rx="13" fill="{L["color"]}"/>')
    svg.append(f'<text x="122" y="{y+40}" font-size="12.5" font-weight="700" fill="#ffffff" text-anchor="middle" letter-spacing="1.2">{L["tag"]}</text>')
    svg.append(f'<text x="62" y="{y+74}" font-size="16" font-weight="700" class="ink">{L["cause"]}</text>')
    svg.append(f'<text x="62" y="{y+95}" font-size="13" class="body">{L["detail"]}</text>')

svg.append("</svg>")

with open("drift-stack.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote drift-stack.svg")
