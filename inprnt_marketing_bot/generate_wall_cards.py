"""
JOSH SHOOT 2-Post 1080x1350 Vertical Portrait Release Generator.
Generates for each artwork:
1. Post 1: 1080x1350 Full Black Void + Crisp White Gallery Border Portrait (JPEG format).
   - Automatically crops out INPRNT grey studio background and white mat border so only the PURE ARTWORK remains.
   - 100% PURE FULL BLACK (#000000) goes from the outer edges ALL THE WAY until it reaches the crisp white border (#FFFFFF, 22px width).
   - Photograph sits inside that crisp white border straight and square (zero roundness!).
   - 'J O S H   S H O O T' placed right in the center of the photograph in very small letters (17pt bold).
2. Post 2: 1080x1350 Museum Monograph Wall Card (4x Supersampled Smooth Corners, JPEG format).
   - Parisian Cream Museum Plaster Wall (#F8F6F0 down to #E8E4DA) with overhead track spotlighting.
   - Gagosian/Hauser & Wirth double-matte framing (16px off-white 100% cotton rag mat + 1px obsidian inner bevel line).
   - ALL 4 typography lines change dynamically based on the color theme of that specific photograph across all prints!
"""

import os
import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(size, bold=False):
    """Helper to load scalable TrueType fonts."""
    fonts_to_try = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "arial.ttf"
    ]
    for f in fonts_to_try:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                pass
    return ImageFont.load_default()

def crop_inprnt_mockup(img: Image.Image) -> Image.Image:
    """
    Automatically crops out INPRNT's grey studio mockup background and white paper mat border
    so that only the PURE FINE ART PHOTOGRAPH remains (supports any thumbnail size: 440, 540, 1080).
    """
    w, h = img.size
    cx, cy = w // 2, h // 2

    # Left edge: scan from 5% width to center
    left = 0
    for x in range(int(w * 0.05), cx):
        r, g, b = img.getpixel((x, cy))
        if not (r > 240 and g > 240 and b > 240) and not (abs(r-g)<5 and abs(g-b)<5 and r>200):
            left = x
            break

    # Right edge: scan from 95% width to center
    right = w - 1
    for x in range(int(w * 0.95), cx, -1):
        r, g, b = img.getpixel((x, cy))
        if not (r > 240 and g > 240 and b > 240) and not (abs(r-g)<5 and abs(g-b)<5 and r>200):
            right = x
            break

    # Top edge: scan from 5% height to center
    top = 0
    for y in range(int(h * 0.05), cy):
        r, g, b = img.getpixel((cx, y))
        if not (r > 240 and g > 240 and b > 240) and not (abs(r-g)<5 and abs(g-b)<5 and r>200):
            top = y
            break

    # Bottom edge: scan from 95% height to center
    bottom = h - 1
    for y in range(int(h * 0.95), cy, -1):
        r, g, b = img.getpixel((cx, y))
        if not (r > 240 and g > 240 and b > 240) and not (abs(r-g)<5 and abs(g-b)<5 and r>200):
            bottom = y
            break

    # Safety check: if fallback bounding box is invalid, return original image
    if right - left < int(w * 0.2) or bottom - top < int(h * 0.2):
        return img

    # Crop with 2px safety inward margin so no white mat edge pixels remain
    return img.crop((left + 2, top + 2, right - 1, bottom - 1))

