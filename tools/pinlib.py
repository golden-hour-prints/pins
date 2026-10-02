"""Pin image generator for Golden Hour Prints (1000x1500 Pinterest pins from the book's line art)."""
import os, random
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
BOOK = os.path.join(ROOT, "assets", "book")
CREAM, TEAL, INK, WHITE, GOLD = (247, 240, 226), (62, 110, 108), (40, 36, 34), (255, 255, 255), (201, 146, 60)
PAL = [(233, 196, 106), (244, 162, 97), (231, 111, 81), (42, 157, 143), (138, 177, 125), (168, 218, 220),
       (69, 123, 157), (229, 152, 155), (181, 131, 141), (242, 204, 143), (129, 178, 154), (224, 122, 95)]
W, H = 1000, 1500


def lora(s, bold=False, italic=False):
    f = ImageFont.truetype(os.path.join(FONTS, "Lora-Italic-Variable.ttf" if italic else "Lora-Variable.ttf"), s)
    try: f.set_variation_by_name("Bold" if bold else "Regular")
    except Exception: pass
    return f


def pop(s, w="Medium"): return ImageFont.truetype(os.path.join(FONTS, f"Poppins-{w}.ttf"), s)


def crop(im):
    a = np.array(im.convert("L")); ys, xs = np.where(a < 128)
    return im.crop((xs.min() - 8, ys.min() - 8, xs.max() + 8, ys.max() + 8))


def line_art(slug): return crop(Image.open(os.path.join(BOOK, f"{slug}.png")).convert("RGB"))


def colorize(slug, seed=3):
    im = line_art(slug); a = np.array(im.convert("L"))
    n, lab, stats, _ = cv2.connectedComponentsWithStats((a > 160).astype(np.uint8), connectivity=4)
    rgb = np.array(im.convert("RGB")); rnd = random.Random(seed)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 40: rgb[lab == i] = rnd.choice(PAL)
    return Image.fromarray(rgb)


def fit(im, w, h):
    s = min(w / im.width, h / im.height); return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)


def ctext(d, y, txt, f, fill, cx=W // 2):
    d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=fill)


def wrap(d, txt, f, maxw):
    out, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: out.append(cur); cur = w
    return out + [cur]


def headline(d, y, txt, size=70, maxw=880):
    f = lora(size, True)
    while len(wrap(d, txt, f, maxw)) > 2 and size > 44: size -= 4; f = lora(size, True)
    for ln in wrap(d, txt, f, maxw): ctext(d, y, ln, f, INK); y += int(size * 1.2)
    return y


def base():
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    d.rounded_rectangle([22, 22, W - 22, H - 22], 30, outline=TEAL, width=8)
    return im, d


def footer(d, txt="Golden Hour Prints  •  on Amazon"):
    d.rounded_rectangle([22, H - 120, W - 22, H - 22], 30, fill=TEAL); d.rectangle([22, H - 120, W - 22, H - 80], fill=TEAL)
    ctext(d, H - 97, txt, pop(38), WHITE)


def framed(im, art, x, y):
    d = ImageDraw.Draw(im); d.rectangle([x - 12, y - 12, x + art.width + 12, y + art.height + 12], fill=WHITE, outline=TEAL, width=5)
    im.paste(art, (x, y))


def badge(d, x, y, txt, color):
    w = d.textlength(txt, font=pop(30, "Bold")) + 50
    d.rounded_rectangle([x, y, x + w, y + 50], 25, fill=color); d.text((x + 25, y + 6), txt, font=pop(30, "Bold"), fill=WHITE)


def before_after(slug, title, sub, seed=4):
    im, d = base()
    y = headline(d, 55, title, 66); ctext(d, y + 5, sub, lora(36, italic=True), TEAL)
    top = y + 75; room = (H - 150 - top - 50) // 2
    la, co = fit(line_art(slug), 760, room), fit(colorize(slug, seed), 760, room)
    framed(im, la, (W - la.width) // 2, top); framed(im, co, (W - co.width) // 2, top + room + 50)
    badge(d, 50, top + 12, "BEFORE", TEAL); badge(d, 50, top + room + 62, "AFTER", GOLD)
    footer(d); return im


def spotlight(slug, title, sub, colored=True, seed=5):
    im, d = base()
    y = headline(d, 60, title, 70); ctext(d, y + 5, sub, lora(38, italic=True), TEAL)
    art = fit(colorize(slug, seed) if colored else line_art(slug), 820, H - 150 - (y + 90) - 30)
    framed(im, art, (W - art.width) // 2, y + 90); footer(d); return im


def quote_card(slug, lines, title, seed=6):
    """Text-led pin: a short list of tips/ideas with a small colored design."""
    im, d = base()
    y = headline(d, 60, title, 62)
    y += 30
    for k, t in enumerate(lines):
        d.ellipse([80, y, 146, y + 66], fill=TEAL); ctext(d, y + 8, str(k + 1), pop(38, "Bold"), WHITE, cx=113)
        yy = y + 6
        for ln in wrap(d, t, pop(35, "Regular"), 740): d.text((176, yy), ln, font=pop(35, "Regular"), fill=INK); yy += 46
        y = max(y + 110, yy + 26)
    art = fit(colorize(slug, seed), 300, max(150, H - 150 - y - 30))
    im.paste(art, (W - art.width - 60, H - 140 - art.height)); footer(d); return im


def save(im, path): im.convert("RGB").save(path, quality=88, optimize=True)
