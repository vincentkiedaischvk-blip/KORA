"""Erzeugt die vier Bild-Ads (1080 × 1350) nach assets/ads/."""

from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W, H = 1080, 1350
M = 88
F = os.path.join(ROOT, "brand", "fonts") + os.sep
OUT = os.path.join(ROOT, "assets", "ads") + os.sep
os.makedirs(OUT, exist_ok=True)

BG   = (244, 244, 242)
CARD = (255, 255, 255)
INK  = (10, 10, 10)
GREY = (138, 138, 138)
GRY2 = (110, 110, 110)
LIME = (200, 241, 105)
LINE = (225, 225, 221)

def f(n, s): return ImageFont.truetype(F + n, s)
BLK = lambda s: f("InterDisplay-Black.ttf", s)
XBD = lambda s: f("InterDisplay-ExtraBold.ttf", s)
BLD = lambda s: f("InterDisplay-Bold.ttf", s)
SBD = lambda s: f("Inter-SemiBold.ttf", s)
MED = lambda s: f("Inter-Medium.ttf", s)


def tw(d, t, fnt, ls=0):
    if ls == 0: return d.textlength(t, font=fnt)
    return sum(d.textlength(c, font=fnt) + ls for c in t) - ls


def ts(d, xy, t, fnt, fill, ls=0):
    x, y = xy
    if ls == 0:
        d.text((x, y), t, font=fnt, fill=fill); return
    for c in t:
        d.text((x, y), c, font=fnt, fill=fill)
        x += d.textlength(c, font=fnt) + ls


def wrap(d, t, fnt, maxw):
    out, cur = [], ""
    for w_ in t.split():
        c = (cur + " " + w_).strip()
        if d.textlength(c, font=fnt) <= maxw: cur = c
        else:
            if cur: out.append(cur)
            cur = w_
    if cur: out.append(cur)
    return out


def logo(d, x, y, ink=INK, grey=GREY):
    fn = XBD(36)
    d.text((x, y), "KORA", font=fn, fill=ink)
    w = d.textlength("KORA", font=fn)
    d.text((x + w + 11, y), "SAFETY", font=BLD(36), fill=grey)


