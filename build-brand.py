#!/usr/bin/env python3
"""
Generate Setmore-ready brand assets:
  - brand/logo-512.png   : profile logo, 512x512
  - brand/logo-1024.png  : profile logo, 1024x1024
  - brand/logo-square-wordmark.png : full logo with text, 1024x1024
  - brand/banner-4runner.jpg : main banner, 1920x600, 4Runner backdrop
  - brand/banner-angel.jpg   : alt banner, 1920x600, Angel-in-action backdrop
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "brand")
os.makedirs(OUT, exist_ok=True)

INK       = (15, 23, 42)     # slate-900
ACCENT    = (245, 158, 11)   # amber-500
ACCENT_LT = (251, 191, 36)   # amber-400
WHITE     = (255, 255, 255)
SLATE300  = (203, 213, 225)

ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
ARIAL_BOLD  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL       = "/System/Library/Fonts/Supplemental/Arial.ttf"


# ---------- LOGO (profile) ----------

def make_profile_logo(size: int, path: str):
    """Orange circle with dark 'R' and a small white shine dot — clean and legible."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Radial-ish gradient for the circle: paint a full amber circle,
    # then overlay a lighter amber upper-left glow for subtle dimension.
    pad = max(4, size // 64)
    d.ellipse((pad, pad, size - pad, size - pad), fill=ACCENT)

    # Subtle highlight — lighter amber circle in upper left, semi-transparent
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    off = size // 6
    gd.ellipse(
        (pad + off, pad + off, size - pad - off * 2, size - pad - off * 2),
        fill=(251, 191, 36, 150),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=size // 20))
    img = Image.alpha_composite(img, glow)

    # Big bold 'R' centered — Arial Black at ~60% of circle height
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(ARIAL_BLACK, int(size * 0.62))
    text = "R"
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    # nudge slightly up — Arial Black has a lot of bottom padding visually
    ty = (size - th) / 2 - bbox[1] - size * 0.03
    d.text((tx, ty), text, font=font, fill=INK)

    # Small white "shine" dot in upper-right quadrant
    sd_size = max(size // 14, 8)
    sx = int(size * 0.72)
    sy = int(size * 0.28)
    d.ellipse(
        (sx - sd_size, sy - sd_size, sx + sd_size, sy + sd_size),
        fill=(255, 255, 255, 230),
    )

    img.save(path, "PNG", optimize=True)
    print(f"✓ {path}")


def make_square_wordmark(path: str):
    """Square version including business name + tagline for use in places that support larger brand images."""
    size = 1024
    margin = int(size * 0.08)  # 8% safe margin
    max_w = size - margin * 2

    img = Image.new("RGBA", (size, size), INK)
    d = ImageDraw.Draw(img)

    # Top + bottom amber accent bands
    d.rectangle((0, 0, size, 14), fill=ACCENT)
    d.rectangle((0, size - 14, size, size), fill=ACCENT)

    # Central circle mark
    circle_d = int(size * 0.34)
    cx, cy = size // 2, int(size * 0.30)
    d.ellipse(
        (cx - circle_d // 2, cy - circle_d // 2, cx + circle_d // 2, cy + circle_d // 2),
        fill=ACCENT,
    )
    font_r = ImageFont.truetype(ARIAL_BLACK, int(circle_d * 0.62))
    bbox = d.textbbox((0, 0), "R", font=font_r)
    d.text(
        (cx - (bbox[2] - bbox[0]) / 2 - bbox[0],
         cy - (bbox[3] - bbox[1]) / 2 - bbox[1] - circle_d * 0.03),
        "R",
        font=font_r,
        fill=INK,
    )
    # Shine dot
    sd = circle_d // 14
    sx = cx + int(circle_d * 0.22)
    sy = cy - int(circle_d * 0.22)
    d.ellipse((sx - sd, sy - sd, sx + sd, sy + sd), fill=(255, 255, 255, 230))

    # Stacked wordmark — auto-size so the longer word fits within max_w
    def fit_font(text, font_path, max_width, start_size):
        fs = start_size
        while fs > 20:
            f = ImageFont.truetype(font_path, fs)
            bbox = d.textbbox((0, 0), text, font=f)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                return f, w, bbox[3] - bbox[1]
            fs -= 2
        f = ImageFont.truetype(font_path, 20)
        bbox = d.textbbox((0, 0), text, font=f)
        return f, bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Stacked wordmark
    word1 = "REFLECTION"
    word2 = "DETAILING"
    f1, _, _ = fit_font(word1, ARIAL_BLACK, max_w, 100)
    f2, _, _ = fit_font(word2, ARIAL_BLACK, max_w, 100)
    chosen_size = min(f1.size, f2.size)
    font_brand = ImageFont.truetype(ARIAL_BLACK, chosen_size)

    # Use font metrics (ascent + descent) for reliable line height
    ascent, descent = font_brand.getmetrics()
    line_h = ascent + descent  # full em height

    def centered_text(text, font, y, fill):
        w = d.textlength(text, font=font)
        d.text(((size - w) / 2, y), text, font=font, fill=fill)

    # Bottom-up layout from within the safe area
    safe_bottom = size - 14 - 30  # above bottom accent bar, with padding

    cert = "IGL COATINGS CERTIFIED  ·  HTL DETAILING CERTIFIED"
    f_cert, _, _ = fit_font(cert, ARIAL_BOLD, max_w, 22)
    cert_ascent, cert_descent = f_cert.getmetrics()
    cert_h = cert_ascent + cert_descent

    tag = "MOBILE AUTO DETAILING  ·  CHULA VISTA"
    f_tag, _, _ = fit_font(tag, ARIAL_BOLD, max_w, 30)
    tag_ascent, tag_descent = f_tag.getmetrics()
    tag_h = tag_ascent + tag_descent

    # Place bottom-to-top
    y_cert = safe_bottom - cert_h
    y_tag = y_cert - 16 - tag_h
    y_word2 = y_tag - 36 - line_h
    y_word1 = y_word2 - 10 - line_h

    centered_text(word1, font_brand, y_word1, WHITE)
    centered_text(word2, font_brand, y_word2, WHITE)
    centered_text(tag, f_tag, y_tag, ACCENT)
    centered_text(cert, f_cert, y_cert, SLATE300)

    img.save(path, "PNG", optimize=True)
    print(f"✓ {path}")


# ---------- BANNER ----------

def draw_star(draw, cx, cy, r, fill):
    """Draw a 5-pointed star polygon."""
    import math
    pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(angle), cy + rr * math.sin(angle)))
    draw.polygon(pts, fill=fill)


def make_banner(photo_rel: str, out_path: str, headline="REFLECTION DETAILING",
                tagline="Mobile Auto Detailing  ·  Chula Vista  ·  South San Diego",
                certs="IGL COATINGS CERTIFIED   ·   HTL DETAILING CERTIFIED",
                rating="5.0",
                align="left", gradient="left"):
    """Build a 1920x600 banner by compositing a photo + overlay + title text."""
    W, H = 1920, 600

    # Load and cover-fit the photo
    photo = Image.open(os.path.join(HERE, photo_rel)).convert("RGB")
    pw, ph = photo.size
    # Cover-fit
    ratio = max(W / pw, H / ph)
    new_w, new_h = int(pw * ratio), int(ph * ratio)
    photo = photo.resize((new_w, new_h), Image.LANCZOS)
    # Center crop
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    photo = photo.crop((left, top, left + W, top + H))

    banner = photo.copy().convert("RGBA")

    # Dark overlay — horizontal gradient from ink (heavy on text side) fading out
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    if gradient == "left":
        for x in range(W):
            # heavier ink on left, very light on right
            t = x / W
            a = int(230 * (1 - t) + 40)  # 230 → 40 alpha
            od.line([(x, 0), (x, H)], fill=(15, 23, 42, a))
    else:
        for y in range(H):
            t = y / H
            a = int(40 + 180 * t)  # top lighter, bottom heavier
            od.line([(0, y), (W, y)], fill=(15, 23, 42, a))
    banner = Image.alpha_composite(banner, overlay)

    # Top amber accent bar
    d = ImageDraw.Draw(banner)
    d.rectangle((0, 0, W, 10), fill=ACCENT)
    # Bottom amber accent bar
    d.rectangle((0, H - 10, W, H), fill=ACCENT)

    # Logo (small amber circle) + wordmark, left-aligned
    pad_x = 90
    pad_y = 90
    circle_size = 120
    # Circle
    d.ellipse((pad_x, pad_y + 40, pad_x + circle_size, pad_y + 40 + circle_size), fill=ACCENT)
    # R in circle
    r_font = ImageFont.truetype(ARIAL_BLACK, int(circle_size * 0.65))
    bbox = d.textbbox((0, 0), "R", font=r_font)
    d.text(
        (pad_x + circle_size / 2 - (bbox[2] - bbox[0]) / 2 - bbox[0],
         pad_y + 40 + circle_size / 2 - (bbox[3] - bbox[1]) / 2 - bbox[1] - circle_size * 0.03),
        "R",
        font=r_font,
        fill=INK,
    )
    # Shine dot
    sd = circle_size // 12
    d.ellipse(
        (pad_x + int(circle_size * 0.72) - sd,
         pad_y + 40 + int(circle_size * 0.28) - sd,
         pad_x + int(circle_size * 0.72) + sd,
         pad_y + 40 + int(circle_size * 0.28) + sd),
        fill=(255, 255, 255, 230),
    )

    # Headline
    headline_font = ImageFont.truetype(ARIAL_BLACK, 86)
    text_x = pad_x + circle_size + 40
    text_y = pad_y + 50
    d.text((text_x, text_y), headline, font=headline_font, fill=WHITE)

    # Tagline
    tag_font = ImageFont.truetype(ARIAL_BOLD, 34)
    d.text((text_x, text_y + 110), tagline, font=tag_font, fill=ACCENT)

    # Certifications bar
    cert_font = ImageFont.truetype(ARIAL_BOLD, 26)
    certs_y = text_y + 170
    d.text((text_x, certs_y), certs, font=cert_font, fill=SLATE300)
    # Append rating with a drawn star — avoids font glyph issues
    bbox = d.textbbox((0, 0), certs, font=cert_font)
    certs_w = bbox[2] - bbox[0]
    sep_x = text_x + certs_w + 20
    d.text((sep_x, certs_y), "·", font=cert_font, fill=SLATE300)
    bbox = d.textbbox((0, 0), "·", font=cert_font)
    sep_w = bbox[2] - bbox[0]
    rating_x = sep_x + sep_w + 20
    # Star glyph (amber)
    star_r = 13
    draw_star(d, rating_x + star_r, certs_y + 18, star_r, ACCENT)
    # Rating text
    d.text((rating_x + star_r * 2 + 10, certs_y), rating, font=cert_font, fill=SLATE300)

    # Phone call-out — right side
    phone_font = ImageFont.truetype(ARIAL_BLACK, 56)
    phone = "(619) 341-0016"
    bbox = d.textbbox((0, 0), phone, font=phone_font)
    phone_w = bbox[2] - bbox[0]
    phone_x = W - phone_w - 90
    phone_y = H - 150
    # Subtle "CALL / TEXT" label
    label_font = ImageFont.truetype(ARIAL_BOLD, 22)
    d.text((phone_x, phone_y - 30), "CALL OR TEXT", font=label_font, fill=ACCENT)
    d.text((phone_x, phone_y), phone, font=phone_font, fill=WHITE)

    banner.convert("RGB").save(out_path, "JPEG", quality=88, optimize=True)
    print(f"✓ {out_path}")


# ---------- APPLE TOUCH ICON (180x180, no transparency) ----------

def make_apple_touch_icon(path: str):
    """180x180 iOS home screen icon — solid ink background with amber R circle centered."""
    size = 180
    img = Image.new("RGB", (size, size), INK)
    d = ImageDraw.Draw(img)

    # Amber circle filling most of the square (iOS auto-rounds corners)
    pad = int(size * 0.08)
    d.ellipse((pad, pad, size - pad, size - pad), fill=ACCENT)

    # Bold R
    font = ImageFont.truetype(ARIAL_BLACK, int(size * 0.55))
    bbox = d.textbbox((0, 0), "R", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text(
        ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1] - size * 0.03),
        "R",
        font=font,
        fill=INK,
    )

    # Shine dot
    sd_size = max(size // 14, 6)
    sx = int(size * 0.70)
    sy = int(size * 0.28)
    d.ellipse(
        (sx - sd_size, sy - sd_size, sx + sd_size, sy + sd_size),
        fill=WHITE,
    )

    img.save(path, "PNG", optimize=True)
    print(f"✓ {path}")


# ---------- TWITTER CARD (1200x628, Twitter's spec) ----------

def make_twitter_card(photo_rel: str, out_path: str):
    """1200x628 (1.91:1) — Twitter's recommended summary_large_image ratio.
    Also safe for Open Graph fallbacks on platforms that prefer this ratio.
    """
    W, H = 1200, 628

    photo = Image.open(os.path.join(HERE, photo_rel)).convert("RGB")
    pw, ph = photo.size
    ratio = max(W / pw, H / ph)
    new_w, new_h = int(pw * ratio), int(ph * ratio)
    photo = photo.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    photo = photo.crop((left, top, left + W, top + H))

    card = photo.copy().convert("RGBA")

    # Dark overlay — slightly heavier at bottom for text legibility
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        t = y / H
        a = int(60 + 180 * t)  # top lighter, bottom darker
        od.line([(0, y), (W, y)], fill=(15, 23, 42, a))
    card = Image.alpha_composite(card, overlay)

    d = ImageDraw.Draw(card)

    # Amber accent bars
    d.rectangle((0, 0, W, 10), fill=ACCENT)
    d.rectangle((0, H - 10, W, H), fill=ACCENT)

    # Logo badge — left, bottom half
    pad = 70
    circle_size = 110
    circle_x = pad
    circle_y = H - circle_size - pad - 100
    d.ellipse((circle_x, circle_y, circle_x + circle_size, circle_y + circle_size), fill=ACCENT)
    r_font = ImageFont.truetype(ARIAL_BLACK, int(circle_size * 0.65))
    bbox = d.textbbox((0, 0), "R", font=r_font)
    d.text(
        (circle_x + circle_size / 2 - (bbox[2] - bbox[0]) / 2 - bbox[0],
         circle_y + circle_size / 2 - (bbox[3] - bbox[1]) / 2 - bbox[1] - circle_size * 0.03),
        "R", font=r_font, fill=INK,
    )
    sd = circle_size // 12
    d.ellipse(
        (circle_x + int(circle_size * 0.72) - sd, circle_y + int(circle_size * 0.28) - sd,
         circle_x + int(circle_size * 0.72) + sd, circle_y + int(circle_size * 0.28) + sd),
        fill=(255, 255, 255, 230),
    )

    # Headline next to logo — "REFLECTION DETAILING"
    text_x = circle_x + circle_size + 28
    text_y = circle_y + 8
    headline_font = ImageFont.truetype(ARIAL_BLACK, 58)
    d.text((text_x, text_y), "REFLECTION DETAILING", font=headline_font, fill=WHITE)

    # Tagline
    tag_font = ImageFont.truetype(ARIAL_BOLD, 26)
    d.text((text_x, text_y + 74), "Mobile Auto Detailing  ·  Chula Vista, CA", font=tag_font, fill=ACCENT)

    # Bottom strip with certs + phone
    strip_font = ImageFont.truetype(ARIAL_BOLD, 22)
    strip_y = H - 55
    d.text((pad, strip_y), "IGL COATINGS CERTIFIED  ·  HTL DETAILING CERTIFIED", font=strip_font, fill=SLATE300)
    phone_font = ImageFont.truetype(ARIAL_BLACK, 32)
    phone = "(619) 341-0016"
    bbox = d.textbbox((0, 0), phone, font=phone_font)
    phone_w = bbox[2] - bbox[0]
    d.text((W - phone_w - pad, strip_y - 4), phone, font=phone_font, fill=WHITE)

    card.convert("RGB").save(out_path, "JPEG", quality=88, optimize=True)
    print(f"✓ {out_path}")


if __name__ == "__main__":
    make_profile_logo(512, os.path.join(OUT, "logo-512.png"))
    make_profile_logo(1024, os.path.join(OUT, "logo-1024.png"))
    make_square_wordmark(os.path.join(OUT, "logo-square-wordmark.png"))
    make_banner("photos/4runner-exterior-after.jpg", os.path.join(OUT, "banner-4runner.jpg"))
    make_banner(
        "photos/angel-mustang-foam-wash.jpg",
        os.path.join(OUT, "banner-angel.jpg"),
        gradient="top",
    )
    make_apple_touch_icon(os.path.join(OUT, "apple-touch-icon.png"))
    make_twitter_card("photos/4runner-exterior-after.jpg", os.path.join(OUT, "twitter-card.jpg"))
    print("\nAll brand assets generated.")
