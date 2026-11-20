"""The stack's icon tile, shared by every toolkit's site: a 96x96 SVG on one rounded tile, its light and dark
colours switched inside the file with prefers-color-scheme, so an icon works as an <img>, as a mermaid image node
and as the favicon.

The tile itself is transparent (no fill, no border), so an icon sits on whatever background the page has, light or dark.

A site's make_icons.py defines its icons as data — `icons[key] = (title, body)`, the body drawn with the classes of
STYLE (.s the structure stroke, .a the accent stroke, .fs and .fa their fills, .d dashed, .lt and .dk the light-only
and dark-only parts) — and calls `write_icons(icons, out)`. Another toolkit's site imports this module from this
repository at a pinned commit and never keeps a copy."""
import math

STYLE = """<style>
.t{fill:none;stroke:none}
.s{fill:none;stroke:#2b5d7d;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.a{fill:none;stroke:#d4622a;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.d{stroke-dasharray:1 7}
.fs{fill:#2b5d7d}.fa{fill:#d4622a}
.dk{display:none}
@media (prefers-color-scheme: dark){
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
    ang = math.atan2(y2 - y1, x2 - x1)
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    return (f'<path class="{cls}" d="M{x1},{y1} L{x2},{y2} '
            f'M{x2 + head*math.cos(a1):.1f},{y2 + head*math.sin(a1):.1f} L{x2},{y2} '
            f'L{x2 + head*math.cos(a2):.1f},{y2 + head*math.sin(a2):.1f}"/>')


def write_icons(icons, out):
    """Write `<key>.svg` into the directory `out` for each `key: (title, body)` of `icons`."""
    for key, (title, body) in icons.items():
        (out / f"{key}.svg").write_text(svg(body, title))
