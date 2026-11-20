# make_social_card.py — the 1200×630 link-preview image (og:image, twitter:card)
# of the landing page: the logo beside the site's name, tagline and URL.
#
#   pixi run social-card        (needs inkscape on PATH to rasterize the logo)
#
# Writes ../icons/social-card.png. The text matches index.html's <title> and
# description; regenerate when either changes. The card's layout is the
# stack's (stack_social_card.py, shared with the other toolkits' sites).
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

from stack_social_card import social_card

HERE = Path(__file__).resolve().parent
ICONS = HERE.parent / "icons"
TITLE = "Visual Geometry Toolkit"
TAGLINE = ["Julia packages for multiple-view geometry:",
           "cameras, features, robust estimation,",
           "fiducial markers and calibration"]
URL = "visualgeometrytoolkit.github.io"

with tempfile.TemporaryDirectory() as tmp:
    png = Path(tmp) / "logo.png"
    subprocess.run(["inkscape", str(ICONS / "vgt_logo.svg"), "--export-type=png",
                    f"--export-filename={png}", "--export-width=360"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logo = Image.open(png).convert("RGBA")

social_card(ICONS / "social-card.png", logo, TITLE, TAGLINE, URL, (203, 60, 51))
