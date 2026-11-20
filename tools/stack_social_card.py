"""The stack's link-preview card, shared by every toolkit's site: the 1200x630 image (og:image, twitter:card) of a
landing page — the logo beside the site's name, tagline and URL.

A site's make_social_card.py supplies its own logo, text and URL colour and calls `social_card`. Another toolkit's
site imports this module from this repository at a pinned commit and never keeps a copy."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
INK, MUTED, BG = (32, 33, 36), (95, 99, 104), (255, 255, 255)


def font(names, size):
    for n in names:
        for d in ("/usr/share/fonts/opentype/inter", "/usr/share/fonts/truetype/dejavu"):
            p = Path(d) / n
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size)


def social_card(out, logo, title, tagline, url, url_fill):
    """Write the card to `out`: `logo` (an RGBA image 360 px wide) at the left, then `title`, the lines of
    `tagline` and `url` in the colour `url_fill`."""
    card = Image.new("RGBA", (W, H), BG)
    card.alpha_composite(logo, (60, (H - logo.height) // 2))
    d = ImageDraw.Draw(card)
    x = 60 + logo.width + 40
    size = 60   # the largest title that fits the card with a 60 px margin
    while d.textlength(title, font=font(["Inter-Bold.otf", "DejaVuSans-Bold.ttf"], size)) > W - x - 60:
        size -= 2
    d.text((x, 160), title, font=font(["Inter-Bold.otf", "DejaVuSans-Bold.ttf"], size), fill=INK)
    body = font(["Inter-Regular.otf", "DejaVuSans.ttf"], 30)
    for i, line in enumerate(tagline):
        d.text((x, 262 + 46 * i), line, font=body, fill=MUTED)
    d.text((x, 452), url, font=font(["Inter-Medium.otf", "DejaVuSans.ttf"], 30), fill=url_fill)
    card.convert("RGB").save(out, optimize=True)
    print("wrote", out)