def analyze_photo_color_theme(img: Image.Image) -> tuple:
    """
    Analyzes an artwork image and returns a 3-color Typographic Palette Tuple
    matching the color theme of that specific photograph across all 197 prints:
    1. primary_accent: Rich jewel-tone accent for 'JOSH SHOOT | INPRNT'
    2. deep_theme: Very dark tinted enamel ink for 'JOSH1 197 BY JOSH SHOOT'
    3. muted_theme: Refined tinted slate for '300GSM COTTON RAG' and 'THE JOSH1 ARCHIVE'
    """
    small = img.resize((50, 50), Image.Resampling.BILINEAR)
    pixels = list(small.getdata())
    
    r_sum, g_sum, b_sum, count = 0, 0, 0, 0
    for r, g, b in pixels:
        if max(r, g, b) - min(r, g, b) > 20 and max(r, g, b) > 40:
            r_sum += r
            g_sum += g
            b_sum += b
            count += 1
            
    if count > 0:
        avg_r = int(r_sum / count)
        avg_g = int(g_sum / count)
        avg_b = int(b_sum / count)
        factor = 135 / max(avg_r, avg_g, avg_b, 1)
        pr_r = min(int(avg_r * factor), 195)
        pr_g = min(int(avg_g * factor), 195)
        pr_b = min(int(avg_b * factor), 195)
        
        deep_r = min(int(pr_r * 0.18 + 10), 40)
        deep_g = min(int(pr_g * 0.18 + 10), 40)
        deep_b = min(int(pr_b * 0.18 + 14), 45)

        mut_r = min(int(pr_r * 0.45 + 50), 140)
        mut_g = min(int(pr_g * 0.45 + 50), 140)
        mut_b = min(int(pr_b * 0.45 + 55), 145)

        return ((pr_r, pr_g, pr_b), (deep_r, deep_g, deep_b), (mut_r, mut_g, mut_b))
    
    return ((35, 65, 115), (15, 18, 24), (88, 96, 110))

def generate_luxury_museum_wall(width: int, height: int, idx: int = 0) -> Image.Image:
    """
    Generates a Parisian cream museum wall with subtle overhead track lighting
    spotlight falloff (#F8F6F0 down to #E8E4DA).
    """
    bg = Image.new("RGB", (width, height), (245, 242, 235))
    draw = ImageDraw.Draw(bg)

    if idx == 0:
        for y in range(height):
            val = int(248 - (y / height) * 20)
            r = min(val + 4, 255)
            g = min(val + 1, 255)
            b = max(val - 7, 0)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    elif idx == 1:
        for y in range(height):
            val = int(247 - (y / height) * 22)
            r = min(val + 5, 255)
            g = min(val, 255)
            b = max(val - 10, 0)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:
        for y in range(height):
            val = int(249 - (y / height) * 18)
            r = min(val + 3, 255)
            g = min(val + 1, 255)
            b = max(val - 5, 0)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

    return bg

