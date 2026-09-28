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
import re
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
MARGIN = 1.0        # breathing room inside the viewBox

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

# Numbers per command. H and V take one, which is why pairing every number in a
# path would misplace everything after the first of either.
_ARGS = {"M": 2, "L": 2, "T": 2, "S": 4, "Q": 4, "C": 6, "H": 1, "V": 1, "Z": 0}


def path_points(d):
    """Every point a path names, control points included.

    Only the absolute commands this module and fontTools emit are understood.
    Anything else raises rather than quietly returning the wrong box.
    """
    tokens = re.findall(r"[A-Za-z]|-?\d*\.?\d+(?:[eE][-+]?\d+)?", d)
    points, i, command, x, y = [], 0, None, 0.0, 0.0
    while i < len(tokens):
        token = tokens[i]
        if token.isalpha():
            if token.islower() and token != "z":
                raise ValueError(f"relative path command {token!r} is not supported")
            command = token.upper()
            if command not in _ARGS:
                raise ValueError(f"unsupported path command {token!r}")
            i += 1
            if command == "Z":
                command = None
            continue
        if command is None:
            raise ValueError("a number in the path has no command in front of it")
        count = _ARGS[command]
        values = [float(v) for v in tokens[i:i + count]]
        if len(values) < count:
            raise ValueError(f"path command {command!r} is missing arguments")
        i += count
        if command == "H":
            x = values[0]
        elif command == "V":
            y = values[0]
        else:
            for j in range(0, count, 2):
                x, y = values[j], values[j + 1]
                points.append((x, y))
            continue
        points.append((x, y))
    return points


def square(box):
    """Grow the shorter side around the centre. Favicons and avatars are square,
    so the icon has to be too."""
    x, y, w, h = box
    side = max(w, h)
    return x - (side - w) / 2, y - (side - h) / 2, side, side


def bounds(art, key=0.0):
    """Every point the artwork can touch, including the off-register copy and
    the die-cut edge. Control points count, which only ever pads more."""
    xs, ys = [], []
    for e in art:
        pad = e["w"] / 2 + key
        points = path_points(e["d"])
        shifts = [(0.0, 0.0)] + ([e["off"]] if e["off"] else [])
        for dx, dy in shifts:
            for x, y in points:
                xs += [x + dx - pad, x + dx + pad]
                ys += [y + dy - pad, y + dy + pad]
    return min(xs), min(ys), max(xs), max(ys)


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
def document(body, box, title, defs=""):
    x, y, w, h = (round(v, 2) for v in box)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:g} {y:g} {w:g} {h:g}" '
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
            art, _, _ = make(ink)
            if suffix == "mono":
                art = [dict(e, off=None) for e in art]
            body = render(art, ink, "currentColor" if suffix == "mono" else CORAL, key, grain)
            x0, y0, x1, y1 = bounds(art, key)
            box = (x0 - MARGIN, y0 - MARGIN,
                   x1 - x0 + 2 * MARGIN, y1 - y0 + 2 * MARGIN)
            if name == "icon":
                box = square(box)
            path = os.path.join(outdir, f"{name}-{suffix}.svg")
            open(path, "w").write(document(body, box, title, GRAIN if grain else ""))
            written.append(os.path.basename(path))
    return sorted(written)

if __name__ == "__main__":
    print("\n".join(build(sys.argv[1] if len(sys.argv) > 1 else ".")))
