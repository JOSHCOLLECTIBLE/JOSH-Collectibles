"""
Main CLI entrypoint for INPRNT Marketing Bot.
Produces JOSH¹ Archive technical metadata campaigns, visual HTML dashboards,
and zero-cost GitHub Actions cloud automation with 100% Guaranteed Cache-Busted JPEG URLs!
"""

import os
import sys
import json
import yaml
import time
import argparse
import re
from typing import Dict, Any, List
from datetime import datetime

from src.scraper import InprntScraper
from src.content_generator import ContentGenerator
from src.storage import HistoryManager
from src.notifier import Notifier
from src.instagram_bot import InstagramAutomator
from generate_wall_cards import generate_post1_dark_mode_portrait, generate_post2_museum_monograph

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Loads YAML configuration file."""
    if not os.path.exists(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def generate_html_report(campaigns: List[Dict[str, Any]], title: str, output_path: str, config: Dict[str, Any]) -> None:
    """
    Generates a standalone, JOSH¹ Archive luxury editorial styled HTML dashboard
    with inline CSS, on-chain identity links (JOSHSHOOT.SOL), and copy buttons.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    artist_name = config.get("artist", {}).get("name", "JOSH SHOOT")
    sol_domain = config.get("artist", {}).get("solana_domain", "JOSHSHOOT.SOL")
    domain = config.get("artist", {}).get("domain", "joshuadenouden21-hiuos.wordpress.com")
    drip_url = config.get("artist", {}).get("drip_url", "https://drip.haus/josh")
    twitter_handle = config.get("artist", {}).get("twitter_handle", "@Joshtakesphoto")
    shop_url = config.get("artist", {}).get("gallery_url", "https://www.inprnt.com/gallery/joshuadenouden/")

    cards_html = []
    for i, camp in enumerate(campaigns):
        art_title = camp.get("artwork_title", "Print")
        art_img = camp.get("artwork_image", "")
        art_url = camp.get("artwork_url", "")
        price = camp.get("price", "$12.00")
        rarity = camp.get("rarity", "Common")
        location = camp.get("location", "Rotterdam (RTM) 🇳🇱")
        device = camp.get("device", "iPhone 12")

        pin = camp.get("pinterest", {})
        twitter = camp.get("twitter_bluesky", {})
        ig = camp.get("instagram", {})
        gh_journal = camp.get("github_journal", {})

        card = f"""
        <div class="card" id="artwork-{i}">
          <div class="card-header">
            <img src="{art_img}" alt="{art_title}" class="artwork-thumb" />
            <div class="header-info">
              <div class="meta-tag">JOSH¹ ARCHIVE // 💎 RARITY: {rarity.upper()} &bull; 📍 {location}</div>
              <h2>{art_title}</h2>
              <div class="badge-row">
                <span class="badge price-badge">{price} &bull; 20% OFF Phygital Release</span>
                <span class="badge device-badge">📸 {device}</span>
                <a href="{art_url}" target="_blank" class="badge shop-badge">Acquire on INPRNT &rarr;</a>
              </div>
            </div>
          </div>

          <div class="channel-tabs">
            <div class="tab-content">
              <div class="tab-header">
                <h3>📌 Pinterest Editorial Pin (Evergreen Organic Traffic)</h3>
                <span class="platform-note">Optimized for interior decor & architectural collectors</span>
              </div>
              <p><strong>Title:</strong> {pin.get('title')}</p>
              <p><strong>Curated Board:</strong> {pin.get('board')}</p>
              <div class="code-box">
                <pre id="pin-desc-{i}">{pin.get('description')}</pre>
                <button class="copy-btn" onclick="copyText('pin-desc-{i}')">Copy Description</button>
              </div>
            </div>

            <div class="tab-content">
              <div class="tab-header">
                <h3>🐦 Twitter / X & Bluesky (Solana & Web3 Collector Community)</h3>
                <span class="platform-note">Featuring {sol_domain} &bull; {twitter_handle}</span>
              </div>
              <div class="code-box">
                <pre id="tw-post-{i}">{twitter.get('short_post')}</pre>
                <button class="copy-btn" onclick="copyText('tw-post-{i}')">Copy Web3 Post</button>
              </div>
            </div>

            <div class="tab-content">
              <div class="tab-header">
                <h3>📸 Instagram / Threads (Sequential Archive Automation)</h3>
                <span class="platform-note">100% AI-Proof Monograph Caption</span>
              </div>
              <p class="carousel-note"><strong>{ig.get('carousel_strategy', '')}</strong></p>
              <div class="code-box">
                <pre id="ig-post-{i}">{ig.get('caption')}</pre>
                <button class="copy-btn" onclick="copyText('ig-post-{i}')">Copy Caption & Hashtags</button>
              </div>
            </div>

            <div class="tab-content">
              <div class="tab-header">
                <h3>📂 GitHub Archive Journal (README & Releases Feature)</h3>
                <span class="platform-note">Turn your GitHub repo into an active curatorial catalog!</span>
              </div>
              <p><strong>Release Title:</strong> <code>{gh_journal.get('title')}</code></p>
              <div class="code-box">
                <pre id="gh-post-{i}">{gh_journal.get('markdown')}</pre>
                <button class="copy-btn" onclick="copyText('gh-post-{i}')">Copy GitHub Markdown</button>
              </div>
            </div>
          </div>
        </div>
        """
        cards_html.append(card)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — {artist_name} ({sol_domain})</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --muted: #475569;
      --primary: #0f172a;
      --accent: #2563eb;
      --border: #e2e8f0;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 40px 20px;
      line-height: 1.6;
    }}
    .container {{
      max-width: 1040px;
      margin: 0 auto;
    }}
    header {{
      text-align: center;
      margin-bottom: 50px;
      border-bottom: 2px solid #0f172a;
      padding-bottom: 30px;
    }}
    .editorial-tag {{
      font-size: 11px;
      letter-spacing: 3px;
      text-transform: uppercase;
      font-weight: 800;
      color: #64748b;
      margin-bottom: 8px;
    }}
    h1 {{
      margin: 0 0 14px 0;
      font-size: 34px;
      font-weight: 900;
      letter-spacing: -1px;
      color: #0f172a;
      text-transform: uppercase;
    }}
    .subtitle {{
      color: var(--muted);
      font-size: 16px;
      margin: 0 0 20px 0;
    }}
    .nav-links {{
      display: flex;
      justify-content: center;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .nav-pill {{
      display: inline-block;
      padding: 6px 14px;
      background: #f1f5f9;
      color: #0f172a;
      text-decoration: none;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
      border: 1px solid var(--border);
    }}
    .nav-pill:hover {{
      background: #e2e8f0;
    }}
    .nav-pill.primary {{
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 4px;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
      margin-bottom: 36px;
      overflow: hidden;
    }}
    .card-header {{
      display: flex;
      align-items: center;
      padding: 28px;
      border-bottom: 1px solid var(--border);
      background: #fdfdfe;
      gap: 24px;
    }}
    .artwork-thumb {{
      width: 140px;
      height: 140px;
      object-fit: cover;
      border-radius: 2px;
      border: 1px solid var(--border);
      flex-shrink: 0;
    }}
    .meta-tag {{
      font-size: 11px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      font-weight: 700;
      color: #64748b;
      margin-bottom: 6px;
    }}
    .header-info h2 {{
      margin: 0 0 14px 0;
      font-size: 24px;
      font-weight: 800;
      color: #0f172a;
    }}
    .badge-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .badge {{
      display: inline-block;
      padding: 8px 14px;
      border-radius: 2px;
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .price-badge {{
      background: #f1f5f9;
      color: #0f172a;
      border: 1px solid #cbd5e1;
    }}
    .device-badge {{
      background: #f8fafc;
      color: #475569;
      border: 1px solid #cbd5e1;
    }}
    .shop-badge {{
      background: var(--primary);
      color: #ffffff;
    }}
    .channel-tabs {{
      padding: 28px;
      display: grid;
      grid-template-columns: 1fr;
      gap: 28px;
    }}
    .tab-content {{
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 20px;
    }}
    .tab-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .tab-header h3 {{
      margin: 0;
      font-size: 15px;
      font-weight: 800;
      color: #0f172a;
    }}
    .platform-note {{
      font-size: 12px;
      color: #64748b;
      font-weight: 600;
    }}
    .carousel-note {{
      font-size: 13px;
      color: #0f172a;
      background: #f1f5f9;
      padding: 10px 14px;
      border-left: 3px solid #0f172a;
      margin: 0 0 12px 0;
      white-space: pre-line;
    }}
    .code-box {{
      position: relative;
      margin-top: 10px;
    }}
    pre {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 2px;
      padding: 16px;
      white-space: pre-wrap;
      word-wrap: break-word;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 13px;
      color: #1e293b;
      margin: 0;
      max-height: 280px;
      overflow-y: auto;
      line-height: 1.6;
    }}
    .copy-btn {{
      position: absolute;
      top: 10px;
      right: 10px;
      background: #0f172a;
      color: #ffffff;
      border: none;
      padding: 7px 14px;
      border-radius: 2px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      cursor: pointer;
      transition: background 0.2s;
    }}
    .copy-btn:hover {{
      background: #334155;
    }}
    footer {{
      text-align: center;
      margin-top: 60px;
      padding-top: 30px;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 13px;
    }}
  </style>
  <script>
    function copyText(elementId) {{
      const text = document.getElementById(elementId).innerText;
      navigator.clipboard.writeText(text).then(() => {{
        alert('Copied editorial copy to clipboard!');
      }}).catch(err => {{
        console.error('Could not copy text: ', err);
      }});
    }}
  </script>
</head>
<body>
  <div class="container">
    <header>
      <div class="editorial-tag">JOSH¹ ARCHIVE // Phygital Curation</div>
      <h1>{title}</h1>
      <p class="subtitle">
        Curated by <strong>{artist_name}</strong> (<code>{sol_domain}</code> &bull; <code>{domain}</code>) &bull; 
        Tactile Archival Print Collection on INPRNT
      </p>
      <div class="nav-links">
        <a href="{shop_url}" target="_blank" class="nav-pill primary">INPRNT Gallery</a>
        <a href="https://{domain}" target="_blank" class="nav-pill">{domain}</a>
        <a href="https://solana.com/" target="_blank" class="nav-pill">{sol_domain} (On-Chain)</a>
        <a href="{drip_url}" target="_blank" class="nav-pill">DRiP Archive</a>
        <a href="https://x.com/{twitter_handle.lstrip('@')}" target="_blank" class="nav-pill">Twitter / X ({twitter_handle})</a>
        <a href="https://github.com/JOSHCOLLECTIBLE/JOSH-Collectibles" target="_blank" class="nav-pill">GitHub (JOSHCOLLECTIBLE)</a>
      </div>
    </header>

    <main>
      {"".join(cards_html)}
    </main>

    <footer>
      <p>
        <strong>THE JOSH¹ ARCHIVE &bull; {sol_domain} &bull; {domain}</strong><br/>
        Phygital Art Copywriting & Curation Engine &bull; 100% Free Automated GitHub Actions Integration
      </p>
    </footer>
  </div>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[SUCCESS] Generated JOSH¹ Archive Editorial Visual Report: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="INPRNT Multi-Channel Art Marketing Bot (JOSH¹ Archive Edition)")
    parser.add_argument(
        "--action",
        choices=["daily-promo", "trigger-instagram", "export-all", "test-webhook"],
        default="daily-promo",
        help="Action to execute: daily-promo (generate files), trigger-instagram (call Make.com AFTER git push), or export-all"
    )
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--no-post", action="store_true", help="Generate and save files without triggering Instagram post")
    args = parser.parse_args()

    config = load_config(args.config)
    artist_name = config.get("artist", {}).get("name", "JOSH SHOOT")
    sol_domain = config.get("artist", {}).get("solana_domain", "JOSHSHOOT.SOL")
    gallery_url = config.get("artist", {}).get("gallery_url")
    profile_url = config.get("artist", {}).get("profile_url")

    scraper = InprntScraper(gallery_url=gallery_url, profile_url=profile_url)
    gen = ContentGenerator(config)
    notifier = Notifier(config)
    ig_automator = InstagramAutomator(config)
    history_mgr = HistoryManager(
        config.get("output", {}).get("history_file", "output/history.json"),
        config=config
    )

    if args.action == "test-webhook":
        print("[INFO] Testing webhook alerts...")
        dummy_campaign = {
            "artwork_title": "JOSH1 222 • The Dutch Blue Man",
            "artwork_url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-222-the-dutch-blue-man/",
            "artwork_image": "https://cdn.inprnt.com/thumbs/26/1d/261d1f5e3ef1d545ae2c96efff584c3c@2x.jpg",
            "price": "$12.00",
            "twitter_bluesky": {
                "short_post": f"「 JOSH1 222 • The Dutch Blue Man 」\n\n  Rotterdam Maritime Museum\n  Brutalist mass against maritime history\n  An archival record of institutional form\n\nTHE JOSH¹ ARCHIVE\n🔗 https://www.inprnt.com/gallery/joshuadenouden/josh1-222-the-dutch-blue-man/"
            },
            "pinterest": {
                "title": f"JOSH1 222 • The Dutch Blue Man | JOSH¹ Archive Brutalist Photography"
            }
        }
        notifier.notify_discord(dummy_campaign)
        notifier.notify_telegram(dummy_campaign)
        return

    print(f"============================================================")
    print(f"🏛️  JOSH¹ ARCHIVE PHYGITAL MARKETING ENGINE - {artist_name} ({sol_domain})")
    print(f"   Target Shop: {gallery_url}")
    print(f"   Action: {args.action} | No-Post: {args.no_post}")
    print(f"============================================================")

    use_cache_flag = (args.action != "export-all")
    prints = scraper.scrape_gallery_prints(use_cache=use_cache_flag)
    print(f"[INFO] Loaded {len(prints)} artwork prints from gallery/cache.")
    if not prints:
        print("[ERROR] No prints found! Please check shop URL or connectivity.")
        sys.exit(1)

    if args.action == "trigger-instagram":
        camp_path = "output/latest_campaign.json"
        if not os.path.exists(camp_path):
            print(f"[ERROR] {camp_path} not found! Run --action daily-promo first.")
            sys.exit(1)
        with open(camp_path, "r", encoding="utf-8") as f:
            campaign = json.load(f)
        
        # Add timestamp parameter (?v=...) to force GitHub CDN to bypass cache 100%!
        ts = int(time.time())
        github_cdn_post1_url = f"https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/post1_daily_instagram.jpg?v={ts}"
        github_cdn_post2_url = f"https://raw.githubusercontent.com/JOSHCOLLECTIBLE/JOSH-Collectibles/main/inprnt_marketing_bot/output/post2_daily_instagram.jpg?v={ts}"

        print("[INFO] 🔍 Verifying that both Slide 1 and Slide 2 are 100% LIVE on GitHub CDN...")
        try:
            import requests
            max_retries = 10
            for attempt in range(1, max_retries + 1):
                r1 = requests.head(github_cdn_post1_url, timeout=5)
                r2 = requests.head(github_cdn_post2_url, timeout=5)
                if r1.status_code == 200 and r2.status_code == 200:
                    print(f"[SUCCESS] ✅ Both carousel slides are 200 OK on GitHub CDN (verified on attempt {attempt})!")
                    break
                else:
                    if attempt < max_retries:
                        print(f"[WAIT] ⏳ GitHub CDN not ready yet (Post 1: {r1.status_code}, Post 2: {r2.status_code}). Retrying in 3s ({attempt}/{max_retries})...")
                        time.sleep(3)
                    else:
                        print(f"[ERROR] ❌ GitHub CDN images are not live after {max_retries} attempts.")
                        print("       Aborting webhook trigger to prevent sending broken/duplicate slides to Make.com!")
                        sys.exit(1)
        except Exception as e:
            print(f"[WARNING] Could not verify GitHub CDN status: {e}")

        print("[INFO] 🚀 Triggering 100% hands-free Instagram Carousel AFTER GitHub CDN push is live (with cache buster)...")
        if ig_automator.is_configured():
            ig_automator.publish_photo(
                image_url=github_cdn_post1_url,
                caption=campaign.get("instagram", {}).get("caption", ""),
                artwork_title=campaign.get("artwork_title", ""),
                image_url_2=github_cdn_post2_url
            )
        else:
            print("[INFO] No INSTAGRAM_ACCESS_TOKEN or MAKE_INSTAGRAM_WEBHOOK_URL set. Skipping post.")
        return

    if args.action == "daily-promo":
        artwork = history_mgr.pick_next_artwork(prints)
        print(f"[INFO] Selected today's promotion: '{artwork.get('title')}' ({artwork.get('price')})")

        m = re.search(r"josh1[- ](\d+)", artwork.get("title", ""), flags=re.IGNORECASE)
        num = int(m.group(1)) if m else 197
        
        post1_img_path = "output/post1_daily_instagram.jpg"
        post2_img_path = "output/post2_daily_instagram.jpg"
        
        generate_post1_dark_mode_portrait(num, artwork.get("title", ""), artwork.get("image_url", ""), 1, 1, post1_img_path)
        generate_post2_museum_monograph(num, artwork.get("title", ""), artwork.get("image_url", ""), 0, post2_img_path)

        campaign = gen.generate_campaign(artwork)
        history_mgr.record_promotion(artwork, campaign)
        notifier.save_campaign_artifacts(campaign)

        generate_html_report(
            [campaign],
            f"JOSH¹ Archive Curation — {campaign.get('artwork_title')}",
            "output/latest_campaign_report.html",
            config
        )

        notifier.export_pinterest_csv_queue([campaign], "output/pinterest_queue.csv")
        notifier.export_instagram_csv_queue([campaign], "output/instagram_queue.csv")

        notifier.notify_discord(campaign)
        notifier.notify_telegram(campaign)

        print(f"\n✅ Daily JOSH¹ Archive promotion successfully completed for: {artwork.get('title')}")

    elif args.action == "export-all":
        print(f"[INFO] Generating JOSH¹ Archive Phygital campaigns for ALL {len(prints)} prints...")
        all_campaigns = []
        for art in prints:
            camp = gen.generate_campaign(art)
            all_campaigns.append(camp)

        json_path = "output/all_campaigns.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_campaigns, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Saved full campaign data to {json_path}")

        notifier.export_pinterest_csv_queue(all_campaigns, "output/pinterest_bulk_queue.csv")
        notifier.export_instagram_csv_queue(all_campaigns, "output/instagram_bulk_queue.csv")

        generate_html_report(
            all_campaigns,
            f"{artist_name} ({sol_domain}) — Complete JOSH¹ Archive Catalog ({len(all_campaigns)} Prints)",
            "output/full_campaign_dashboard.html",
            config
        )

        print(f"\n✅ Full JOSH¹ Archive catalog campaign export completed! Checked {len(all_campaigns)} artworks.")

if __name__ == "__main__":
    main()
