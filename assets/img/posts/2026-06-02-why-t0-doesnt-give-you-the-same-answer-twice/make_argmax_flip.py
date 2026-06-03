# make_argmax_flip.py
# Regenerate with: python make_argmax_flip.py
# The concrete case: the top two logits sit a hair apart. A last-bit rounding
# between runs flips the argmax, so T=0 hands back a different token on the same prompt.
from svg_theme import svg_open

W, H = 720, 420

# Two runs of the same prompt. A coin flip gives the model no reason to prefer
# "heads" over "tails", so the top two logits sit a few millionths apart — well
# inside the rounding noise a different sum order produces, so the winner flips.
RUN1 = [("heads", 9.731043, True), ("tails", 9.731040, False)]
RUN2 = [("heads", 9.731041, False), ("tails", 9.731044, True)]

PANEL_W = 300
NAME_Y = [156, 212]     # baseline for each token's name + logit label
BAR_Y = [162, 218]      # top of each token's bar

def panel(x, title, rows):
    # Token name (left) and logit value (right) share a baseline, both inside the
    # panel; the bar sits just below. Winner's bar is drawn longer so the eye can
    # see who edges ahead — the near-identical logit labels carry the real story.
    out = [f'<rect x="{x}" y="92" width="{PANEL_W}" height="200" rx="12" class="panel bdr" stroke-width="1.5"/>']
    out.append(f'<text x="{x+22}" y="124" font-size="15" font-weight="700" class="ink">{title}</text>')
    for i, (name, value, win) in enumerate(rows):
        ny, by = NAME_Y[i], BAR_Y[i]
        out.append(f'<text x="{x+22}" y="{ny}" font-size="13.5" class="ink">{name}</text>')
        out.append(f'<text x="{x+PANEL_W-22}" y="{ny}" font-size="11.5" class="mut" text-anchor="end">logit {value:.6f}</text>')
        w = 232 if win else 176
        fill = "#6366f1" if win else "#9aa3b5"
        out.append(f'<rect x="{x+22}" y="{by}" width="{w}" height="22" rx="6" fill="{fill}"/>')
        if win:
            out.append(f'<text x="{x+22+w-15}" y="{by+16}" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">&#10003;</text>')
    winner = next(n for n, v, wn in rows if wn)
    out.append(f'<text x="{x+22}" y="270" font-size="13.5" class="body">argmax &#8594; <tspan font-weight="700" class="ink">{winner}</tspan></text>')
    return out

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="44" font-size="19" font-weight="600" class="ink">A margin thinner than the arithmetic</text>')
svg.append('<text x="36" y="66" font-size="13" class="mut">prompt: &#8220;I flipped a coin. It landed on&#8221;  ·  T = 0  ·  two runs, same input</text>')

svg += panel(36, "Run 1", RUN1)
svg += panel(384, "Run 2", RUN2)

# flip marker bridging the two runs
cx, cy = 360, 188
svg.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="#f59e0b"/>')
svg.append(f'<text x="{cx}" y="{cy+6}" font-size="19" font-weight="700" fill="#ffffff" text-anchor="middle">&#8644;</text>')
svg.append(f'<text x="{cx}" y="{cy+38}" font-size="11.5" font-weight="700" class="sub" text-anchor="middle" letter-spacing="0.5">FLIPS</text>')

svg.append('<text x="360" y="328" font-size="13.5" class="body" text-anchor="middle">The top two logits sit about <tspan font-weight="700" class="ink">0.000003</tspan> apart — the coin gives the model no reason to prefer one.</text>')
svg.append('<text x="360" y="352" font-size="13.5" class="body" text-anchor="middle">Re-batch the request, sum in a different order, and the last bits round the other way.</text>')
svg.append('<text x="360" y="380" font-size="13.5" font-style="italic" class="sub" text-anchor="middle">That alone flips the argmax: &#8220;heads&#8221; on one run, &#8220;tails&#8221; on the next, both at T = 0.</text>')
svg.append("</svg>")

with open("argmax-flip.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote argmax-flip.svg")
