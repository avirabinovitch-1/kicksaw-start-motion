#!/usr/bin/env python3
"""Draws numbered click markers on screenshots, the way the Neo walkthrough guide did.

  python3 mark.py marks.json

marks.json is a list of shots:
  [{"src": "raw/01-lead.png", "out": "shots/s1a.jpg",
    "crop": [x, y, w, h],                      optional, applied first, in source pixels
    "width": 1483,                             optional, resize after cropping
    "marks": [{"n": 1, "box": [x, y, w, h]}]}] box is in source pixels (before crop and resize)

Each mark is an orange rounded outline around the thing to click, with its number in an orange
circle on the top-left corner. Numbers match the numbered instructions above the screenshot.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ORANGE = (232, 89, 12)

def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/Library/Fonts/Arial Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def mark(shot, base="."):
    im = Image.open(os.path.join(base, shot["src"])).convert("RGB")
    ox = oy = 0
    if shot.get("crop"):
        x, y, w, h = shot["crop"]; im = im.crop((x, y, x + w, y + h)); ox, oy = x, y
    scale = 1.0
    if shot.get("width") and shot["width"] != im.width:
        scale = shot["width"] / im.width
        im = im.resize((shot["width"], round(im.height * scale)), Image.LANCZOS)
    # Draw at 2x and scale down so outlines and circles are smooth.
    big = im.resize((im.width * 2, im.height * 2), Image.LANCZOS); d = ImageDraw.Draw(big)
    unit = max(im.width / 1483, 0.6) * 2          # sizes were tuned on 1483px-wide screenshots
    r = round(20 * unit); line = max(round(4.5 * unit), 3); f = font(round(25 * unit))
    for m in shot.get("marks", []):
        x, y, w, h = [(v - o) * scale * 2 for v, o in zip(m["box"], (ox, oy, 0, 0))]
        pad = 4 * unit
        d.rounded_rectangle((x - pad, y - pad, x + w + pad, y + h + pad), radius=round(7 * unit), outline=ORANGE, width=line)
        cx, cy = x - pad, y - pad
        cx = min(max(cx, r + 2), big.width - r - 2); cy = min(max(cy, r + 2), big.height - r - 2)
        d.ellipse((cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3), fill=(255, 255, 255))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE)
        d.text((cx, cy), str(m["n"]), font=f, fill=(255, 255, 255), anchor="mm")
    out = os.path.join(base, shot["out"]); os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    big.resize(im.size, Image.LANCZOS).save(out, quality=88)
    return out, im.size

if __name__ == "__main__":
    spec = sys.argv[1]; base = os.path.dirname(os.path.abspath(spec))
    for s in json.load(open(spec)):
        out, size = mark(s, base); print(f"{out}  {size[0]}x{size[1]}  {len(s.get('marks', []))} marks")
