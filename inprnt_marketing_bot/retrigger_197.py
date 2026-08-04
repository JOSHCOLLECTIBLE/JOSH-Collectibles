# ==============================================================================
# 1-CLICK INSTAGRAM RE-TRIGGER SCRIPT FOR #197 (100% CACHE-BUSTED JPEG FORMAT)
# ==============================================================================
# Verifies that both Slide 1 (Black Void Portrait) and Slide 2 (Museum Monograph)
# are live on GitHub CDN before calling Make.com.
# Guarantees ZERO duplicate carousel slides and ZERO wasted Make.com credits!

import sys
import time
import requests

webhook_url = "https://hook.eu1.make.com/30d9gkhnrtlmspxqh1bl3ekxyxndd93i"

# Test if GitHub raw URLs are 200 OK
ts = int(time.time())

# Check both standard daily filenames and specific #197 filenames
gh_u1_daily = f"https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/post1_daily_instagram.jpg?v={ts}"
gh_u2_daily = f"https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/post2_daily_instagram.jpg?v={ts}"

gh_u1_specific = f"https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/JOSH1_197_Post1_Square.jpg?v={ts}"
gh_u2_specific = f"https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/JOSH1_197_Post2_Monograph.jpg?v={ts}"

print("🔍 Checking if GitHub 1080x1350 JPEG carousel images are live (200 OK)...")

final_u1 = None
final_u2 = None

for u1_candidate, u2_candidate in [(gh_u1_daily, gh_u2_daily), (gh_u1_specific, gh_u2_specific)]:
    try:
        r1 = requests.head(u1_candidate, timeout=5)
        r2 = requests.head(u2_candidate, timeout=5)
        if r1.status_code == 200 and r2.status_code == 200:
            final_u1 = u1_candidate
            final_u2 = u2_candidate
            break
    except Exception:
        pass

if not final_u1 or not final_u2:
    print("❌ ABORTING: GitHub CDN images are not live yet (404).")
    print("   To protect your Make.com free credits and NEVER upload Post 1 twice on the carousel,")
    print("   please push the images to GitHub first by running:")
    print("   ------------------------------------------------------------")
    print("   cd ~/JOSH-Collectibles && bash inprnt_marketing_bot/deploy.sh")
    print("   ------------------------------------------------------------")
    print("   After pushing, re-run this script to post the 2-Slide Carousel live to Instagram!")
    sys.exit(1)

print("✅ SUCCESS: Both Slide 1 (Black Void) and Slide 2 (Museum Monograph) are 100% LIVE and 200 OK!")
print(f"   Slide 1: {final_u1}")
print(f"   Slide 2: {final_u2}")

payload = {
    "image_url": final_u1,
    "image_url_2": final_u2,
    "caption": (
        "JOSH1 197 • Maritime Museum, Rotterdam\n\n"
        "  Rotterdam Maritime Museum\n"
        "  Brutalist mass against maritime history\n"
        "  An archival record of institutional form\n\n"
        "THE JOSH¹ ARCHIVE\n"
        "Limited Edition Phygital Art Piece\n"
        "Edition: 100% Cotton Rag Archival Fine Art Print (300gsm)\n"
        "Provenance: Solana Blockchain verified (JOSHSHOOT.SOL) to Physical exhibition print via INPRNT\n\n"
        "Collect the archive via link in bio\n"
        "📸 iPhone 12 / Archival Capture\n"
        "📍 Rotterdam (RTM) 🇳🇱\n"
        "💎 Rarity: Common\n"
        "⚡ On Chain: JOSHSHOOT.SOL\n\n"
        ".\n.\n.\n"
        "#WallArtDecor #SolanaNFT #JOSHSHOOTPRINTS #INPRNT"
    ),
    "title": "JOSH1 197 • Maritime Museum, Rotterdam"
}

print(f"🚀 Sending 2-Slide Carousel (#197 .jpg format) to Make.com Webhook...")
r = requests.post(webhook_url, json=payload, timeout=15)
if r.status_code == 200:
    print(f"✅ SUCCESS! Sent #197 2-Slide Carousel to Make.com! Check your Instagram app now!")
else:
    print(f"❌ Webhook responded with status: {r.status_code} - {r.text}")
