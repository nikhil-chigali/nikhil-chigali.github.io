# make_consistency_correctness.py
# Regenerate with: python make_consistency_correctness.py
# A 2x2 with the axes outside the grid. The y-axis IS the temperature dial,
# pointing down (lower T); the x-axis is correctness, pointing right (driven by
# RAG / tools / guardrails). Lowering T walks you DOWN into a consistent cell,
# but never RIGHT into a correct one. Bottom-left (consistent & wrong) is the trap.
from svg_theme import svg_open

W, H = 720, 474
X0, Y0, PW, PH = 216, 116, 392, 268
XM, YM = X0 + PW / 2, Y0 + PH / 2
QX, QY = PW / 4, PH / 4                    # quarter offsets -> cell centers

svg = [svg_open(W, H)]
svg.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" class="bg bdr" stroke-width="2"/>')
svg.append('<text x="36" y="46" font-size="19" font-weight="600" class="ink">Consistency is not correctness</text>')

# quadrant tints: low T (consistent) is the bottom row, so the trap/goal sit at the bottom
svg.append(f'<rect x="{X0}" y="{Y0}" width="{PW/2}" height="{PH/2}" class="panel" stroke="none"/>')          # top-left  varies & wrong
svg.append(f'<rect x="{XM}" y="{Y0}" width="{PW/2}" height="{PH/2}" class="panel" stroke="none"/>')          # top-right varies & right
svg.append(f'<rect x="{X0}" y="{YM}" width="{PW/2}" height="{PH/2}" class="warn" stroke="none"/>')           # bot-left  consistent & wrong
svg.append(f'<rect x="{XM}" y="{YM}" width="{PW/2}" height="{PH/2}" class="good" stroke="none"/>')           # bot-right consistent & correct

# frame + center cross
svg.append(f'<rect x="{X0}" y="{Y0}" width="{PW}" height="{PH}" rx="4" class="bdr" fill="none" stroke-width="1.5"/>')
svg.append(f'<line x1="{XM}" y1="{Y0}" x2="{XM}" y2="{Y0+PH}" class="bdr" stroke-width="1.5"/>')
svg.append(f'<line x1="{X0}" y1="{YM}" x2="{X0+PW}" y2="{YM}" class="bdr" stroke-width="1.5"/>')

# cell labels, centered in each cell
svg.append(f'<text x="{X0+QX}" y="{Y0+QY+5}" font-size="13" class="sub" text-anchor="middle">varies &amp; wrong</text>')
svg.append(f'<text x="{XM+QX}" y="{Y0+QY+5}" font-size="13" class="sub" text-anchor="middle">varies &amp; right</text>')
svg.append(f'<text x="{X0+QX}" y="{YM+QY-4}" font-size="13.5" font-weight="700" fill="#dc2626" text-anchor="middle">consistent &amp; wrong</text>')
svg.append(f'<text x="{X0+QX}" y="{YM+QY+16}" font-size="11" fill="#dc2626" text-anchor="middle">same wrong answer, every user</text>')
svg.append(f'<text x="{XM+QX}" y="{YM+QY-4}" font-size="13.5" font-weight="700" fill="#15803d" text-anchor="middle">consistent &amp; correct</text>')
svg.append(f'<text x="{XM+QX}" y="{YM+QY+16}" font-size="11" fill="#15803d" text-anchor="middle">the goal</text>')

# x-axis ABOVE the grid: correctness, pointing right (green = RAG / tools / guardrails)
axy = Y0 - 24
svg.append(f'<line x1="{X0}" y1="{axy}" x2="{X0+PW-8}" y2="{axy}" stroke="#22c55e" stroke-width="2.5"/>')
svg.append(f'<path d="M {X0+PW-8} {axy-6} L {X0+PW-8} {axy+6} L {X0+PW+4} {axy} Z" fill="#22c55e"/>')
svg.append(f'<text x="{X0+2}" y="{axy-9}" font-size="13" font-weight="700" class="body">more correct &#8594;</text>')
svg.append(f'<text x="{X0+PW+4}" y="{axy-9}" font-size="11.5" font-weight="700" fill="#15803d" text-anchor="end">RAG &#183; tools &#183; guardrails</text>')

# y-axis LEFT of the grid: the temperature dial, pointing down. Labels rotated to
# run along the arrow — quality (more consistent) at the base, lever (lower T) at the head.
ayx = X0 - 22
svg.append(f'<line x1="{ayx}" y1="{Y0}" x2="{ayx}" y2="{Y0+PH-8}" stroke="#6366f1" stroke-width="2.5"/>')
svg.append(f'<path d="M {ayx-6} {Y0+PH-8} L {ayx+6} {Y0+PH-8} L {ayx} {Y0+PH+4} Z" fill="#6366f1"/>')
lblx = ayx - 13
ytop, ybot = Y0 + 66, Y0 + PH - 44
svg.append(f'<text x="{lblx}" y="{ytop}" font-size="12.5" font-weight="700" class="body" text-anchor="middle" transform="rotate(-90 {lblx} {ytop})">&#8592; more consistent</text>')
svg.append(f'<text x="{lblx}" y="{ybot}" font-size="12.5" font-weight="700" fill="#6366f1" text-anchor="middle" transform="rotate(-90 {lblx} {ybot})">lower T</text>')

# caption
svg.append(f'<text x="360" y="{Y0+PH+38}" font-size="13" font-style="italic" class="sub" text-anchor="middle">Temperature only moves you down this grid: it makes the answer consistent, not correct.</text>')
svg.append(f'<text x="360" y="{Y0+PH+58}" font-size="13" font-style="italic" class="sub" text-anchor="middle">A wrong answer at T = 0 is just reliably wrong; only RAG, tools, and guardrails move you right.</text>')
svg.append("</svg>")

with open("consistency-correctness.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("wrote consistency-correctness.svg")
