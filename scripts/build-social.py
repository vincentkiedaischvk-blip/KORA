"""Erzeugt die sechs Instagram-Posts (1080 × 1350) nach assets/social/."""

from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W, H = 1080, 1350
M = 88
F = os.path.join(ROOT, "brand", "fonts") + os.sep
OUT = os.path.join(ROOT, "assets", "social") + os.sep
os.makedirs(OUT, exist_ok=True)

# Palette der Landingpage
BG    = (244, 244, 242)     # helles Off-White
CARD  = (255, 255, 255)
INK   = (10, 10, 10)        # Schwarz
GREY  = (138, 138, 138)     # zweite Headline-Zeile / Fließtext
GREY2 = (110, 110, 110)
LIME  = (200, 241, 105)     # VERIFIED-Badge
LINE  = (223, 223, 219)

def f(n, s): return ImageFont.truetype(F + n, s)
BLK  = lambda s: f("InterDisplay-Black.ttf", s)
XBD  = lambda s: f("InterDisplay-ExtraBold.ttf", s)
BLD  = lambda s: f("InterDisplay-Bold.ttf", s)
SBD  = lambda s: f("Inter-SemiBold.ttf", s)
MED  = lambda s: f("Inter-Medium.ttf", s)
REG  = lambda s: f("Inter-Regular.ttf", s)


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
    fn = XBD(38)
    d.text((x, y), "KORA", font=fn, fill=ink)
    w = d.textlength("KORA", font=fn)
    d.text((x + w + 12, y), "SAFETY", font=BLD(38), fill=grey)


