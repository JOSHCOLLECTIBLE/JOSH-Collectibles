"""
Instagram Direct Posting Automation Module (Official Meta Graph API).
Safely publishes high-resolution INPRNT artwork images and technical Rarity/Metadata
captions directly to @joshuadenouden via GitHub Actions without triggering spam bans.
"""

import os
import time
import requests
from typing import Dict, Any, Optional

class InstagramGraphAPI:
    """
    Automates Instagram photo posting using the Official Meta Graph API v19.0+.
    Requires INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_ACCOUNT_ID environment variables.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ig_config = config.get("instagram_automation", {})
        self.access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
        self.account_id = os.environ.get("INSTAGRAM_ACCOUNT_ID", "").strip()
        self.api_version = "v19.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def is_configured(self) -> bool:
        """Checks if official Instagram Graph API credentials are present."""
        return bool(self.access_token and self.account_id)

    def publish_photo(self, image_url: str, caption: str) -> Optional[str]:
        """
        Uploads an image container to Instagram and publishes it to the feed.
        Returns the published Instagram Media ID if successful.
        """
        if not self.is_configured():
            print("[INFO] INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_ACCOUNT_ID not set. Skipping automated Instagram post.")
            return None

        print(f"[INFO] Initializing Instagram Graph API post for container creation...")
        create_url = f"{self.base_url}/{self.account_id}/media"
        payload_create = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }

        try:
            # 1. Create Media Container
            r_create = requests.post(create_url, data=payload_create, timeout=20)
            r_create.raise_for_status()
            create_data = r_create.json()
            creation_id = create_data.get("id")

            if not creation_id:
                print(f"[ERROR] Failed to obtain creation_id from Meta API: {create_data}")
                return None

            print(f"[SUCCESS] Media container created (ID: {creation_id}). Waiting for Meta image processing...")
            time.sleep(5)  # Allow Meta servers 5 seconds to download the image from INPRNT CDN

            # 2. Publish Media Container
            publish_url = f"{self.base_url}/{self.account_id}/media_publish"
            payload_publish = {
                "creation_id": creation_id,
                "access_token": self.access_token
            }

            r_publish = requests.post(publish_url, data=payload_publish, timeout=20)
            r_publish.raise_for_status()
            publish_data = r_publish.json()
            media_id = publish_data.get("id")

            print(f"[SUCCESS] 📸 Successfully published artwork directly to Instagram feed! Media ID: {media_id}")
            return media_id

        except Exception as e:
            print(f"[ERROR] Instagram Graph API publishing failed: {e}")
            if hasattr(e, "response") and getattr(e, "response", None) is not None:
                print(f"[ERROR DETAILS] {e.response.text}")
            return None
