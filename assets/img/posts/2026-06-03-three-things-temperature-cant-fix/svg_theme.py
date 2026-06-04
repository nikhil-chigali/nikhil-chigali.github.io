# svg_theme.py
# Shared light/dark theme for the post's SVG diagrams.
# Card, text, panels, and tints adapt to prefers-color-scheme; saturated accents stay literal.
# svg_open() also writes width/height (not just viewBox) so Chirpy's lazy-load sizes the image.

STYLE = """<style>
.bg{fill:#ffffff}.bdr{stroke:#e2e8f0}
.ink{fill:#1e293b}.inks{stroke:#1e293b}
.body{fill:#475569}.sub{fill:#64748b}.mut{fill:#94a3b8}
.panel{fill:#f8fafc}.grid{stroke:#f1f5f9}.axis{stroke:#cbd5e1}
.warn{fill:#fef2f2;stroke:#fecaca}.good{fill:#f0fdf4;stroke:#bbf7d0}
.heat{fill:#fff7ed;stroke:#fed7aa}.heattx{fill:#c2410c}.heatsub{fill:#b45309}
.pillw{fill:#fee2e2}.pillwtx{fill:#b91c1c}.pillg{fill:#dcfce7}.pillgtx{fill:#15803d}
.cjunk{fill:#f1f5f9}.cjunktx{fill:#475569}.cmore{fill:#ffffff;stroke:#cbd5e1}.cmoretx{fill:#64748b}
.filt{fill:#eef2ff;stroke:#c7d2fe}
@media (prefers-color-scheme:dark){
.bg{fill:#1f2430}.bdr{stroke:#39414f}
.ink{fill:#e6e9f0}.inks{stroke:#e6e9f0}
.body{fill:#c2cad8}.sub{fill:#aab2c2}.mut{fill:#8b93a5}
.panel{fill:#272d3a}.grid{stroke:#2a3140}.axis{stroke:#525a6b}
.warn{fill:#3a2527;stroke:#5e3a3d}.good{fill:#1e3328;stroke:#356048}
.heat{fill:#3a2a1b;stroke:#6b4a2a}.heattx{fill:#fdba74}.heatsub{fill:#e8a06a}
.pillw{fill:#4a2527}.pillwtx{fill:#fca5a5}.pillg{fill:#1f3a2a}.pillgtx{fill:#86efac}
.cjunk{fill:#2b3140}.cjunktx{fill:#aeb6c6}.cmore{fill:#1f2430;stroke:#475063}.cmoretx{fill:#9aa3b5}
.filt{fill:#262b40;stroke:#434b73}
}
</style>"""

def svg_open(W, H):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f"font-family=\"-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif\">\n"
        + STYLE
    )