def pill(d, x, y, text, bg=INK, fg=(255, 255, 255), fs=24, padx=28, pady=16, ls=1.2):
    fnt = SBD(fs)
    w = tw(d, text, fnt, ls)
    h = fs + pady * 2
    d.rounded_rectangle([x, y, x + w + padx * 2, y + h], radius=h // 2, fill=bg)
    ts(d, (x + padx, y + pady - 2), text, fnt, fg, ls=ls)
    return x + w + padx * 2, y + h


def badge(d, x, y, text):
    """Limetten-Pill wie das VERIFIED-Label."""
    return pill(d, x, y, text, bg=LIME, fg=INK, fs=22, padx=24, pady=13, ls=1.6)


def base(bg=BG, page=None, ink=INK, grey=GREY):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    logo(d, M, M - 6, ink, grey)
    if page:
        fnt = SBD(22)
        lbl = f"{page:02d}/06"
        ts(d, (W - M - tw(d, lbl, fnt, 1.5), M + 6), lbl, fnt, grey, ls=1.5)
    return img, d


def head(d, y, lines, size=104, lh=1.02, c1=INK, c2=GREY):
    """Erste Zeile schwarz, folgende grau — wie im Hero."""
    fnt = BLK(size)
    for i, ln in enumerate(lines):
        d.text((M, y), ln, font=fnt, fill=(c1 if i == 0 else c2))
        y += int(size * lh)
    return y


def body(d, y, t, size=32, col=GREY2, maxw=W - 2 * M, lh=1.48):
    fnt = MED(size)
    for ln in wrap(d, t, fnt, maxw):
        d.text((M, y), ln, font=fnt, fill=col)
        y += int(size * lh)
    return y


def card(d, y, num, title, sub, h=168, r=26):
    d.rounded_rectangle([M, y, W - M, y + h], radius=r, fill=CARD)
    ts(d, (M + 36, y + 30), num, SBD(21), GREY, ls=2)
    d.text((M + 36, y + 62), title, font=BLD(42), fill=INK)
    d.text((M + 36, y + 116), sub, font=MED(27), fill=GREY2)
    return y + h + 16


def foot(d, text, col=GREY):
    ts(d, (M, H - M - 26), text, SBD(25), col, ls=0.4)


# ── 01 · Cover ─────────────────────────────────────────────
img, d = base(page=1)
badge(d, M, 430, "COMING SOON · GERMANY")
y = head(d, 550, ["Security.", "On demand."], size=118)
y += 34
body(d, y, "Das Portal für geprüfte Security-Dienstleister. "
           "Auftrag stellen, Angebote vergleichen, beauftragen.", size=33)
foot(d, "korasafety.de")
img.save(OUT + "01-cover.png")

# ── 02 · Problem ───────────────────────────────────────────
img, d = base(bg=INK, page=2, ink=(255, 255, 255), grey=(130, 130, 130))
badge(d, M, 360, "SO LÄUFT ES HEUTE")
y = 495
fn = BLK(112)
colw = max(d.textlength(n, font=fn) for n in ("20", "3", "1"))
for num, label in [("20", "Anrufe"), ("3", "Rückmeldungen"), ("1", "Angebot")]:
    nw = d.textlength(num, font=fn)
    d.text((M + colw - nw, y), num, font=fn, fill=(255, 255, 255))
    d.text((M + colw + 34, y + 36), label, font=BLD(54), fill=(130, 130, 130))
    y += 150
y += 26
body(d, y, "Security zu beauftragen kostet heute mehr Zeit als der Einsatz selbst.",
     size=33, col=(150, 150, 150))
foot(d, "korasafety.de", col=(120, 120, 120))
img.save(OUT + "02-problem.png")

# ── 03 · Für Unternehmen ───────────────────────────────────
img, d = base(page=3)
badge(d, M, 262, "FÜR UNTERNEHMEN")
y = head(d, 370, ["Eine Anfrage.", "Mehrere Angebote."], size=76)
y += 34
y = card(d, y, "01", "Bedarf eingeben", "Ort, Zeitraum, Anzahl der Kräfte")
y = card(d, y, "02", "Anbieter erhalten", "Geprüfte Dienstleister aus der Region")
y = card(d, y, "03", "Angebote vergleichen", "Preis und Leistung nebeneinander")
foot(d, "Kostenlos · Unverbindlich")
img.save(OUT + "03-unternehmen.png")

# ── 04 · Für Anbieter ──────────────────────────────────────
img, d = base(page=4)
badge(d, M, 262, "FÜR SECURITY-ANBIETER")
y = head(d, 370, ["Mehr Aufträge.", "Weniger Verwaltung."], size=76)
y += 34
y = card(d, y, "01", "Anfragen erhalten", "Passend zu Region und Kapazität")
y = card(d, y, "02", "Angebot abgeben", "Kalkulieren und digital senden")
y = card(d, y, "03", "Team einteilen", "Einsätze planen ohne Excel-Chaos")
foot(d, "Kostenlos starten")
img.save(OUT + "04-anbieter.png")

# ── 05 · Geprüft ───────────────────────────────────────────
img, d = base(page=5)
badge(d, M, 262, "VERTRAUEN")
y = head(d, 370, ["Geprüft, bevor", "gebucht wird."], size=76)
y += 46
items = ["Unternehmensprüfung", "Nachweise", "Qualifikationen",
         "Versicherungsschutz", "Referenzen", "Bewertungen"]
fnt = SBD(34)
x, ry = M, y
for it in items:
    w = tw(d, it, fnt, 0) + 44 + 34
    if x + w > W - M:
        x = M; ry += 84
    d.rounded_rectangle([x, ry, x + w, ry + 66], radius=33, fill=CARD)
    d.line([(x + 26, ry + 36), (x + 34, ry + 45)], fill=INK, width=4)
    d.line([(x + 34, ry + 45), (x + 48, ry + 23)], fill=INK, width=4)
    d.text((x + 60, ry + 15), it, font=fnt, fill=INK)
    x += w + 14
y = ry + 66 + 70
body(d, y, "Kein anonymes Verzeichnis. Jeder Anbieter wird vor der Freischaltung geprüft.", size=32)
foot(d, "korasafety.de")
img.save(OUT + "05-geprueft.png")

# ── 06 · Call to Action ────────────────────────────────────
img, d = base(bg=INK, page=6, ink=(255, 255, 255), grey=(130, 130, 130))
badge(d, M, 400, "EARLY ACCESS")
y = head(d, 520, ["Sei dabei,", "bevor KORA", "live geht."], size=94,
         c1=(255, 255, 255), c2=(255, 255, 255))
y += 46
body(d, y, "Wir bauen KORA mit Unternehmen und Anbietern aus der Praxis.",
     size=32, col=(150, 150, 150))
pill(d, M, H - M - 130, "korasafety.de", bg=LIME, fg=INK, fs=30, padx=40, pady=24, ls=0.4)
img.save(OUT + "06-cta.png")

print("ok", sorted(os.listdir(OUT)))
