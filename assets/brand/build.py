#!/usr/bin/env python3
"""Redraw every Model Picker logo file.

The mark is a pen circle: one stroke that overshoots and crosses itself. The
colour prints slightly off-register, the way a cheap two-colour press does, and
a cream die-cut edge lets the sticker sit on any background.

Needs fonttools and Shantell Sans:
    python3 -m venv venv && ./venv/bin/pip install fonttools
    curl -L -o Shantell.ttf \
      "https://raw.githubusercontent.com/google/fonts/main/ofl/shantellsans/ShantellSans%5BBNCE%2CINFM%2CSPAC%2Cwght%5D.ttf"
    ./venv/bin/python build.py .
"""
import os
import sys

# fontTools is imported where it is used, so the geometry in this module can be
# imported and tested without it.

FONT  = "Shantell.ttf"
LOC   = {"wght": 640, "BNCE": 45, "INFM": 35, "SPAC": 20}
CORAL = "#F2542D"   # the circle
INK   = "#1C1B19"   # the pen
PAPER = "#FAF4E6"   # the sticker
OFF   = (2.6, -2.8) # off-register shift, in user units
KEY   = 11.0        # half-width of the die-cut edge

# ---------------------------------------------------------------- type
_cache = {}
def _font():
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    if FONT not in _cache:
        f = TTFont(FONT)
        axes = {a.axisTag for a in f["fvar"].axes}
        _cache[FONT] = instancer.instantiateVariableFont(
            f, {a: v for a, v in LOC.items() if a in axes})
    return _cache[FONT]

def glyphs(text, size, tracking=0.0, x=0.0, baseline=0.0):
    from fontTools.misc.transform import Transform
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    f = _font()
    upm = f["head"].unitsPerEm
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    sc, tr = size / upm, tracking * size
    out, pos = [], x
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            pos += size * 0.30
            continue
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        gs[name].draw(TransformPen(pen, Transform(sc, 0, 0, -sc, pos, baseline)))
        d = pen.getCommands()
        if d:
            out.append(d)
        pos += gs[name].width * sc + tr
    return out, pos - x - tr

# ---------------------------------------------------------------- drawing
def el(d, kind="stroke", w=5.0, col=None, off=None):
    return dict(d=d, kind=kind, w=w, col=col, off=off)

def _draw(e, col, extra=0.0):
    if e["kind"] == "fill":
        s = f' stroke="{col}" stroke-width="{extra:.1f}" stroke-linejoin="round"' if extra else ""
        return f'<path d="{e["d"]}" fill="{col}"{s}/>'
    return (f'<path d="{e["d"]}" fill="none" stroke="{col}" stroke-width="{e["w"]+extra:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')

def render(art, ink, accent, key=KEY, grain=False):
    offs = [e for e in art if e["off"]]
    out = []
    if key:
        for e in offs:
            dx, dy = e["off"]
            out.append(f'<g transform="translate({dx} {dy})">{_draw(e, PAPER, key*2)}</g>')
        for e in art:
            out.append(_draw(e, PAPER, key*2))
    shifted = []
    for e in offs:
        dx, dy = e["off"]
        shifted.append(f'<g transform="translate({dx} {dy})">{_draw(e, accent)}</g>')
    if shifted:
        out.append(f'<g filter="url(#gr)">{"".join(shifted)}</g>' if grain else "".join(shifted))
    for e in art:
        out.append(_draw(e, e["col"] or ink))
    return "".join(out)

GRAIN = ('<defs><filter id="gr" x="-20%" y="-20%" width="140%" height="140%">'
         '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7" result="n"/>'
         '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  '
         '0 0 0 -1.1 1.05" result="a"/>'
         '<feComposite in="SourceGraphic" in2="a" operator="in"/></filter></defs>')

# ---------------------------------------------------------------- the mark
def pen_loop(cx, cy, rx, ry):
    """One pen stroke round an ellipse. It overshoots the start and crosses itself."""
    return (f"M{cx+rx*0.86:.1f} {cy-ry*0.34:.1f} "
            f"C{cx+rx*0.90:.1f} {cy-ry*0.98:.1f} {cx+rx*0.22:.1f} {cy-ry*1.16:.1f} {cx-rx*0.38:.1f} {cy-ry*1.02:.1f} "
            f"C{cx-rx*1.06:.1f} {cy-ry*0.86:.1f} {cx-rx*1.14:.1f} {cy+ry*0.40:.1f} {cx-rx*0.52:.1f} {cy+ry*0.92:.1f} "
            f"C{cx-rx*0.06:.1f} {cy+ry*1.26:.1f} {cx+rx*0.78:.1f} {cy+ry*1.10:.1f} {cx+rx*1.02:.1f} {cy+ry*0.40:.1f} "
            f"C{cx+rx*1.16:.1f} {cy-ry*0.12:.1f} {cx+rx*0.98:.1f} {cy-ry*0.76:.1f} {cx+rx*0.48:.1f} {cy-ry*1.08:.1f}")

TICK = "M24 34 C29 40.5 32 44 34.5 46.5 C40 37 46.5 27.5 54 20.5"

def lockup(ink=INK):
    size, base, pad = 52.0, 60.0, 26.0
    a, w1 = glyphs("model", size, -0.005, pad, base)
    x2 = pad + w1 + size*0.30
    b, w2 = glyphs("picker", size, -0.005, x2, base)
    art = [el(d, "fill", 0, ink) for d in a] + [el(d, "fill", 0, ink) for d in b]
    art.append(el(pen_loop(x2 + w2/2, base - size*0.26, w2*0.64, size*0.58),
                  "stroke", 5.2, ink, off=OFF))
    return art, x2 + w2 + pad + 16, base + size*0.36 + 18

def icon(ink=INK):
    return [el(pen_loop(39, 35, 26, 24), "stroke", 5.6, ink, off=(3.0, -3.0)),
            el(TICK, "stroke", 6.0, ink)], 78, 74

# ---------------------------------------------------------------- files
def document(body, w, h, title, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'width="{w:g}" height="{h:g}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{defs}{body}\n</svg>\n')

def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    written = []
    for name, make, title in (("lockup", lockup, "Model Picker"),
                              ("icon",   icon,   "Model Picker icon")):
        for suffix, ink, key, grain in (("sticker",       INK,            KEY, False),
                                        ("sticker-grain", INK,            KEY, True),
                                        ("light",         INK,            0,   False),
                                        ("dark",          PAPER,          0,   False),
                                        ("mono",          "currentColor", 0,   False)):
            art, w, h = make(ink)
            if suffix == "mono":
                art = [dict(e, off=None) for e in art]
            body = render(art, ink, "currentColor" if suffix == "mono" else CORAL, key, grain)
            path = os.path.join(outdir, f"{name}-{suffix}.svg")
            open(path, "w").write(document(body, w, h, title, GRAIN if grain else ""))
            written.append(os.path.basename(path))
    return sorted(written)

if __name__ == "__main__":
    print("\n".join(build(sys.argv[1] if len(sys.argv) > 1 else ".")))
