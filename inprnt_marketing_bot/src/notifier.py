"""
Notification and Social API Posting Module.
Supports Discord Webhooks, Telegram Bot alerts, Pinterest CSV export,
and optional direct posting to Twitter/X and Bluesky APIs.
"""

import os
import csv
import json
import requests
from typing import Dict, Any, List, Optional

class Notifier:
    """Handles sending notifications and exporting queues."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.notif_config = config.get("notifications", {})
        self.apis_config = config.get("social_apis", {})

    def notify_discord(self, campaign: Dict[str, Any]) -> bool:
        """
        Sends a rich Discord embed via Webhook with the daily artwork, pricing,
        and copy-paste marketing text for each platform.
        """
        webhook_url_env = self.notif_config.get("discord_webhook_env", "DISCORD_WEBHOOK_URL")
        webhook_url = os.environ.get(webhook_url_env, "").strip()
        if not webhook_url:
            print("[INFO] No DISCORD_WEBHOOK_URL set in environment. Skipping Discord alert.")
            return False

        title = campaign.get("artwork_title", "Fine Art Print")
        url = campaign.get("artwork_url", "")
        img_url = campaign.get("artwork_image", "")
        price = campaign.get("price", "$12.00")

        short_post = campaign.get("twitter_bluesky", {}).get("short_post", "")
        pin_title = campaign.get("pinterest", {}).get("title", "")

        payload = {
            "username": "INPRNT Art Marketing Bot",
            "avatar_url": "https://cdn.inprnt.com/thumbs/26/1d/261d1f5e3ef1d545ae2c96efff584c3c.jpg",
            "embeds": [
                {
                    "title": f"🎨 Today's Art Promotion: {title}",
                    "url": url,
                    "color": 2450411, # Blue (#2563eb)
                    "description": f"**Current Price:** {price} (20% OFF)\nHere is your ready-to-post copy for today's promotion!",
                    "image": {"url": img_url} if img_url else {},
                    "fields": [
                        {
                            "name": "📌 Pinterest Pin Title",
                            "value": f"```{pin_title}```",
                            "inline": False
                        },
                        {
                            "name": "🐦 Twitter / X / Bluesky Post",
                            "value": f"```{short_post}```",
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": "100% Free Automated GitHub Actions Art Marketing Bot"
                    }
                }
            ]
        }

        try:
            resp = requests.post(webhook_url, json=payload, timeout=10)
            resp.raise_for_status()
            print("[SUCCESS] Sent daily promotion alert to Discord webhook!")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send Discord webhook alert: {e}")
            return False

    def notify_telegram(self, campaign: Dict[str, Any]) -> bool:
        """Sends a Telegram Bot message with photo and copy-paste caption."""
        bot_token_env = self.notif_config.get("telegram_bot_token_env", "TELEGRAM_BOT_TOKEN")
        chat_id_env = self.notif_config.get("telegram_chat_id_env", "TELEGRAM_CHAT_ID")

        bot_token = os.environ.get(bot_token_env, "").strip()
        chat_id = os.environ.get(chat_id_env, "").strip()

        if not bot_token or not chat_id:
            print("[INFO] Telegram credentials not set. Skipping Telegram alert.")
            return False

        title = campaign.get("artwork_title", "Fine Art Print")
        url = campaign.get("artwork_url", "")
        img_url = campaign.get("artwork_image", "")
        short_post = campaign.get("twitter_bluesky", {}).get("short_post", "")

        api_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        caption = f"🎨 **Today's Art Promotion: {title}**\n\n{short_post}"

        payload = {
            "chat_id": chat_id,
            "photo": img_url,
            "caption": caption[:1020], # Telegram limit
            "parse_mode": "Markdown"
        }

        try:
            resp = requests.post(api_url, data=payload, timeout=10)
            resp.raise_for_status()
            print("[SUCCESS] Sent daily promotion alert to Telegram!")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send Telegram alert: {e}")
            return False

    def export_pinterest_csv_queue(self, campaigns: List[Dict[str, Any]], output_path: str = "output/pinterest_queue.csv") -> None:
        """
        Exports a bulk Pinterest CSV file ready to be uploaded to Pinterest,
        Later, Buffer, or Metricool.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        headers = ["Title", "Media URL", "Pinterest Board", "Thumbnail", "Description", "Link", "Publish Date", "Keywords"]

        with open(output_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for camp in campaigns:
                pin = camp.get("pinterest", {})
                writer.writerow([
                    pin.get("title", ""),
                    camp.get("artwork_image", ""),
                    pin.get("board", "Fine Art Prints"),
                    camp.get("artwork_image", ""),
                    pin.get("description", ""),
                    pin.get("link", camp.get("artwork_url", "")),
                    "", # Leave date blank for immediate / default queue
                    pin.get("hashtags", "")
                ])
        print(f"[SUCCESS] Exported Pinterest Bulk Queue CSV: {output_path}")

    def save_campaign_artifacts(self, campaign: Dict[str, Any], output_dir: str = "output") -> None:
        """Saves daily campaign files in JSON and Markdown format."""
        os.makedirs(output_dir, exist_ok=True)
        date_str = campaign.get("artwork_id", "campaign")

        # Save JSON
        json_path = os.path.join(output_dir, "latest_campaign.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(campaign, f, indent=2, ensure_ascii=False)

        # Save Markdown
        md_path = os.path.join(output_dir, "latest_campaign.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# 🎨 Marketing Campaign: {campaign.get('artwork_title')}\n\n")
            f.write(f"**Artwork URL:** [{campaign.get('artwork_url')}]({campaign.get('artwork_url')})\n")
            f.write(f"**Current Price:** {campaign.get('price')} ({campaign.get('discount_note')})\n\n")
            f.write(f"![{campaign.get('artwork_title')}]({campaign.get('artwork_image')})\n\n")
            
            f.write("## 📌 Pinterest Pin Copy\n")
            f.write(f"- **Title:** `{campaign.get('pinterest', {}).get('title')}`\n")
            f.write(f"- **Board:** `{campaign.get('pinterest', {}).get('board')}`\n")
            f.write(f"- **Description:**\n```text\n{campaign.get('pinterest', {}).get('description')}\n```\n\n")

            f.write("## 🐦 Twitter / X & Bluesky Post\n")
            f.write(f"```text\n{campaign.get('twitter_bluesky', {}).get('short_post')}\n```\n\n")

            f.write("## 📸 Instagram / TikTok Caption\n")
            f.write(f"```text\n{campaign.get('instagram', {}).get('caption')}\n```\n\n")

            f.write("## 🔴 Reddit Artist Showcase\n")
            f.write(f"- **Suggested Title:** `{campaign.get('reddit', {}).get('title')}`\n")
            f.write(f"- **Target Subreddits:** {', '.join(campaign.get('reddit', {}).get('target_subreddits', []))}\n")
            f.write(f"- **Post Body:**\n```markdown\n{campaign.get('reddit', {}).get('body')}\n```\n")
        
        print(f"[SUCCESS] Saved daily campaign artifacts to {output_dir}/")