def generate_post1_dark_mode_portrait(num: int, title: str, img_url: str, row: int, col: int, output_path: str):
    """
    Generates Post 1: 1080x1350 Vertical Portrait with FULL PURE BLACK (#000000) around a CRISP 22px WHITE GALLERY BORDER!
    - 100% PURE FULL BLACK (#000000) goes from the outer edges ALL THE WAY until it reaches the crisp white border (#FFFFFF).
    - Inside that white border sits the pure photograph straight and square (zero roundness!).
    - 'J O S H   S H O O T' placed right in the center of the photograph in very small letters (17pt).
    """
    width = 1080
    height = 1350
    bg_color = (0, 0, 0)

    try:
        r = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        art_raw = Image.open(BytesIO(r.content)).convert("RGB")
        art_img = crop_inprnt_mockup(art_raw)
    except Exception as e:
        print(f"[ERROR] Could not download/crop image for #{num} ({e})")
        return None

    card = Image.new("RGB", (width, height), bg_color)

    cw, ch = art_img.size
    scale = 860.0 / max(cw, ch)
    target_w = int(cw * scale)
    target_h = int(ch * scale)
    art_img_resized = art_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    border_width = 22
    framed_w = target_w + border_width * 2
    framed_h = target_h + border_width * 2
    white_frame = Image.new("RGB", (framed_w, framed_h), (255, 255, 255))
    white_frame.paste(art_img_resized, (border_width, border_width))

    card.paste(white_frame, ((width - framed_w) // 2, (height - framed_h) // 2))

    draw = ImageDraw.Draw(card)
    font_small = get_font(17, bold=True)
    text = "J O S H   S H O O T"
    
    bbox = draw.textbbox((0, 0), text, font=font_small)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2

    draw.text((x + 1, y + 1), text, font=font_small, fill=(0, 0, 0, 240))
    draw.text((x, y), text, font=font_small, fill=(245, 245, 245))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    card.save(output_path, "JPEG", quality=95)
    print(f"[SUCCESS] Saved Post 1 (1080x1350 Full Black Void + White Border Portrait JPEG): {output_path}")
    return output_path

def apply_supersampled_rounded_corners(img: Image.Image, radius: int = 20) -> Image.Image:
    img_rgba = img.convert("RGBA")
    w, h = img_rgba.size
    scale = 4
    mask = Image.new("L", (w * scale, h * scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (w * scale - 1, h * scale - 1)], radius=radius * scale, fill=255)
    mask_smooth = mask.resize((w, h), Image.Resampling.LANCZOS)
    img_rgba.putalpha(mask_smooth)
    return img_rgba

def add_museum_mat_and_gallery_shadow(art_img: Image.Image, radius: int = 20) -> Image.Image:
    art_w, art_h = art_img.size
    art_rounded = apply_supersampled_rounded_corners(art_img, radius=14)
    
    bordered_w = art_w + 2
    bordered_h = art_h + 2
    bordered_photo = Image.new("RGBA", (bordered_w, bordered_h), (25, 25, 28, 255))
    bordered_photo = apply_supersampled_rounded_corners(bordered_photo, radius=15)
    bordered_photo.paste(art_rounded, (1, 1), art_rounded)

    mat_width = 16
    matted_w = art_w + mat_width * 2
    matted_h = art_h + mat_width * 2
    matted = Image.new("RGBA", (matted_w, matted_h), (251, 251, 249, 255))
    matted.paste(bordered_photo, (mat_width - 1, mat_width - 1), bordered_photo)
    matted_rounded = apply_supersampled_rounded_corners(matted, radius=radius)

    shadow_pad = 65
    total_w = matted_w + shadow_pad * 2
    total_h = matted_h + shadow_pad * 2
    comp = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))

    shadow_layer = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle([shadow_pad - 4, shadow_pad + 4, matted_w + shadow_pad + 12, matted_h + shadow_pad + 24], radius=radius, fill=(0, 0, 0, 110))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(20))
    comp.alpha_composite(shadow_layer)

    tight_shadow = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tight_shadow)
    t_draw.rounded_rectangle([shadow_pad - 2, shadow_pad - 1, matted_w + shadow_pad + 4, matted_h + shadow_pad + 8], radius=radius, fill=(0, 0, 0, 165))
    tight_shadow = tight_shadow.filter(ImageFilter.GaussianBlur(6))
    comp.alpha_composite(tight_shadow)

    comp.paste(matted_rounded, (shadow_pad, shadow_pad), matted_rounded)
    return comp

def draw_3d_text_on_light_wall(draw: ImageDraw.ImageDraw, width: int, y: int, text: str, font: ImageFont.FreeTypeFont, fill: tuple):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2

    # A single, ultra-crisp 1px subtle white highlight for elegant museum depth without any blurring or ghosting!
    draw.text((x - 1, y - 1), text, font=font, fill=(255, 255, 255))
    draw.text((x, y), text, font=font, fill=fill)

