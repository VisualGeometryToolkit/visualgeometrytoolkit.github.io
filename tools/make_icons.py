"""Build the site's package icons into ../icons (run from tools/: `pixi run icons`).

Every icon is a 96x96 SVG on the same rounded tile; light and dark colours are
switched inside the file with prefers-color-scheme, so an icon works as an
<img>, as a mermaid image node, and as the favicon. Icons derived from the
project heroes embed downscaled PNG crops (light and dark where the hero has
both)."""
import base64, io, os, pathlib
from PIL import Image

OUT = pathlib.Path(__file__).resolve().parent.parent / "icons"
OUT.mkdir(parents=True, exist_ok=True)
# Checkouts of the package repos whose landing heroes the hero-derived icons
# crop (default ~/src; override with VGT_SRC).
SRC = pathlib.Path(os.environ.get("VGT_SRC", pathlib.Path.home() / "src"))

STYLE = """<style>
.t{fill:#eef3f9;stroke:#d3deea}
.s{fill:none;stroke:#2b5d7d;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.a{fill:none;stroke:#d4622a;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.d{stroke-dasharray:1 7}
.fs{fill:#2b5d7d}.fa{fill:#d4622a}
.dk{display:none}
@media (prefers-color-scheme: dark){
.t{fill:#1c2830;stroke:#304350}
.s{stroke:#9ccbe8}.a{stroke:#f28c52}
.fs{fill:#9ccbe8}.fa{fill:#f28c52}
.lt{display:none}.dk{display:inline}
}
</style>"""

def svg(body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" role="img">'
            f'<title>{title}</title>{STYLE}'
            f'<rect class="t" x="2" y="2" width="92" height="92" rx="20" stroke-width="2"/>{body}</svg>\n')

def arrow(x1, y1, x2, y2, cls="s", head=7):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    return (f'<path class="{cls}" d="M{x1},{y1} L{x2},{y2} '
            f'M{x2 + head*math.cos(a1):.1f},{y2 + head*math.sin(a1):.1f} L{x2},{y2} '
            f'L{x2 + head*math.cos(a2):.1f},{y2 + head*math.sin(a2):.1f}"/>')

def frustum(ax, ay, cx, cy, half):
    """Side-view pinhole: apex, and an image plane of half-width `half`
    perpendicular to the axis apex->(cx, cy)."""
    import math
    dx, dy = cx - ax, cy - ay
    n = math.hypot(dx, dy); px, py = -dy / n, dx / n
    p1 = (cx + half*px, cy + half*py); p2 = (cx - half*px, cy - half*py)
    return (f'<path class="s" d="M{p1[0]:.1f},{p1[1]:.1f} L{ax},{ay} L{p2[0]:.1f},{p2[1]:.1f} Z"/>')

def frustum3d(ax, ay, quad):
    """A pinhole camera: the apex joined to the four corners of its image plane."""
    q = " ".join(f"L{x},{y}" for x, y in quad[1:])
    rays = " ".join(f"M{ax},{ay} L{x},{y}" for x, y in quad)
    return f'<path class="s" d="M{quad[0][0]},{quad[0][1]} {q} Z {rays}"/>'

icons = {}

# VisualGeometryCore: a camera frustum and its coordinate frame
icons["vgc"] = ("VisualGeometryCore.jl",
    frustum3d(32, 62, [(50, 16), (82, 24), (78, 52), (46, 44)])
    + arrow(32, 62, 32, 86, "a", 6)    # y down
    + arrow(32, 62, 10, 62, "a", 6))   # x

# VisualGeometryIo: a data file with data in and out
icons["vgio"] = ("VisualGeometryIo.jl",
    '<path class="s" d="M34,18 H56 L66,28 V78 H34 Z M56,18 V28 H66"/>'
    + '<path class="a" d="M42,42 H58 M42,52 H58 M42,62 H52"/>'
    + arrow(8, 36, 26, 36) + arrow(72, 64, 90, 64))

# VisualGeometryFeatures: keypoints with scale circles and orientations
kp = [(37, 39, 15, 0.6), (66, 63, 11, -2.2), (68, 29, 7, 2.6), (30, 72, 8, 1.2)]
body = ""
import math
for x, y, r, th in kp:
    body += f'<circle class="s" cx="{x}" cy="{y}" r="{r}"/>'
    body += f'<path class="s" d="M{x},{y} L{x + r*math.cos(th):.1f},{y + r*math.sin(th):.1f}"/>'
    body += f'<circle class="fa" cx="{x}" cy="{y}" r="3.2"/>'
