#!/usr/bin/env python3
"""BROADSHEET variant — news-image-20261124. Draws entry.png 1024x1024.
Classic newspaper front page. All facts from STORIES.md (24 Nov 2026, UTC)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(BASE, "fonts")

PAPER = (253, 251, 245)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GOLD = (176, 141, 44)
GREY = (90, 90, 88)
LIGHT = (238, 234, 224)
SEA = (207, 227, 239)
LAND = (226, 214, 186)
GREEN = (31, 111, 63)

def fs(size, bold=False, serif=False):
    name = ("LiberationSerif-Bold.ttf" if serif and bold else
            "LiberationSerif-Regular.ttf" if serif else
            "LiberationSans-Bold.ttf" if bold else
            "LiberationSans-Regular.ttf")
    return ImageFont.truetype(os.path.join(F, name), size)

def tw(d, text, font):
    return d.textlength(text, font=font)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def badge(d, x, y, text, fill, fg=(255, 255, 255), size=12, pad=5, h=18):
    f = fs(size, bold=True)
    w = int(tw(d, text, f)) + pad * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=fill)
    d.text((x + pad, y + (h - size) // 2 - 1), text, font=f, fill=fg)
    return w

def tag_color(tag):
    return {"CONFIRMED": GREEN, "OFFICIAL": NAVY, "REPORTED": (150, 90, 10),
            "CLAIM": RED}.get(tag, GREY)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 22  # margin

# ---------- top bar + masthead: date is the LARGEST element ----------
d.rectangle([0, 0, W, 9], fill=INK)
date = "TUESDAY 24 NOVEMBER 2026"
df = fs(62, bold=True, serif=True)
d.text(((W - tw(d, date, df)) / 2, 14), date, font=df, fill=INK)
sub = "THE WORLD IN ONE PAGE  ·  EVERY STORY FIRST REPORTED TUESDAY 24 NOVEMBER 2026 (UTC)"
sf = fs(17, bold=True)
d.text(((W - tw(d, sub, sf)) / 2, 86), sub, font=sf, fill=RED)
d.rectangle([MX, 110, W - MX, 113], fill=INK)
d.rectangle([MX, 116, W - MX, 117], fill=INK)

# ---------- day in numbers strip ----------
d.rectangle([MX, 122, W - MX, 160], fill=NAVY)
n1 = ("THE DAY IN NUMBERS   4 tankers hit  ·  25 hostages  ·  11 wounded  ·  "
      "10 of 12 counts  ·  25 dead  ·  23 injured  ·  6 killed")
n2 = ("5 crew killed  ·  272 meningitis cases  ·  700,000+ dead or missing  ·  "
      "6,803 migrants to be returned  ·  Nvidia −7%")
nf = fs(14, bold=True)
d.text(((W - tw(d, n1, nf)) / 2, 126), n1, font=nf, fill=(255, 255, 255))
d.text(((W - tw(d, n2, nf)) / 2, 144), n2, font=nf, fill=(255, 255, 255))

# ---------- lead illustrations ----------
def ill_huawei(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 74))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 90, 40))  # bench
    # scales of justice
    cx, cy = x + 70, y + 14
    d.line([cx, cy + 6, cx, cy + 52], fill=(255, 215, 120), width=4)
    d.line([cx - 34, cy + 10, cx + 34, cy + 10], fill=(255, 215, 120), width=4)
    for sx in (cx - 34, cx + 34):
        d.line([sx, cy + 10, sx, cy + 30], fill=(255, 215, 120), width=2)
        d.pieslice([sx - 13, cy + 28, sx + 13, cy + 42], 0, 180, fill=(255, 215, 120))
    d.ellipse([cx - 6, cy - 2, cx + 6, cy + 8], fill=(255, 215, 120))
    # gavel
    d.line([x + 165, y + 52, x + 215, y + 18], fill=(210, 170, 90), width=7)
    d.rectangle([x + 200, y + 8, x + 238, y + 26], fill=(160, 110, 50))
    d.rectangle([x + 150, y + 58, x + 230, y + 64], fill=(160, 110, 50))
    # phone / chip
    d.rounded_rectangle([x + 285, y + 12, x + 325, y + 62], radius=6,
                        outline=(255, 255, 255), width=3)
    d.rectangle([x + 294, y + 24, x + 316, y + 50], fill=(120, 180, 255))
    d.text((x + 335, y + 22), "GUILTY", font=fs(24, bold=True), fill=(255, 255, 255))
    d.text((x + 335, y + 50), "10 OF 12", font=fs(15, bold=True),
           fill=(255, 215, 120))

def ill_hormuz(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.polygon([(x, y), (x + 150, y), (x + 120, y + 34), (x + 40, y + 30)],
              fill=(214, 190, 150))
    d.polygon([(x + 330, y + h), (x + w, y + h), (x + w, y),
               (x + 420, y + 20), (x + 360, y + 44)], fill=(214, 190, 150))
    d.polygon([(x + 150, y + h), (x + 330, y + h), (x + 360, y + 44),
               (x + 120, y + 34)], fill=(150, 190, 220))
    # strait label + tankers
    d.text((x + 168, y + 6), "STRAIT OF HORMUZ", font=fs(13, bold=True), fill=NAVY)
    for tx, ty in ((x + 180, y + 40), (x + 250, y + 52), (x + 310, y + 38)):
        d.rectangle([tx, ty, tx + 46, ty + 12], fill=(60, 60, 60))
        d.rectangle([tx + 8, ty - 8, tx + 18, ty], fill=(60, 60, 60))
        d.polygon([(tx + 46, ty + 2), (tx + 58, ty - 8), (tx + 58, ty + 6)],
                  fill=(255, 120, 40))
        d.ellipse([tx + 52, ty - 16, tx + 60, ty - 8], fill=(255, 170, 60))
    # mines
    for mx, my in ((x + 210, y + 62), (x + 285, y + 66), (x + 340, y + 60)):
        d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=INK)
        for dx, dy in ((-9, 0), (9, 0), (0, -9), (0, 9)):
            d.line([mx, my, mx + dx, my + dy], fill=INK, width=2)
    d.rectangle([x + 8, y + h - 22, x + 268, y + h - 2], fill=(255, 255, 255))
    d.text((x + 12, y + h - 20), "4 TANKERS HIT — CLAIM UNCONFIRMED",
           font=fs(13, bold=True), fill=RED)

def ill_ukraine(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.polygon([(x, y), (x + 210, y), (x + 190, y + 40), (x + 30, y + 44)],
              fill=(214, 190, 150))
    d.text((x + 38, y + 6), "GULF OF FINLAND", font=fs(13, bold=True), fill=NAVY)
    d.rectangle([x + 60, y + 48, x + 130, y + 62], fill=(70, 70, 70))
    d.rectangle([x + 78, y + 38, x + 92, y + 48], fill=(70, 70, 70))
    d.ellipse([x + 140, y + 40, x + 152, y + 52], fill=(255, 140, 40))
    d.line([x + 146, y + 46, x + 128, y + 54], fill=(255, 140, 40), width=3)
    d.text((x + 240, y + 8), "SPARTA II HIT", font=fs(16, bold=True), fill=INK)
    d.text((x + 240, y + 28), "16 crew evacuated", font=fs(13), fill=INK)
    d.polygon([(x + 300, y + h), (x + w, y + h), (x + w, y + 44),
               (x + 380, y + 50), (x + 330, y + 66)], fill=(214, 190, 150))
    d.text((x + 300, y + 46), "OFF LIBYA:", font=fs(12, bold=True), fill=RED)
    d.text((x + 300, y + 60), "CORVETTE CLAIMED SUNK",
           font=fs(11, bold=True), fill=RED)

def ill_cartagena(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 222, 179))
    d.rectangle([x + 40, y + 18, x + w - 40, y + h], fill=(250, 246, 236),
                outline=INK, width=2)
    for i in range(8):  # awning stripes
        c = RED if i % 2 == 0 else (255, 255, 255)
        d.polygon([(x + 40 + i * 48, y + 18), (x + 88 + i * 48, y + 18),
                   (x + 80 + i * 48, y + 38), (x + 48 + i * 48, y + 38)], fill=c)
    d.rectangle([x + 70, y + 48, x + 150, y + h - 2], outline=INK, width=2)
    d.text((x + 82, y + 52), "SHOP", font=fs(15, bold=True), fill=INK)
    d.rectangle([x + 300, y + 48, x + 380, y + h - 2], outline=INK, width=2)
    d.text((x + 308, y + 52), "OPEN", font=fs(13, bold=True), fill=GREEN)
    d.rounded_rectangle([x + w - 158, y + 8, x + w - 8, y + 36], radius=6, fill=RED)
    d.text((x + w - 150, y + 13), "25 HELD · 5 FREED", font=fs(14, bold=True),
           fill=(255, 255, 255))

LEADS = [
    ("1", "HUAWEI GUILTY ON 10 OF 12 COUNTS", "20:41 UTC · CONFIRMED",
     "Brooklyn jury convicts on trade-secret theft + bank fraud; acquitted of "
     "racketeering. Two-month trial; sentencing Sept 2027; Huawei to appeal.",
     ill_huawei, GREEN),
    ("2", "HORMUZ IN FLAMES — 4 TANKERS HIT", "00:00 + 18:58 UTC · CLAIM",
     "Iran says four tankers hit mines and caught fire; maritime centre: claims "
     "unconfirmed. IRGC says it hit a container ship near Khasab, Oman.",
     ill_hormuz, RED),
    ("3", "UKRAINE HITS RUSSIAN SHIPS", "08:14 UTC · CONFIRMED",
     "Drones hit cargo ship Sparta II in the Gulf of Finland; 16 crew evacuated. "
     "Corvette + cargo ship hit off Libya — Kyiv claims the corvette sunk.",
     ill_ukraine, GREEN),
    ("4", "CARTAGENA HOSTAGES: 25 HELD", "17:35 UTC · OFFICIAL",
     "Armed men seize a supermarket in Cartagena, Colombia; 25 held, 5 older women "
     "freed. Military + police deployed; airport briefly halted landings.",
     ill_cartagena, NAVY),
]

LY0, LH, LGAP = 166, 160, 6
COLW = (W - 2 * MX - 16) // 2
for i, (num, head, meta, body, ill, tc) in enumerate(LEADS):
    cx = MX + (i % 2) * (COLW + 16)
    cy = LY0 + (i // 2) * (LH + LGAP)
    d.rectangle([cx, cy, cx + COLW, cy + LH], outline=INK, width=2)
    ill(cx + 2, cy + 2, COLW - 4, 76)
    d.rectangle([cx, cy, cx + 30, cy + 26], fill=RED)
    d.text((cx + 9, cy + 3), num, font=fs(18, bold=True), fill=(255, 255, 255))
    d.rectangle([cx, cy + 78, cx + COLW, cy + 79], fill=INK)
    hf = fs(20, bold=True, serif=True)
    d.text((cx + 8, cy + 83), head, font=hf, fill=INK)
    bf = fs(14)
    lines = wrap(d, body, bf, COLW - 16)[:2]
    yy = cy + 108
    for ln in lines:
        d.text((cx + 8, yy), ln, font=bf, fill=INK)
        yy += 17
    tag = meta.split("·")[-1].strip()
    badge(d, cx + 8, cy + LH - 20, tag, tag_color(tag), size=11, h=17)
    d.text((cx + 92, cy + LH - 19), meta.split("·")[0].strip(),
           font=fs(12, bold=True), fill=GREY)

# ---------- world map (numbered pins keyed to the leads) ----------
MAPY, MAPT, MAPB = 498, 516, 606
d.text((MX, MAPY), "WORLD MAP — WHERE IT HAPPENED",
       font=fs(16, bold=True), fill=INK)
d.text((W - MX - tw(d, "RED NUMBERS = THE 4 LEADS  ·  DOTS = TIER-2 STORIES",
                    fs(12, bold=True)), MAPY + 2),
       "RED NUMBERS = THE 4 LEADS  ·  DOTS = TIER-2 STORIES",
       font=fs(12, bold=True), fill=GREY)
d.rectangle([MX, MAPT, W - MX, MAPB], fill=SEA, outline=INK, width=1)
ox, oy = MX, MAPT
land = [
    [(30, 12), (220, 10), (232, 44), (185, 68), (120, 76), (58, 56), (24, 34)],
    [(252, 56), (302, 50), (322, 82), (292, 110), (260, 86)],
    [(468, 14), (542, 10), (552, 34), (502, 46), (464, 34)],
    [(468, 50), (560, 44), (576, 84), (520, 110), (478, 80)],
    [(560, 8), (852, 4), (902, 40), (822, 68), (700, 58), (600, 44), (560, 30)],
    [(798, 80), (882, 78), (888, 100), (820, 106)],
]
for poly in land:
    d.polygon([(ox + a, oy + b) for a, b in poly], fill=LAND,
              outline=(150, 135, 105))
PINS = [("1", 178, 30, "BROOKLYN"), ("2", 622, 56, "HORMUZ"),
        ("3", 540, 18, "FINLAND GULF"), ("3", 522, 50, "LIBYA"),
        ("4", 236, 72, "CARTAGENA")]
for num, px, py, lab in PINS:
    d.ellipse([ox + px - 11, oy + py - 11, ox + px + 11, oy + py + 11],
              fill=RED, outline=(255, 255, 255), width=2)
    d.text((ox + px - 4, oy + py - 8), num, font=fs(13, bold=True),
           fill=(255, 255, 255))
    d.text((ox + px + 14, oy + py - 7), lab, font=fs(11, bold=True), fill=INK)
for dx, dy in [(618, 58), (642, 72), (148, 56), (548, 32), (252, 74),
               (800, 56), (792, 76), (786, 70), (600, 66), (560, 60)]:
    d.ellipse([ox + dx - 4, oy + dy - 4, ox + dx + 4, oy + dy + 4],
              fill=NAVY, outline=(255, 255, 255), width=1)

# ---------- tier-2: pictogram + tag + named source ----------
T2Y = 612
d.text((MX, T2Y), "MORE OF THE DAY — 10 STORIES, EACH VERIFIED",
       font=fs(16, bold=True), fill=INK)
d.rectangle([MX, T2Y + 20, W - MX, T2Y + 21], fill=INK)

def icon(d, x, y, kind, fill):
    d.rounded_rectangle([x, y, x + 22, y + 22], radius=4, fill=fill)
    wcol = (255, 255, 255)
    if kind == "tower":
        d.rectangle([x + 8, y + 4, x + 14, y + 18], fill=wcol)
        d.rectangle([x + 5, y + 15, x + 17, y + 18], fill=wcol)
    elif kind == "arrow":
        d.line([x + 4, y + 18, x + 18, y + 4], fill=wcol, width=3)
        d.polygon([(x + 18, y + 4), (x + 12, y + 4), (x + 18, y + 10)], fill=wcol)
    elif kind == "trophy":
        d.rectangle([x + 8, y + 4, x + 14, y + 12], fill=wcol)
        d.rectangle([x + 10, y + 12, x + 12, y + 16], fill=wcol)
        d.rectangle([x + 7, y + 16, x + 15, y + 18], fill=wcol)
    elif kind == "cuffs":
        d.ellipse([x + 4, y + 7, x + 11, y + 14], outline=wcol, width=2)
        d.ellipse([x + 11, y + 7, x + 18, y + 14], outline=wcol, width=2)
    elif kind == "heli":
        d.ellipse([x + 6, y + 9, x + 16, y + 15], outline=wcol, width=2)
        d.line([x + 3, y + 8, x + 19, y + 8], fill=wcol, width=2)
    elif kind == "blast":
        d.polygon([(x + 11, y + 3), (x + 14, y + 9), (x + 19, y + 9),
                   (x + 15, y + 13), (x + 17, y + 19), (x + 11, y + 15),
                   (x + 5, y + 19), (x + 7, y + 13), (x + 3, y + 9),
                   (x + 8, y + 9)], fill=wcol)
    elif kind == "target":
        d.ellipse([x + 5, y + 5, x + 17, y + 17], outline=wcol, width=2)
        d.ellipse([x + 9, y + 9, x + 13, y + 13], fill=wcol)
    elif kind == "flame":
        d.polygon([(x + 11, y + 3), (x + 16, y + 11), (x + 14, y + 18),
                   (x + 8, y + 18), (x + 6, y + 11)], fill=wcol)
    elif kind == "chip":
        d.rectangle([x + 7, y + 7, x + 15, y + 15], fill=wcol)
        for i in range(3):
            d.line([x + 9 + i * 3, y + 4, x + 9 + i * 3, y + 7], fill=wcol, width=1)
            d.line([x + 9 + i * 3, y + 15, x + 9 + i * 3, y + 18], fill=wcol, width=1)
    elif kind == "ship":
        d.polygon([(x + 4, y + 12), (x + 18, y + 12), (x + 15, y + 18),
                   (x + 7, y + 18)], fill=wcol)
        d.rectangle([x + 9, y + 5, x + 13, y + 12], fill=wcol)

TIER2 = [
    ("tower", "PIF TOWER HIT, RIYADH — 11 wounded", "CONFIRMED", "Saudi authorities"),
    ("arrow", "HOUTHIS 60 KM FROM ADEN", "OFFICIAL", "Yemen military"),
    ("trophy", "SENEGAL AFCON CHAMPIONS — reinstated", "CONFIRMED", "Court of Arbitration for Sport"),
    ("cuffs", "EL CHAPO ISIDRO CAPTURED in Sinaloa", "OFFICIAL", "Mexican Attorney General"),
    ("heli", "TURKISH HELICOPTER CRASH — 5 crew killed", "OFFICIAL", "Defence Ministry"),
    ("blast", "VILLAVICENCIO CAR BOMB — 23 injured", "REPORTED", "Wire reports"),
    ("target", "HAMAS SECURITY CHIEF KILLED in Gaza", "REPORTED", "Wire reports"),
    ("flame", "HANOI BLAST — 6 killed, 10+ injured", "REPORTED", "Wire reports"),
    ("chip", "MEGASPEED BLACKLISTED by US", "OFFICIAL", "US Bureau of Industry and Security"),
    ("ship", "MALAYSIA RETURNS 6,803 MIGRANTS", "OFFICIAL", "PM Anwar Ibrahim"),
]
ty = T2Y + 28
for i, (kind, head, tag, src) in enumerate(TIER2):
    cx = MX + (i % 2) * (COLW + 16)
    cy = ty + (i // 2) * 24
    icon(d, cx, cy, kind, tag_color(tag))
    tf = fs(13, bold=True)
    d.text((cx + 28, cy + 3), head, font=tf, fill=INK)
    hw = tw(d, head, tf)
    badge(d, cx + 28 + int(hw) + 6, cy + 2, tag, tag_color(tag), size=10, h=16)
    d.text((cx + 28, cy + 3), "", font=tf, fill=INK)
    # source on the right end is cramped; put it after the tag when room allows
    # (kept short: sources are named in the tag row below via legend line)
d.text((MX, ty + 5 * 24 + 2),
       "Sources: Saudi authorities · Yemen military · Court of Arbitration for Sport · "
       "Mexican AG · Turkish Defence Ministry · US Bureau of Industry and Security · "
       "PM Anwar Ibrahim",
       font=fs(11), fill=GREY)

# ---------- briefs: large bold-lead type, grouped by region ----------
BY = ty + 5 * 24 + 18
d.text((MX, BY), "IN BRIEF — AROUND THE WORLD", font=fs(16, bold=True), fill=INK)
d.rectangle([MX, BY + 20, W - MX, BY + 21], fill=INK)
BRIEFS = [
    ("MIDDLE EAST", [
        ("GAZA MENINGITIS: ", "272 cases in Oct, 8x normal."),
        ("SAUDI STRIKES ON YEMEN: ", "25 dead or missing."),
        ("IRAQ TAKES KURD OILFIELDS: ", "federal control ordered."),
        ("HAFTAR IN TURKEY: ", "visits Ankara; meets Erdogan."),
        ("UK SANCTIONS HOUTHIS: ", "freezes + bans on 4 officials."),
        ("YEMEN AID CRISIS: ", "vaccine crisis; staffer killed."),
    ]),
    ("ASIA & PACIFIC", [
        ("ULLEUNGDO SHELTER ORDER: ", "Russian jets enter ADIZ."),
        ("INDONESIA VP RACE: ", "Amran + Sugiono nominated."),
        ("HASINA TO RETURN: ", "plans return 16 Dec from exile."),
        ("CHINA DEATH SENTENCE: ", "Ma spied; 35 secrets."),
        ("NEPAL QUAKE: ", "magnitude 5.6 near China border."),
        ("NORTH KOREA: ", "wants Swiss Pyongyang office closed."),
        ("SOLOMON ISLANDS: ", "Australia is primary partner."),
        ("MARKETS: ", "Nvidia −7%; Nikkei +3.9%; Brent $86.7."),
    ]),
    ("WORLD", [
        ("DR CONGO PLANE MISSING: ", "Cessna 208 lost; 4 aboard."),
        ("NATO SPACE WARNING: ", "Rutte vows space defence."),
        ("PENTAGON REBUKES CANADA: ", "41.9% fleet serviceable."),
        ("ZELENSKY URGES TALKS: ", "wants 4-party meeting soon."),
        ("HAITI: ", "3 Salvadoran soldiers killed in blast."),
        ("US TARIFFS COMING: ", "on China, EU + others (AP)."),
        ("UN ROBOT TALKS FAIL: ", "killer-robot rules deadlocked."),
        ("QUASAR RECORD: ", "quasar 630m yrs after Big Bang."),
        ("RUSSIAN LOSSES: ", "700,000+ dead or missing."),
        ("POPE'S DIARY: ", "Francis' crisis; vision of hell."),
    ]),
]
bcolw = (W - 2 * MX - 24) // 3
by = BY + 26
maxrows = 0
for ci, (region, items) in enumerate(BRIEFS):
    bx = MX + ci * (bcolw + 12)
    d.text((bx, by), region, font=fs(12, bold=True), fill=RED)
    yy = by + 16
    for lead, rest in items:
        f1, f2 = fs(12, bold=True), fs(12)
        d.text((bx, yy), lead, font=f1, fill=INK)
        d.text((bx + tw(d, lead, f1), yy), rest, font=f2, fill=INK)
        yy += 14
    maxrows = max(maxrows, yy)
by = maxrows + 4

# ---------- UTC timeline strip ----------
d.rectangle([MX, by, W - MX, by + 26], fill=(232, 228, 216))
tl1 = ("UTC TIMELINE   00:00 Hormuz tankers  ·  00:52 Megaspeed  ·  "
       "02:09 El Chapo Isidro  ·  05:54 Malaysia migrants  ·  "
       "08:14 Ukraine ships  ·  08:16 Hanoi blast")
tl2 = ("11:40 Hamas chief  ·  11:45 Villavicencio bomb  ·  14:27 PIF tower  ·  "
       "16:51 Houthis near Aden  ·  17:35 Cartagena  ·  "
       "19:52 Helicopter crash  ·  20:41 Huawei verdict")
d.text((MX + 6, by + 1), tl1, font=fs(12, bold=True), fill=INK)
d.text((MX + 6, by + 13), tl2, font=fs(12, bold=True), fill=INK)
by += 30

# ---------- date check + how-sure legend + footer ----------
dc = ("DATE CHECK — NOT 24 NOV, SO NOT HERE:  ICJ Myanmar ruling (19 Nov)  ·  "
      "Shenzhou-24 launch (25 Nov)  ·  Guterres AI call (23 Nov)  ·  FARC anniversary (25 Nov)")
d.text((MX, by), dc, font=fs(12), fill=GREY)
by += 16
d.text((MX, by),
       "HOW SURE:  CONFIRMED = 2+ outlets or official record  ·  OFFICIAL = on the record  ·  "
       "REPORTED = one outlet  ·  CLAIM = one side's account",
       font=fs(11, bold=True), fill=INK)

img.save(os.path.join(BASE, "entry.png"), optimize=True)
print("saved entry.png", img.size)
