#!/usr/bin/env python3
"""og.png for Bull Creek Fish Camp — 1200x630 share card.
Cypress green + creek teal + sun gold; wave-line bands, badge stamp. Shop identity only."""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public", "og.png")

W, H = 1200, 630
CYPRESS = (29, 49, 40)
CYPRESS2 = (39, 66, 53)
CREEK = (47, 109, 109)
CEDAR = (181, 118, 58)
SUN = (216, 178, 94)
CREAM = (233, 239, 220)
FOG = (169, 180, 147)

SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

img = Image.new("RGB", (W, H), CYPRESS)
d = ImageDraw.Draw(img)

# radial washes: teal top-right, cedar bottom-left
wash = Image.new("RGB", (W, H), CYPRESS)
wd = ImageDraw.Draw(wash)
wd.ellipse((620, -320, 1500, 420), fill=CREEK)
wd.ellipse((-320, 320, 560, 900), fill=CEDAR)
wash = wash.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(150))
blend = Image.new("RGBA", (W, H), (0, 0, 0, 92))
img = Image.composite(wash, img, blend).convert("RGB")
d = ImageDraw.Draw(img)

# top band (teal / gold / cedar) + wave line
d.rectangle((0, 0, W, 7), fill=CREEK)
d.rectangle((W * 0.40, 0, W * 0.62, 7), fill=SUN)
d.rectangle((W * 0.62, 0, W, 7), fill=CEDAR)
import math
def waved(y0, amp, color, w=5, phase=0.0, n=3):
    for seg in range(n):
        pts = [(x, y0 + amp * math.sin(x / 46.0 + phase + seg * 0.55)) for x in range(60, 641, 10)]
        d.line(pts, fill=color, width=w)
waved(486, 9, (*SUN,), 4, 0.0)
waved(506, 9, CREEK, 4, 1.0)
waved(526, 9, CEDAR, 4, 2.1)

# badge stamp
cx, cy, r = 168, 280, 92
d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=SUN, width=4)
d.ellipse((cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12), outline=CREAM, width=3)
# fish glyph
d.polygon([(cx - 52, cy - 8), (cx + 18, cy - 34), (cx + 58, cy - 8), (cx + 18, cy + 14)], fill=SUN)
d.polygon([(cx + 58, cy - 8), (cx + 92, cy - 30), (cx + 92, cy + 14), (cx + 58, cy - 8)], fill=SUN)
d.ellipse((cx - 36, cy - 18, cx - 26, cy - 8), fill=CYPRESS)
# badge waves
for i, wy in enumerate((cy + 30, cy + 46)):
    pts = [(x, wy + 7 * math.sin(x / 24.0 + i)) for x in range(cx - 62, cx + 63, 8)]
    d.line(pts, fill=CREAM, width=4)

f_serif = ImageFont.truetype(SERIF, 74)
f_sub = ImageFont.truetype(SANS, 27)
f_kick = ImageFont.truetype(SANS, 21)

x0 = 320
d.text((x0, 128), "REOPENING · BUNNELL · ON THE WATER", font=f_kick, fill=SUN)
d.text((x0, 170), "Bull Creek", font=f_serif, fill=CREAM)
d.text((x0, 250), "Fish Camp", font=f_serif, fill=CREAM)
d.line((x0, 352, x0 + 470, 352), fill=CEDAR, width=4)
d.text((x0, 372), "January 2027 — 3861 County Rd 2006 W", font=f_sub, fill=CREAM)
d.text((x0, 412), "Breakfast, lunch and dinner — by land or by boat", font=f_sub, fill=FOG)

img.save(OUT, "PNG")
print("wrote", OUT, os.path.getsize(OUT), "bytes")
