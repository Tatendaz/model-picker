import math, os, json
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

R2 = math.sqrt(2)

# ---------------------------------------------------------------- palette
AMBER   = "#EE9B21"
INK     = "#0B0C0E"
PAPER   = "#FBFAF8"
N_DARK  = "#454B57"
N_LIGHT = "#C4C9D0"
T_DARK  = "#F2F3F5"
T_LIGHT = "#16181C"

# ---------------------------------------------------------------- geometry
def dia(cx, cy, d, fill, r=2.4, op=None):
    s = d / R2
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<rect x="{cx-s/2:.3f}" y="{cy-s/2:.3f}" width="{s:.3f}" height="{s:.3f}" '
            f'rx="{r:.3f}" transform="rotate(45 {cx:.3f} {cy:.3f})" fill="{fill}"{o}/>')

MARK_DS, MARK_GAP, MARK_R = (16, 26, 38), 5, 2.4
MARK_W = sum(MARK_DS) + MARK_GAP * 2          # 90
MARK_H = max(MARK_DS)                          # 38

def mark_body(amber, neutral, op_neutral=None):
    xs, cur = [], 0
    for d in MARK_DS:
        xs.append(cur + d / 2); cur += d + MARK_GAP
    out = []
    for i, d in enumerate(MARK_DS):
        picked = (i == 1)
        out.append(dia(xs[i], MARK_H - d / 2, d,
                       amber if picked else neutral, MARK_R,
                       None if picked else op_neutral))
    return "".join(out)

ICON_DS, ICON_GAP, ICON_R, ICON_BOX = (15, 23, 31), 6, 2.2, 64

def icon_body(amber, neutral, op_neutral=None):
    s = [d / R2 for d in ICON_DS]
    d12 = ((s[0] + s[1]) / 2 + ICON_GAP) / R2
    d23 = ((s[1] + s[2]) / 2 + ICON_GAP) / R2
    total = d12 + d23 + ICON_DS[0] / 2 + ICON_DS[2] / 2
    pad = (ICON_BOX - total) / 2
    c1x = pad + ICON_DS[0] / 2; c2x = c1x + d12; c3x = c2x + d23
    c1y = ICON_BOX - pad - ICON_DS[0] / 2; c2y = c1y - d12; c3y = c2y - d23
    return (dia(c1x, c1y, ICON_DS[0], neutral, ICON_R, op_neutral)
            + dia(c3x, c3y, ICON_DS[2], neutral, ICON_R, op_neutral)
            + dia(c2x, c2y, ICON_DS[1], amber, ICON_R))

# ---------------------------------------------------------------- type
_cache = {}
def font_at(wght, opsz=32):
    key = (wght, opsz)
    if key not in _cache:
        f = TTFont("Inter.ttf")
        _cache[key] = instancer.instantiateVariableFont(f, {"wght": wght, "opsz": opsz})
    return _cache[key]

def text_paths(s, wght, size, tracking=-0.022, x=0.0, baseline=0.0):
    f = font_at(wght)
    upm = f["head"].unitsPerEm
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    scale = size / upm
    track = tracking * size
    pen_out, pos = [], x
    for ch in s:
        gname = cmap.get(ord(ch))
        if gname is None:
            pos += size * 0.3; continue
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        tp = TransformPen(pen, Transform(scale, 0, 0, -scale, pos, baseline))
        gs[gname].draw(tp)
        d = pen.getCommands()
        if d:
            pen_out.append(d)
        pos += gs[gname].width * scale + track
    return pen_out, pos - x - track

def wordmark(size, baseline, x, ink):
    d1, w1 = text_paths("Model", 620, size, x=x, baseline=baseline)
    gapsp = size * 0.26
    d2, w2 = text_paths("Picker", 400, size, x=x + w1 + gapsp, baseline=baseline)
    body = (f'<g fill="{ink}">' + "".join(f'<path d="{d}"/>' for d in d1) + '</g>'
            f'<g fill="{ink}" opacity="0.55">' + "".join(f'<path d="{d}"/>' for d in d2) + '</g>')
    return body, w1 + gapsp + w2

# ---------------------------------------------------------------- files
def svg_doc(body, w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'width="{w:g}" height="{h:g}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    W = {}
    # marks
    W["mark-dark.svg"]  = svg_doc(mark_body(AMBER, N_DARK),  MARK_W, MARK_H, "Model Picker mark")
    W["mark-light.svg"] = svg_doc(mark_body(AMBER, N_LIGHT), MARK_W, MARK_H, "Model Picker mark")
    W["mark-mono.svg"]  = svg_doc(mark_body("currentColor", "currentColor", 0.34), MARK_W, MARK_H, "Model Picker mark")
    # icons (transparent)
    W["icon-dark.svg"]  = svg_doc(icon_body(AMBER, N_DARK),  ICON_BOX, ICON_BOX, "Model Picker icon")
    W["icon-light.svg"] = svg_doc(icon_body(AMBER, N_LIGHT), ICON_BOX, ICON_BOX, "Model Picker icon")
    W["icon-mono.svg"]  = svg_doc(icon_body("currentColor", "currentColor", 0.34), ICON_BOX, ICON_BOX, "Model Picker icon")
    # app icon with plate
    pad = 9
    inner = f'<g transform="translate({pad} {pad}) scale({(ICON_BOX-2*pad)/ICON_BOX:.5f})">{icon_body(AMBER, "#5A6170")}</g>'
    W["appicon-dark.svg"] = svg_doc(f'<rect width="64" height="64" rx="14.5" fill="#15171B"/>{inner}',
                                    64, 64, "Model Picker app icon")
    inner_l = f'<g transform="translate({pad} {pad}) scale({(ICON_BOX-2*pad)/ICON_BOX:.5f})">{icon_body(AMBER, "#B9BEC6")}</g>'
    W["appicon-light.svg"] = svg_doc(f'<rect width="64" height="64" rx="14.5" fill="#F0EEEA"/>{inner_l}',
                                     64, 64, "Model Picker app icon")
    # lockups
    for name, neutral, ink in (("lockup-dark.svg", N_DARK, T_DARK), ("lockup-light.svg", N_LIGHT, T_LIGHT)):
        size = 34.0
        cap = 0.727 * size
        baseline = MARK_H / 2 + cap / 2
        gap = 15.0
        wm, ww = wordmark(size, baseline, MARK_W + gap, ink)
        total = MARK_W + gap + ww
        W[name] = svg_doc(mark_body(AMBER, neutral) + wm, round(total, 2), MARK_H, "Model Picker")
    for k, v in W.items():
        open(os.path.join(outdir, k), "w").write(v)
    return list(W)

if __name__ == "__main__":
    import sys
    print("\n".join(build(sys.argv[1] if len(sys.argv) > 1 else "out")))