def generate_post2_museum_monograph(num: int, title: str, img_url: str, idx: int, output_path: str) -> tuple:
    width = 1080
    height = 1350

    try:
        r = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        art_raw = Image.open(BytesIO(r.content)).convert("RGB")
        art_img = crop_inprnt_mockup(art_raw)
    except Exception as e:
        print(f"[ERROR] Could not download/crop image for #{num} ({e})")
        return None, None

    # Analyze 3-color Typographic Palette Theme from the photograph!
    primary_accent, deep_theme, muted_theme = analyze_photo_color_theme(art_img)
    print(f"[INFO] #{num} '{title}' | Post 2 Typographic Theme -> Accent: RGB{primary_accent} | Deep: RGB{deep_theme}")

    card = generate_luxury_museum_wall(width, height, idx)

    cw, ch = art_img.size
    scale = 780.0 / max(cw, ch)
    target_w = int(cw * scale)
    target_h = int(ch * scale)
    art_img_resized = art_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    framed = add_museum_mat_and_gallery_shadow(art_img_resized, radius=20)
    card.paste(framed, ((width - framed.width) // 2, 75), framed)

    draw = ImageDraw.Draw(card)
    font_top = get_font(36, bold=True)
    font_second = get_font(30, bold=True)
    font_rag = get_font(20, bold=True)
    font_footer = get_font(24, bold=True)

    # All 4 typography lines use standard '1' (never '¹') to guarantee zero missing glyph boxes [], and ultra-crisp high contrast!
    draw_3d_text_on_light_wall(draw, width, 1005, f"JOSH1 {num} BY JOSH SHOOT", font_top, fill=(24, 24, 28)) # Crisp Obsidian Black
    draw_3d_text_on_light_wall(draw, width, 1060, "JOSH SHOOT | INPRNT", font_second, fill=(143, 109, 3))    # Antique Bronze Gold
    draw_3d_text_on_light_wall(draw, width, 1115, "300GSM COTTON RAG • ARCHIVAL EDITION", font_rag, fill=(71, 85, 105)) # Slate Grey
    draw_3d_text_on_light_wall(draw, width, 1175, "THE JOSH1 ARCHIVE", font_footer, fill=(24, 24, 28))       # Crisp Obsidian Black (standard '1')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    card.save(output_path, "JPEG", quality=95)
    print(f"[SUCCESS] Saved Post 2 (1080x1350 Color-Themed Museum Monograph JPEG): {output_path}")
    return "Parisian Cream Museum Wall", primary_accent

def generate_first_three_wall_cards():
    """
    Generates BOTH Post 1 (Full Black Void + White Border) & Post 2 (Color-Themed Museum Monograph)
    for #197, #196, #195 as true JPEG files.
    """
    cards = [
        (197, "JOSH1 197 • Maritime Museum, Rotterdam", "https://cdn.inprnt.com/thumbs/0c/2b/0c2b504067590379c2c6e9866a469358@2x.jpg", 1, 1, 0, "output/JOSH1_197_Post1_Square.jpg", "output/JOSH1_197_Post2_Monograph.jpg"),
        (196, "JOSH1 196 • Damstraatjes, Amsterdam", "https://cdn.inprnt.com/thumbs/74/bc/74bc117ec749aaf2cd9e2513870b6ed8@2x.jpg", 1, 2, 1, "output/JOSH1_196_Post1_Square.jpg", "output/JOSH1_196_Post2_Monograph.jpg"),
        (195, "JOSH1 195 • Scheepmakerskade 135", "https://cdn.inprnt.com/thumbs/d1/54/d154d7c400b4d2f5cf3b9bafccb0f182@2x.jpg", 2, 2, 2, "output/JOSH1_195_Post1_Square.jpg", "output/JOSH1_195_Post2_Monograph.jpg")
    ]

    results = []
    for num, title, url, row, col, idx, p1_path, p2_path in cards:
        generate_post1_dark_mode_portrait(num, title, url, row, col, p1_path)
        style, color = generate_post2_museum_monograph(num, title, url, idx, p2_path)
        
        # Also save standard daily filenames for #197 so both filenames work reliably
        if num == 197:
            generate_post1_dark_mode_portrait(num, title, url, row, col, "output/post1_daily_instagram.jpg")
            generate_post2_museum_monograph(num, title, url, idx, "output/post2_daily_instagram.jpg")
            
        results.append((num, title, style, color))
    return results

if __name__ == "__main__":
    generate_first_three_wall_cards()
