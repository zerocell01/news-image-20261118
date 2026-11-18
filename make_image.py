#!/usr/bin/env python3
"""Compose the day-in-one-picture cover: 1024x1024 PNG, no network."""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
INK = (245, 245, 242)
DIM = (168, 176, 190)
RED = (226, 62, 54)
NIGHT_TOP = (9, 11, 16)
NIGHT_BOT = (22, 29, 40)

F_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def gradient():
    img = Image.new("RGB", (W, H), NIGHT_TOP)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(
            round(NIGHT_TOP[0] + (NIGHT_BOT[0] - NIGHT_TOP[0]) * t),
            round(NIGHT_TOP[1] + (NIGHT_BOT[1] - NIGHT_TOP[1]) * t),
            round(NIGHT_TOP[2] + (NIGHT_BOT[2] - NIGHT_TOP[2]) * t),
        ))
    return img


def glow(img, xy, radius, colour, strength=120):
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse([x - radius, y - radius, x + radius, y + radius], fill=colour)
    layer = layer.filter(ImageFilter.GaussianBlur(radius // 2))
    return Image.blend(img, Image.blend(img, layer, strength / 255), 1.0)


def bridge(d):
    """Stylised bridge: two steel trusses, the middle span torn out."""
    deck_y = 300
    water_y = 320
    d.rectangle([0, water_y, W, H], fill=(12, 17, 25))
    d.line([(0, water_y), (W, water_y)], fill=(44, 54, 70), width=2)
    for i in range(40):
        y = water_y + i * 3
        d.line([(40, y), (W - 40, y)], fill=(12 + i // 6, 17 + i // 5, 25 + i // 4))
    # piers
    for px in (150, 300, 724, 874):
        d.rectangle([px - 13, deck_y - 6, px + 13, water_y + 26], fill=(24, 30, 40))
    # standing spans (left and right), truss diagonals
    for start, end in ((60, 430), (594, 964)):
        d.rectangle([start, deck_y - 10, end, deck_y + 8], fill=(38, 46, 58))
        span = end - start
        for k in range(span // 26):
            x0 = start + k * 26
            d.line([(x0, deck_y - 10), (x0 + 26, deck_y + 8)], fill=(56, 66, 82), width=3)
            d.line([(x0, deck_y + 8), (x0 + 26, deck_y - 10)], fill=(56, 66, 82), width=3)
        d.line([(start, deck_y - 34), (end, deck_y - 34)], fill=(52, 61, 76), width=3)
    # broken span: jagged stubs sagging into the water
    d.polygon([(430, deck_y - 10), (470, deck_y + 4), (452, water_y + 30), (430, water_y + 30)],
              fill=(46, 54, 68))
    d.polygon([(594, deck_y - 10), (556, deck_y + 6), (572, water_y + 30), (594, water_y + 30)],
              fill=(46, 54, 68))
    # snapped rails
    for dy in (-2, 4):
        d.line([(430, deck_y + dy), (470, water_y + 26)], fill=RED, width=2)
        d.line([(594, deck_y + dy), (556, water_y + 26)], fill=RED, width=2)
    # fire at the gap and smoke plumes
    rnd = random.Random(7)
    for i in range(90):
        cx = rnd.gauss(512, 44)
        cy = rnd.gauss(288, 30) - abs(rnd.gauss(0, 24))
        r = rnd.randint(6, 26)
        shade = rnd.randint(150, 235)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(shade, shade // 2 + 30, 40))
    for i in range(46):
        cx = rnd.gauss(512, 52)
        cy = rnd.gauss(238, 52)
        r = rnd.randint(9, 28)
        g = rnd.randint(28, 60)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(g, g + 2, g + 6))


def masthead(d):
    d.text((56, 46), "THE DAY IN ONE PICTURE", font=font(F_BOLD, 30), fill=RED)
    right = "WEDNESDAY 18 NOVEMBER 2026"
    f = font(F_REG, 19)
    d.text((W - 56 - d.textlength(right, font=f), 52), right, font=f, fill=DIM)
    d.line([(56, 88), (W - 56, 88)], fill=(70, 78, 92), width=2)


def headline(d):
    y = 438
    d.text((52, y), "CRIMEAN", font=font(F_BOLD, 120), fill=INK)
    d.text((52, y + 106), "BRIDGE CUT", font=font(F_BOLD, 120), fill=INK)
    d.text((52, y + 212), "IN TWO", font=font(F_BOLD, 120), fill=RED)
    d.rectangle([56, y + 338, 132, y + 348], fill=RED)


def deck(d):
    body = ("Ukraine's seven-stage missile and drone attack drops a span of Putin's "
            "bridge over the Kerch Strait; Russia strikes Kyiv's bridges in reply.")
    f = font(F_REG, 23)
    wrap = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    words, lines, cur = body.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if wrap.textlength(trial, font=f) <= W - 112:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    y = 792
    for ln in lines:
        d.text((56, y), ln, font=f, fill=(214, 220, 230))
        y += 30


def also(d):
    items = [
        "Trump, Xi and Putin meet in Shenzhen as a spy scandal bites China's AI plans",
        "US loses measles elimination status after 26 years and 5,400 cases",
        "Democrats take the Alaska Senate race, two weeks after the midterms",
        "Ghana's new $60m presidential jet stirs anger over the cost of living",
    ]
    f = font(F_REG, 17)
    d.text((56, 872), "ALSO TODAY", font=font(F_BOLD, 17), fill=(120, 128, 142))
    cols = [(56, 0, 1), (536, 0, 2)]
    y = [900, 900]
    for idx, txt in enumerate(items):
        col = 0 if idx < 2 else 1
        x = 56 if col == 0 else 536
        n = idx + 1
        d.text((x, y[col]), f"{n}", font=font(F_BOLD, 17), fill=RED)
        words, cur, lines = txt.split(), "", []
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=f) <= 380:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        for ln in lines:
            d.text((x + 22, y[col]), ln, font=f, fill=(148, 156, 170))
            y[col] += 20
        y[col] += 8


def main():
    img = gradient()
    img = glow(img, (512, 290), 260, (120, 62, 26), 80)
    img = glow(img, (512, 190), 220, (58, 68, 92), 60)
    d = ImageDraw.Draw(img)
    bridge(d)
    masthead(d)
    d.line([(56, 414), (W - 56, 414)], fill=(72, 80, 96), width=2)
    headline(d)
    deck(d)
    also(d)
    d.line([(56, 998), (W - 56, 998)], fill=(52, 58, 70), width=1)
    d.text((56, 1004), "one image, a day's world news · make.fun · news-image-20261118", font=font(F_REG, 14), fill=(92, 100, 114))
    img.save("entry.png", "PNG", optimize=True)


if __name__ == "__main__":
    main()