def pill(d, x, y, text, bg=INK, fg=(255, 255, 255), fs=24, padx=28, pady=16, ls=1.2):
    fnt = SBD(fs)
    w = tw(d, text, fnt, ls)
    h = fs + pady * 2
    d.rounded_rectangle([x, y, x + w + padx * 2, y + h], radius=h // 2, fill=bg)
    ts(d, (x + padx, y + pady - 2), text, fnt, fg, ls=ls)
    return y + h


def head(d, y, lines, size=88, lh=1.03, c1=INK, c2=GREY):
    fnt = BLK(size)
    for i, ln in enumerate(lines):
        d.text((M, y), ln, font=fnt, fill=(c1 if i == 0 else c2))
        y += int(size * lh)
    return y


def body(d, y, t, size=32, col=GRY2, maxw=W - 2 * M, lh=1.46):
    fnt = MED(size)
    for ln in wrap(d, t, fnt, maxw):
        d.text((M, y), ln, font=fnt, fill=col)
        y += int(size * lh)
    return y


def cta(d, text, dark=False):
    """Button unten links + Zielgruppen-Fußzeile."""
    y = H - M - 108
    pill(d, M, y, text, bg=(LIME if dark else INK),
         fg=(INK if dark else (255, 255, 255)), fs=30, padx=40, pady=24, ls=0.4)


def base(dark=False):
    bg = INK if dark else BG
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    if dark:
        logo(d, M, M - 4, (255, 255, 255), (130, 130, 130))
    else:
        logo(d, M, M - 4)
    return img, d


# ══════════════════════════════════════════════════════════════
# AD 1 — ANBIETER · Auftragslage (hell, Angebots-Karte als Beweis)
# ══════════════════════════════════════════════════════════════
img, d = base()
pill(d, M, 300, "FÜR SICHERHEITSDIENSTE", bg=LIME, fg=INK, fs=22, padx=24, pady=13, ls=1.6)
y = head(d, 412, ["Aufträge,", "ohne Vertrieb."], size=92)
y += 26
y = body(d, y, "Anfragen aus Ihrer Region landen direkt bei Ihnen. "
               "Prüfen, Preis kalkulieren, Angebot abgeben.", size=32)

# Anfrage-Karte
cy = y + 44
d.rounded_rectangle([M, cy, W - M, cy + 250], radius=26, fill=CARD)
ts(d, (M + 36, cy + 34), "NEUE ANFRAGE", SBD(20), GREY, ls=2.6)
d.text((M + 36, cy + 74), "Event Security · Stuttgart", font=BLD(42), fill=INK)
d.text((M + 36, cy + 132), "8 Kräfte · Fr, 04.09. · 18:00–02:00", font=MED(28), fill=GRY2)
d.line([(M + 36, cy + 184), (W - M - 36, cy + 184)], fill=LINE, width=2)
d.text((M + 36, cy + 202), "Angebot abgeben", font=SBD(28), fill=INK)
# Pfeil
ax = W - M - 76
d.line([(ax, cy + 216), (ax + 26, cy + 216)], fill=INK, width=4)
d.line([(ax + 16, cy + 206), (ax + 26, cy + 216)], fill=INK, width=4)
d.line([(ax + 16, cy + 226), (ax + 26, cy + 216)], fill=INK, width=4)

cta(d, "Jetzt Early Access")
img.save(OUT + "ad-1-anbieter-auftraege.png")

# ══════════════════════════════════════════════════════════════
# AD 2 — ANBIETER · Verwaltung (dunkel, Kontrast im Feed)
# ══════════════════════════════════════════════════════════════
img, d = base(dark=True)
pill(d, M, 250, "FÜR SICHERHEITSDIENSTE", bg=LIME, fg=INK, fs=22, padx=24, pady=13, ls=1.6)
y = head(d, 360, ["Schluss mit", "Excel-Chaos."], size=92,
         c1=(255, 255, 255), c2=(130, 130, 130))
y += 26
y = body(d, y, "Verfügbarkeiten, Schichten und Einsätze zentral planen — "
               "statt Dienstplan per WhatsApp.", size=32, col=(150, 150, 150))

# Schichtzeilen
cy = y + 50
rows = [("Max", "Event Security", "18:00–02:00"),
        ("Leon", "Objektschutz", "06:00–14:00"),
        ("Tim", "Event Security", "18:00–02:00")]
for nm, art, zeit in rows:
    d.rounded_rectangle([M, cy, W - M, cy + 98], radius=18, fill=(26, 26, 26))
    d.ellipse([M + 28, cy + 30, M + 66, cy + 68], fill=LIME)
    d.text((M + 84, cy + 22), nm, font=BLD(32), fill=(255, 255, 255))
    d.text((M + 84, cy + 60), art, font=MED(24), fill=(130, 130, 130))
    zt = SBD(30)
    d.text((W - M - 36 - d.textlength(zeit, font=zt), cy + 34), zeit, font=zt, fill=LIME)
    cy += 112

cta(d, "Jetzt Early Access", dark=True)
img.save(OUT + "ad-2-anbieter-planung.png")

# ══════════════════════════════════════════════════════════════
# AD 3 — KUNDEN · Vergleich (hell, zwei Angebote nebeneinander)
# ══════════════════════════════════════════════════════════════
img, d = base()
pill(d, M, 250, "FÜR UNTERNEHMEN", bg=LIME, fg=INK, fs=22, padx=24, pady=13, ls=1.6)
y = head(d, 360, ["Eine Anfrage.", "Mehrere Angebote."], size=84)
y += 26
y = body(d, y, "Bedarf einmal eingeben, Angebote geprüfter Anbieter vergleichen, "
               "den passenden auswählen.", size=32)

cy = y + 44
d.rounded_rectangle([M, cy, W - M, cy + 118], radius=22, fill=CARD)
d.text((M + 34, cy + 26), "Security für Event · Berlin", font=BLD(38), fill=INK)
d.text((M + 34, cy + 74), "12 Kräfte · Sa, 18:00–02:00", font=MED(26), fill=GRY2)

cy += 134
half = (W - 2 * M - 18) // 2
for i, (nm, preis) in enumerate([("Alpha Security", "1.440 €"), ("Nord Guard", "1.560 €")]):
    x = M + i * (half + 18)
    d.rounded_rectangle([x, cy, x + half, cy + 190], radius=22, fill=CARD)
    d.text((x + 30, cy + 26), nm, font=BLD(34), fill=INK)
    d.line([(x + 32, cy + 84), (x + 42, cy + 95)], fill=INK, width=4)
    d.line([(x + 42, cy + 95), (x + 58, cy + 71)], fill=INK, width=4)
    d.text((x + 70, cy + 70), "Geprüft", font=MED(26), fill=GRY2)
    d.text((x + 30, cy + 122), preis, font=BLK(44), fill=INK)

cta(d, "Kostenlos anfragen")
img.save(OUT + "ad-3-kunden-vergleich.png")

# ══════════════════════════════════════════════════════════════
# AD 4 — KUNDEN · Problem (dunkel, harte Zahl als Hook)
# ══════════════════════════════════════════════════════════════
img, d = base(dark=True)
pill(d, M, 288, "FÜR UNTERNEHMEN", bg=LIME, fg=INK, fs=22, padx=24, pady=13, ls=1.6)
y = 420
fn = BLK(190)
d.text((M, y), "20", font=fn, fill=LIME)
nw = d.textlength("20", font=fn)
d.text((M + nw + 30, y + 62), "Anrufe für", font=BLD(56), fill=(255, 255, 255))
d.text((M + nw + 30, y + 124), "ein Angebot?", font=BLD(56), fill=(130, 130, 130))
y += 276

d.line([(M, y), (W - M, y)], fill=(45, 45, 45), width=2)
y += 52
y = head(d, y, ["Geht auch", "in einer Anfrage."], size=68,
         c1=(255, 255, 255), c2=(255, 255, 255))
y += 22
body(d, y, "KORA holt Angebote geprüfter Security-Dienstleister für Sie ein.",
     size=31, col=(150, 150, 150))

cta(d, "Kostenlos anfragen", dark=True)
img.save(OUT + "ad-4-kunden-problem.png")

print("ok", sorted(os.listdir(OUT)))
