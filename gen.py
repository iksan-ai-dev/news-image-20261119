#!/usr/bin/env python3
"""Draw one 1024x1024 image summing up the world news of 19 November 2026.

Flat editorial front page: one lead story (the Shenzhen trilateral summit) and a
2x2 grid of the day's other consequential stories across regions, plus a ticker.
Everything is drawn with PIL primitives so the output is deterministic bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 24
NAVY = (9, 16, 28)
PANEL = (18, 27, 44)
PANEL_HI = (24, 35, 56)
INK = (240, 244, 250)
DIM = (150, 163, 184)
GOLD = (232, 179, 58)
RED = (214, 69, 69)
TEAL = (47, 168, 160)
LINE = (38, 52, 76)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)


def f(path, size):
    return ImageFont.truetype(path, size)


def text(x, y, s, font, fill=INK):
    d.text((x, y), s, font=font, fill=fill)


def wrap(s, font, width):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(box, fill=PANEL, radius=10):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=LINE, width=2)


# ---------------------------------------------------------------- header
text(M, 20, "19 NOVEMBER 2026", f(FB, 44), INK)
kicker = "ONE DAY IN THE WORLD"
kw = d.textlength(kicker, font=f(FB, 20))
text(W - M - kw, 30, kicker, f(FB, 20), GOLD)
d.line([(M, 84), (W - M, 84)], fill=GOLD, width=3)

# ---------------------------------------------------------------- lead panel
lead = (M, 96, W - M, 566)
panel(lead)

text(M + 22, 110, "LEAD STORY", f(FB, 17), GOLD)

# three flag roundels, overlapping, centred against the text block
cy = 370
r = 50
centers = [(M + 96, cy), (M + 168, cy), (M + 240, cy)]
names = ["US", "CN", "RU"]


def roundel(cx, cy, r, draw_flag):
    m = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    tile = Image.new("RGB", (2 * r, 2 * r), (255, 255, 255))
    draw_flag(tile, 2 * r)
    img.paste(tile, (cx - r, cy - r), m)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=NAVY, width=4)


def flag_us(tile, s):
    td = ImageDraw.Draw(tile)
    stripe = s / 13
    for i in range(13):
        td.rectangle((0, i * stripe, s, (i + 1) * stripe),
                     fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    td.rectangle((0, 0, s * 0.45, stripe * 7), fill=(60, 59, 110))
    for row in range(4):
        for col in range(5):
            cx = s * 0.05 + col * s * 0.085
            cy = s * 0.10 + row * s * 0.17
            td.ellipse((cx, cy, cx + s * 0.022, cy + s * 0.022), fill=(255, 255, 255))


def flag_cn(tile, s):
    td = ImageDraw.Draw(tile)
    td.rectangle((0, 0, s, s), fill=(222, 41, 16))
    star(td, s * 0.22, s * 0.25, s * 0.15, (255, 222, 0))
    for (px, py) in ((0.42, 0.10), (0.50, 0.20), (0.50, 0.33), (0.42, 0.43)):
        star(td, s * px, s * py, s * 0.05, (255, 222, 0))


def star(td, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    td.polygon(pts, fill=fill)


def flag_ru(tile, s):
    td = ImageDraw.Draw(tile)
    td.rectangle((0, 0, s, s / 3), fill=(255, 255, 255))
    td.rectangle((0, s / 3, s, 2 * s / 3), fill=(0, 57, 166))
    td.rectangle((0, 2 * s / 3, s, s), fill=(213, 43, 30))


roundel(*centers[0], r, flag_us)
roundel(*centers[1], r, flag_cn)
roundel(*centers[2], r, flag_ru)

text(M + 320, 172, "SHENZHEN SUMMIT", f(FB, 20), TEAL)
lead_lines = wrap("Trump, Xi and Putin sign a pact on energy, nuclear risk and UN reform",
                  f(FB, 36), W - M - 320 - 30)
ly = 198
for ln in lead_lines:
    text(M + 320, ly, ln, f(FB, 36))
    ly += 43

sub = "First trilateral of the three nuclear powers; Putin tells Europe: come to Moscow"
for ln in wrap(sub, f(FR, 22), W - M - 320 - 30)[:2]:
    text(M + 320, ly + 4, ln, f(FR, 22), DIM)
    ly += 29

# three short outcome lines, so the panel is not half empty
outcomes = [
    ("ENERGY", "Raise refined-fuel supply, keep energy flows stable"),
    ("NUCLEAR", "\"A nuclear war can never be won, and must never be fought\""),
    ("UN + ICC", "Reform the Security Council; the ICC must not overreach"),
]
oy = ly + 22
list_x = M + 342
for tag, line in outcomes:
    d.ellipse((M + 322, oy + 8, M + 330, oy + 16), fill=GOLD)
    tag_w = d.textlength(tag, font=f(FB, 17))
    text(list_x, oy, tag, f(FB, 17), GOLD)
    body_x = list_x + tag_w + 12
    body_w = W - M - 26 - body_x
    rows = wrap(line, f(FR, 19), body_w)[:2]
    by = oy + 1
    for row in rows:
        text(body_x, by, row, f(FR, 19), INK)
        by += 23
    oy += max(29, 23 * len(rows) + 8)

# ---------------------------------------------------------------- grid of four
gw = (W - 2 * M - 16) // 2
gh = 168
gx = [M, M + gw + 16]
gy = [582, 582 + gh + 12]


def icon_justice(cx, cy, s):
    d.line([(cx, cy - s * 0.45), (cx, cy + s * 0.34)], fill=GOLD, width=6)
    d.line([(cx - s * 0.5, cy - s * 0.30), (cx + s * 0.5, cy - s * 0.30)], fill=GOLD, width=6)
    d.line([(cx - s * 0.22, cy + s * 0.34), (cx + s * 0.22, cy + s * 0.34)], fill=GOLD, width=6)
    for sx in (-1, 1):
        px = cx + sx * s * 0.5
        d.line([(px, cy - s * 0.30), (px - s * 0.16, cy + s * 0.02)], fill=GOLD, width=4)
        d.line([(px, cy - s * 0.30), (px + s * 0.16, cy + s * 0.02)], fill=GOLD, width=4)
        d.arc((px - s * 0.16, cy - s * 0.06, px + s * 0.16, cy + s * 0.10), 0, 180, fill=GOLD, width=4)


def icon_chart(cx, cy, s):
    base = cy + s * 0.34
    d.line([(cx - s * 0.45, base), (cx + s * 0.45, base)], fill=LINE, width=3)
    heights = [0.10, 0.26, 0.18, 0.34, 0.22, 0.42]
    bw = s * 0.11
    x = cx - s * 0.40
    for i, hgt in enumerate(heights):
        col = RED if i >= 4 else TEAL
        top = base - s * hgt * 1.4
        d.rectangle((x, top, x + bw, base), fill=col)
        x += bw + s * 0.045
    d.line([(cx - s * 0.44, cy - s * 0.30), (cx + s * 0.46, cy + s * 0.10)], fill=RED, width=5)


def icon_leaf(cx, cy, s):
    # emissions curve falling under a leaf: climate policy, not a prohibition sign
    d.line([(cx - s * 0.44, cy + s * 0.34), (cx + s * 0.44, cy + s * 0.34)],
           fill=LINE, width=3)
    pts = []
    for i in range(21):
        t = i / 20
        px = cx - s * 0.44 + t * s * 0.88
        py = cy - s * 0.30 + (t ** 2.2) * s * 0.60
        pts.append((px, py))
    d.line(pts, fill=TEAL, width=5)
    d.polygon([(cx + s * 0.34, cy + s * 0.30), (cx + s * 0.48, cy + s * 0.30),
               (cx + s * 0.41, cy + s * 0.16)], fill=TEAL)


def icon_wall(cx, cy, s):
    bw, bh = s * 0.22, s * 0.14
    for row in range(3):
        off = (row % 2) * bw * 0.5
        for col in range(3):
            x0 = cx - s * 0.42 + col * bw + off
            y0 = cy + s * 0.30 - (row + 1) * bh
            d.rectangle((x0, y0, x0 + bw - 4, y0 + bh - 4), fill=DIM)
    d.line([(cx - s * 0.46, cy + s * 0.30), (cx + s * 0.46, cy + s * 0.30)],
           fill=RED, width=4)


cards = [
    (gx[0], gy[0], icon_justice, "JUSTICE", "ICJ: Myanmar committed genocide against the Rohingya", RED),
    (gx[1], gy[0], icon_chart, "MARKETS", "AI rally fades after Anthropic's record IPO; S&P 500 falls 2%", RED),
    (gx[0], gy[1], icon_leaf, "CLIMATE", "COP31 draft drops fossil-fuel mention, keeps electrification", TEAL),
    (gx[1], gy[1], icon_wall, "MIDDLE EAST", "Israeli tanks and bulldozers push past Gaza's Yellow Line", RED),
]

for (px, py, icon, tag, headline, accent) in cards:
    panel((px, py, px + gw, py + gh), PANEL_HI if py == gy[0] else PANEL)
    icon(px + 58, py + 62, 84)
    text(px + 118, py + 30, tag, f(FB, 17), accent)
    hy = py + 54
    for ln in wrap(headline, f(FB, 24), gw - 140)[:3]:
        text(px + 118, hy, ln, f(FB, 24))
        hy += 30

# ---------------------------------------------------------------- ticker
ty = 950
d.line([(M, ty - 12), (W - M, ty - 12)], fill=LINE, width=2)
d.rounded_rectangle((M, ty - 2, W - M, H - 14), radius=8, fill=PANEL, outline=LINE, width=2)
text(M + 16, ty + 8, "ALSO TODAY", f(FB, 16), GOLD)
tick = "US–Venezuela oil pact · Denmark backs Greenland security deal · COVID variant PJ.2.1 spreads"
tx = M + 152
avail = W - M - tx - 16
for ln in wrap(tick, f(FR, 19), avail)[:2]:
    text(tx, ty + 7, ln, f(FR, 19), (196, 206, 222))
    ty += 22

# ---------------------------------------------------------------- bounds check
bottom_cards = gy[1] + gh
assert bottom_cards <= ty - 12, f"cards overlap the ticker: {bottom_cards} > {ty - 12}"
assert oy <= lead[3] - 10, f"lead bullets overflow the panel: {oy} > {lead[3] - 10}"
print("bounds ok: bullets end", oy, "panel", lead[3], "| cards end", bottom_cards)

img.save("/home/agentuser/makefun-workspace/news/entry.png", "PNG", optimize=True)
print("saved", img.size)