icons["vgf"] = ("VisualGeometryFeatures.jl", body)

# VisualGeometryEval: benchmark bars and a target
icons["vgeval"] = ("VisualGeometryEval.jl",
    '<path class="s" d="M16,18 V80 H82"/>'
    + '<path class="s" d="M27,80 V62 H37 V80 M44,80 V50 H54 V80 M61,80 V40 H71 V80"/>'
    + '<circle class="a" cx="71" cy="22" r="11"/><circle class="fa" cx="71" cy="22" r="4"/>')

# RobustVisualGeometry: a robust line fit, inliers on it and outliers off it
inl = [(18, 70), (27, 66), (35, 59), (44, 55), (52, 47), (61, 43), (70, 35), (78, 31)]
outl = [(24, 30), (44, 22), (66, 70), (82, 58), (36, 84)]
body = '<path class="s" d="M12,75 L84,27"/>'
body += "".join(f'<circle class="fs" cx="{x}" cy="{y}" r="3.6"/>' for x, y in inl)
body += "".join(f'<circle class="fa" cx="{x}" cy="{y}" r="3.6"/>' for x, y in outl)
icons["rvg"] = ("RobustVisualGeometry.jl", body)

# PoseLib: two cameras viewing one point, linked by their relative pose
icons["poselib"] = ("PoseLib.jl",
    frustum3d(18, 68, [(16, 38), (36, 34), (40, 50), (20, 54)])
    + frustum3d(78, 68, [(80, 38), (60, 34), (56, 50), (76, 54)])
    + '<path class="a d" d="M28,43 L48,16 L68,43"/>'
    + '<circle class="fa" cx="48" cy="16" r="4.5"/>'
    + '<path class="a" d="M24,80 Q48,92 72,80"/>' + arrow(66, 83.2, 72, 80, "a", 6))

for key, (title, body) in icons.items():
    (OUT / f"{key}.svg").write_text(svg(body, title))

# Hero-derived icons
def b64png(im, size=176):
    im = im.copy(); im.thumbnail((size, size), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return im.size, base64.b64encode(buf.getvalue()).decode()

def square(im, box):
    return im.crop(box)

def hero_svg(title, light, dark=None, inset=10):
    w = 96 - 2*inset
    (lw, lh), l64 = b64png(light)
    def tag(data, cls, sz):
        iw, ih = sz; s = w / max(iw, ih); dw, dh = iw*s, ih*s
        return (f'<image class="{cls}" x="{inset + (w-dw)/2:.1f}" y="{inset + (w-dh)/2:.1f}" '
                f'width="{dw:.1f}" height="{dh:.1f}" href="data:image/png;base64,{data}"/>')
    body = tag(l64, "lt" if dark is not None else "", (lw, lh))
    if dark is not None:
        dsz, d64 = b64png(dark); body += tag(d64, "dk", dsz)
    return svg(body, title)

lodr = Image.open(SRC / "LocalOptimizationDoneRight/docs/src/assets/landing/hero_manifold.png").convert("RGBA")
lodr = lodr.crop((16, 16, 1015, 741))
(OUT / "lodr.svg").write_text(hero_svg("LocalOptimizationDoneRight.jl", lodr, inset=5))

rl = Image.open(SRC / "RansacScoringDoneRight.jl/docs/src/assets/landing/hero_scoring_light.png").convert("RGBA")
rd = Image.open(SRC / "RansacScoringDoneRight.jl/docs/src/assets/landing/hero_scoring_dark.png").convert("RGBA")
box = (330, 214, 1285, 1169)
(OUT / "rsdr.svg").write_text(hero_svg("RansacScoringDoneRight.jl", rl.crop(box), rd.crop(box), inset=7))

# BlobBoards: its landing hero, a board at the current authoring defaults
# exported by BlobBoards' own API (docs/make_hero.jl; light and dark renderings)
BB = SRC / "BlobBoards.jl/docs/src/assets/landing"
def legible(im, gamma=2.2):
    """Darken the blob gradients (luminance gamma) so the board reads at icon size."""
    l, a = im.convert("LA").split()
    l = l.point(lambda v: round(255 * (v / 255) ** gamma))
    return Image.merge("LA", (l, a)).convert("RGBA")
bl = legible(Image.open(BB / "hero_board.png"))
bd = legible(Image.open(BB / "hero_board_dark.png"))
(OUT / "blobboards.svg").write_text(hero_svg("BlobBoards.jl", bl, bd, inset=9))

for p in sorted(OUT.iterdir()):
    print(p.name, p.stat().st_size)
