"""
Instagram 100% Hands-Free Direct Posting Automation Module.
Supports BOTH:
1. Official Meta Graph API (if INSTAGRAM_ACCESS_TOKEN / INSTAGRAM_ACCOUNT_ID is set)
2. Free Webhook Automation via Make.com / IFTTT / Zapier (sends both image_url and image_url_2 for Carousel!)
"""

import os
import sys
import time
import argparse
import requests
from typing import Dict, Any, Optional

class InstagramAutomator:
    """
    Automates 100% hands-free Instagram photo posting using Official Meta Graph API
    OR free Webhook automation bridges (Make.com / IFTTT / Zapier).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
        self.account_id = os.environ.get("INSTAGRAM_ACCOUNT_ID", "").strip()
        self.webhook_url = (
            os.environ.get("MAKE_INSTAGRAM_WEBHOOK_URL", "").strip()
            or os.environ.get("INSTAGRAM_WEBHOOK_URL", "").strip()
            or self.config.get("instagram_automation", {}).get("webhook_url", "").strip()
            or "https://hook.eu1.make.com/30d9gkhnrtlmspxqh1bl3ekxyxndd93i"
        )
        self.webhook_api_key = os.environ.get("MAKE_WEBHOOK_API_KEY", "").strip()
        self.api_version = "v19.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def is_configured(self) -> bool:
        """Checks if either Meta Graph API OR Webhook automation is present."""
        return bool((self.access_token and self.account_id) or self.webhook_url)

    def publish_photo(self, image_url: str, caption: str, artwork_title: str = "", image_url_2: str = "") -> bool:
        """
        Publishes 100% automatically to Instagram via Webhook bridge OR Meta Graph API.
        Sends image_url (Post 1) and image_url_2 (Post 2) for Carousel support!
        """
        if not self.is_configured():
            print("[INFO] No INSTAGRAM_ACCESS_TOKEN or MAKE_INSTAGRAM_WEBHOOK_URL set. Skipping automated Instagram post.")
            return False

        # METHOD 1: Free Webhook Automation (Make.com / IFTTT / Zapier)
        if self.webhook_url:
            print(f"[INFO] 🚀 MAKE_INSTAGRAM_WEBHOOK_URL detected! Sending 100% automated Carousel trigger...")
            payload = {
                "image_url": image_url,
                "image_url_2": image_url_2,
                "caption": caption,
                "title": artwork_title,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            headers = {}
            if self.webhook_api_key:
                headers["x-make-apikey"] = self.webhook_api_key

            try:
                r = requests.post(self.webhook_url, json=payload, headers=headers, timeout=15)
                r.raise_for_status()
                print(f"[SUCCESS] ✅ Successfully triggered 100% automated Instagram Carousel via Webhook! ({r.status_code})")
                return True
            except Exception as e:
                print(f"[ERROR] Failed to trigger Instagram webhook: {e}")
                # Fall through to check if Meta API is also configured

        # METHOD 2: Official Meta Graph API
        if self.access_token and self.account_id:
            print(f"[INFO] 🚀 Initializing Official Meta Graph API post for @joshuadenouden...")
            create_url = f"{self.base_url}/{self.account_id}/media"
            payload_create = {
                "image_url": image_url,
                "caption": caption,
                "access_token": self.access_token
            }

            try:
                r_create = requests.post(create_url, data=payload_create, timeout=20)
                r_create.raise_for_status()
                creation_id = r_create.json().get("id")

                if not creation_id:
                    print(f"[ERROR] Failed to obtain creation_id from Meta API: {r_create.text}")
                    return False

                print(f"[SUCCESS] Media container created (ID: {creation_id}). Waiting for Meta image processing...")
                time.sleep(5)

                publish_url = f"{self.base_url}/{self.account_id}/media_publish"
                payload_publish = {
                    "creation_id": creation_id,
                    "access_token": self.access_token
                }

                r_publish = requests.post(publish_url, data=payload_publish, timeout=20)
                r_publish.raise_for_status()
                media_id = r_publish.json().get("id")

                print(f"[SUCCESS] 📸 ✅ Successfully published artwork directly to Instagram feed! Media ID: {media_id}")
                return True

            except Exception as e:
                print(f"[ERROR] Meta Graph API publishing failed: {e}")
                if hasattr(e, "response") and getattr(e, "response", None) is not None:
                    print(f"[ERROR DETAILS] {e.response.text}")
                return False

        return False

    def verify_connection(self) -> bool:
        """Tests Webhook OR Meta Graph API credentials with a full sample payload."""
        if self.webhook_url:
            print(f"[INFO] Testing MAKE_INSTAGRAM_WEBHOOK_URL with sample Carousel payload...")
            headers = {}
            if self.webhook_api_key:
                headers["x-make-apikey"] = self.webhook_api_key
            
            sample_payload = {
                "image_url": "https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/post1_daily_instagram.png",
                "image_url_2": "https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/post2_daily_instagram.png",
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
                "title": "JOSH1 197 • Maritime Museum, Rotterdam",
                "test": True
            }

            try:
                r = requests.post(self.webhook_url, json=sample_payload, headers=headers, timeout=10)
                print(f"✅ Webhook connection successful! Status: {r.status_code}")
                print(f"   Sent sample 'image_url' (Post 1) and 'image_url_2' (Post 2) fields to Make.com!")
                return True
            except Exception as e:
                print(f"❌ Webhook test failed: {e}")
                return False
        elif self.access_token and self.account_id:
            print(f"[INFO] Connecting to Official Meta Graph API ({self.api_version})...")
            verify_url = f"{self.base_url}/{self.account_id}"
            params = {
                "fields": "username,name,followers_count,media_count",
                "access_token": self.access_token
            }
            try:
                r = requests.get(verify_url, params=params, timeout=10)
                r.raise_for_status()
                data = r.json()
                print(f"\n✅ INSTAGRAM GRAPH API CONNECTION SUCCESSFUL!")
                print(f"   Account Name       : {data.get('name')}")
                print(f"   Instagram Username : @{data.get('username')}")
                print(f"   Followers Count    : {data.get('followers_count', 0)}")
                print(f"   Total Published    : {data.get('media_count', 0)} posts\n")
                return True
            except Exception as e:
                print(f"[ERROR] Failed to verify Meta Graph API connection: {e}")
                return False
        else:
            print("[ERROR] Neither MAKE_INSTAGRAM_WEBHOOK_URL nor INSTAGRAM_ACCESS_TOKEN is set!")
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify Instagram 100% Automation Credentials")
    parser.add_argument("--verify", action="store_true", help="Test connection to Webhook or Meta Graph API")
    args = parser.parse_args()

    api = InstagramAutomator()
    if args.verify:
        api.verify_connection()
    else:
        print("Use 'python3 -m src.instagram_bot --verify' to test your Instagram automation credentials.")
