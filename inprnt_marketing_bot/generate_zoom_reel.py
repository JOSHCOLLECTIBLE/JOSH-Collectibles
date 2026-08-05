"""
JOSH¹ ARCHIVE - 1080x1920 (9:16) Cinematic Zoom-Out Reel & TikTok Video Generator
================================================================================
Generates automated 1080x1920 vertical MP4 video reels for any artwork (#222 down to #1).
- Automatically crops out INPRNT studio mockup borders.
- Applies a cinematic, ultra-smooth 1.15x -> 1.00x zoom-out over 4 seconds,
  followed by a 1-second full-frame hold.
- Features Parisian Cream Museum Plaster Wall and color-harmonized 3D embossed typography.
"""

import os
import time
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np

def get_font(size, bold=False):
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
    w, h = img.size
    cx, cy = w // 2, h // 2
    left = 0
    for x in range(int(w * 0.05), cx):
        r, g, b = img.getpixel((x, cy))
        if not (r > 240 and g > 240 and b > 240) and not (abs(r-g)<5 and abs(g-b)<5 and r>200):
            left = x
            break
    right = w - 1
    for x in range(int(w * 0.95), cx, -1):
        r, g, b = img.getpixel((x, cy))
        if not (r > 240 and g > 240 and b > 240) and not (abs(r-g)<5 and abs(g-b)<5 and r>200):
            right = x
            break
    top = 0
    for y in range(int(h * 0.05), cy):
        r, g, b = img.getpixel((cx, y))
        if not (r > 240 and g > 240 and b > 240) and not (abs(r-g)<5 and abs(g-b)<5 and r>200):
            top = y
            break
    bottom = h - 1
    for y in range(int(h * 0.95), cy, -1):
        r, g, b = img.getpixel((cx, y))
        if not (r > 240 and g > 240 and b > 240) and not (abs(r-g)<5 and abs(g-b)<5 and r>200):
            bottom = y
            break
    if right - left < int(w * 0.2) or bottom - top < int(h * 0.2):
        return img
    return img.crop((left + 2, top + 2, right - 1, bottom - 1))

def analyze_photo_color_theme(img: Image.Image) -> tuple:
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
    draw.text((x + 2, y + 3), text, font=font, fill=(160, 155, 145))
    draw.text((x + 1, y + 2), text, font=font, fill=(180, 175, 165))
    draw.text((x - 1, y - 1), text, font=font, fill=(255, 255, 255))
    draw.text((x, y), text, font=font, fill=fill)

def generate_tiktok_zoom_reel(num: int, title: str, img_url: str, output_path: str):
    """
    Generates a 1080x1920 (9:16) MP4 video with an ultra-smooth 1.15x -> 1.00x zoom-out
    over 4 seconds + 1 second hold (150 frames total at 30 fps).
    """
    print(f"🎬 [START] Generating 1080x1920 Cinematic Zoom-Out Reel for #{num}: '{title}'...")
    width, height = 1080, 1920

    r = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    art_raw = Image.open(BytesIO(r.content)).convert("RGB")
    art_img = crop_inprnt_mockup(art_raw)

    primary_accent, deep_theme, muted_theme = analyze_photo_color_theme(art_img)

    # Base Parisian Cream wall background for 1080x1920
    bg = Image.new("RGB", (width, height), (245, 242, 235))
    draw = ImageDraw.Draw(bg)
    for y in range(height):
        val = int(248 - (y / height) * 20)
        r_c = min(val + 4, 255)
        g_c = min(val + 1, 255)
        b_c = max(val - 7, 0)
        draw.line([(0, y), (width, y)], fill=(r_c, g_c, b_c))

    # Add Bold Museum-Exhibition 3D Typography at the bottom of 1080x1920 canvas
    font_top = get_font(64, bold=True)
    font_second = get_font(52, bold=True)
    font_rag = get_font(36, bold=False)
    font_footer = get_font(44, bold=True)

    draw_3d_text_on_light_wall(draw, width, 1400, f"JOSH1 {num} BY JOSH SHOOT", font_top, fill=deep_theme)
    draw_3d_text_on_light_wall(draw, width, 1500, "JOSH SHOOT | INPRNT", font_second, fill=primary_accent)
    draw_3d_text_on_light_wall(draw, width, 1590, "300GSM COTTON RAG • ARCHIVAL EDITION", font_rag, fill=muted_theme)
    draw_3d_text_on_light_wall(draw, width, 1680, "THE JOSH¹ ARCHIVE • JOSHSHOOT.SOL", font_footer, fill=deep_theme)

    # Prepare base framed artwork at 1.0x scale (target art size = 880x880 box)
    cw, ch = art_img.size
    scale_1x = 860.0 / max(cw, ch)
    w_1x = int(cw * scale_1x)
    h_1x = int(ch * scale_1x)
    art_1x = art_img.resize((w_1x, h_1x), Image.Resampling.LANCZOS)
    framed_1x = add_museum_mat_and_gallery_shadow(art_1x, radius=20)

    # VideoWriter setup
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 30
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_frames = 150 # 5 seconds total
    zoom_frames = 120  # 4 seconds zooming out from 1.15x to 1.00x
    hold_frames = 30   # 1 second holding full frame at 1.00x

    fw, fh = framed_1x.size
    center_y = 740 # vertical center position on 1080x1920 canvas

    for i in range(total_frames):
        if i < zoom_frames:
            # Smooth cosine easing for luxury cinematic feel
            progress = i / float(zoom_frames)
            ease = (1.0 - np.cos(progress * np.pi)) / 2.0
            zoom = 1.15 - 0.15 * ease
        else:
            zoom = 1.00

        if abs(zoom - 1.00) < 0.001:
            frame_img = bg.copy()
            frame_img.paste(framed_1x, ((width - fw) // 2, center_y - fh // 2), framed_1x)
        else:
            cur_w = int(fw * zoom)
            cur_h = int(fh * zoom)
            framed_scaled = framed_1x.resize((cur_w, cur_h), Image.Resampling.BILINEAR)
            frame_img = bg.copy()
            frame_img.paste(framed_scaled, ((width - cur_w) // 2, center_y - cur_h // 2), framed_scaled)

        bgr = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGB2BGR)
        out.write(bgr)

    out.release()
    print(f"[SUCCESS] ✅ Created 1080x1920 Zoom-Out Reel: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_tiktok_zoom_reel(197, "JOSH1-197: Maritime Museum, Rotterdam", "https://cdn.inprnt.com/thumbs/0c/2b/0c2b504067590379c2c6e9866a469358@2x.jpg", "output/JOSH1_197_ZoomOut_Reel.mp4")
