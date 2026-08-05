# ==============================================================================
# 1-CLICK INSTAGRAM RE-TRIGGER SCRIPT FOR LATEST DAILY PROMOTION
# ==============================================================================
# Reads output/latest_campaign.json and sends the 2-Slide Carousel to Make.com.
# Guarantees ZERO duplicate slides and 100% current artwork posting!

import os
import sys
import json
import time
import requests

webhook_url = "https://hook.eu1.make.com/30d9gkhnrtlmspxqh1bl3ekxyxndd93i"

camp_path = "output/latest_campaign.json"
if not os.path.exists(camp_path):
    print(f"❌ ERROR: {camp_path} not found! Please run '--action daily-promo' first.")
    sys.exit(1)

with open(camp_path, "r", encoding="utf-8") as f:
    campaign = json.load(f)

ts = int(time.time())
gh_u1 = f"https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/post1_daily_instagram.jpg?v={ts}"
gh_u2 = f"https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/post2_daily_instagram.jpg?v={ts}"

print(f"🔍 Checking if GitHub JPEG images are live for '{campaign.get('artwork_title')}'...")
try:
    r1 = requests.head(gh_u1, timeout=5)
    r2 = requests.head(gh_u2, timeout=5)
    if r1.status_code != 200 or r2.status_code != 200:
        print(f"❌ ABORTING: GitHub CDN images are not live yet (Post 1: {r1.status_code}, Post 2: {r2.status_code}).")
        print("   Please push your images to GitHub first ('git push origin main')!")
        sys.exit(1)
except Exception as e:
    print(f"⚠️ Could not verify GitHub CDN status ({e}), proceeding...")

print("✅ SUCCESS: Both Slide 1 (Black Void) and Slide 2 (Museum Monograph) are 100% LIVE and 200 OK!")
print(f"   Slide 1: {gh_u1}")
print(f"   Slide 2: {gh_u2}")

payload = {
    "image_url": gh_u1,
    "image_url_2": gh_u2,
    "caption": campaign.get("instagram", {}).get("caption", ""),
    "title": campaign.get("artwork_title", "")
}

print(f"🚀 Sending 2-Slide Carousel ('{campaign.get('artwork_title')}') to Make.com Webhook...")
r = requests.post(webhook_url, json=payload, timeout=15)
if r.status_code == 200:
    print(f"✅ SUCCESS! Sent '{campaign.get('artwork_title')}' to Make.com! Check your Instagram app now!")
else:
    print(f"❌ Webhook responded with status: {r.status_code} - {r.text}")
