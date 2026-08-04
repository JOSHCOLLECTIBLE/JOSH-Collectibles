# 🎨 JOSHSHOOT PRINTS — Multi-Channel Art Marketing Bot

An automated, **100% free cloud-ready** marketing engine built for INPRNT artists (configured for **[JOSH SHOOT - Joshua den Ouden](https://www.inprnt.com/profile/joshuadenouden/)** &bull; `JOSHSHOOT.SOL`).

This tool automatically scrapes your INPRNT gallery, tracks previously promoted artworks to prevent repetition, and generates **high-converting, avant-garde editorial promotional campaigns** across:
- **📌 Pinterest:** Minimalist, architectural SEO Titles, rich descriptions, board recommendations, tags, and a **bulk CSV queue** ready for instant import.
- **🐦 Twitter / X & Bluesky:** Punchy "JOSHSHOOT PRINTS &bull; ARCHIVAL RELEASE" short-form posts with emojis, discount badges, links, and a **2-part storytelling thread**.
- **📸 Instagram / TikTok:** High-luxury editorial captions with structured curatorial specs and a targeted **30-hashtag stack**.
- **🔴 Reddit:** Authentic, non-spammy showcase copy tailored for art collector subreddits (`r/Artstore`, `r/artprints`, `r/photographicprints`, `r/artcollectors`, `r/streetphotography`).
- **📧 Newsletter / Email:** Clean HTML and Markdown digest cards for Substack, Mailchimp, or Beehiiv.

---

## 🚀 Features

1. **Zero-Cost GitHub Actions Cloud Automation:**
   - Runs automatically on a daily schedule (`0 14 * * *` - 2 PM UTC daily) on GitHub Actions.
   - Requires **no servers, no paid APIs, and no monthly fees**.
   - Automatically commits updated promotion history (`output/history.json`) back to your repository so it never promotes the same artwork two days in a row.

2. **Interactive HTML Visual Report & Copy Dashboard:**
   - Generates a beautifully styled luxury HTML report (`output/latest_campaign_report.html` & `output/full_campaign_dashboard.html`) with thumbnail previews and **1-click Copy to Clipboard buttons** for every platform.

3. **Discord & Telegram Automated Notifications:**
   - Can send daily embedded alerts directly to your Discord server or Telegram chat with ready-to-post copy-paste blocks!

4. **Pinterest Bulk CSV Queue:**
   - Automatically exports `output/pinterest_queue.csv` and `output/pinterest_bulk_queue.csv`, formatted for immediate upload to Pinterest, Later, Buffer, or Tailwind.

---

## 📂 Project Structure

```text
inprnt_marketing_bot/
├── README.md                          # This overview document
├── SETUP_GUIDE.md                     # Step-by-step GitHub deployment & organic marketing playbook
├── GITHUB_SETUP_JOSH_COLLECTIBLES.md    # Guide to update your existing JOSH-Collectibles repo from Step 1
├── MARKET_TRENDS_2026.md              # 2026 Fine Art Print Sales & Market Trends Report
├── config.yaml                        # Configuration for artist URL, discount notes, hashtags, & channels
├── requirements.txt                   # Python dependencies (requests, beautifulsoup4, pyyaml, jinja2, rich)
├── .github/
│   └── workflows/
│       └── daily_art_promotion.yml    # 100% Free automated GitHub Actions cron workflow
├── src/
│   ├── scraper.py                     # INPRNT gallery scraper & metadata parser
│   ├── content_generator.py           # JOSHSHOOT PRINTS editorial SEO & copy generator
│   ├── storage.py                     # History tracking (history.json) to cycle through all prints
│   ├── notifier.py                    # Discord, Telegram, and CSV export integration
│   └── main.py                        # CLI entrypoint & HTML report dashboard generator
└── output/                            # Generated daily reports, CSV queues, & history
```

---

## 💻 Local Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Daily Promotion (Single Print)
Picks the next unpromoted artwork from your shop, generates all marketing copy, updates history, and saves reports:
```bash
python -m src.main --action daily-promo
```

### 3. Generate Complete Catalog Campaign (All Prints)
Scrapes your entire INPRNT gallery and creates a comprehensive marketing dashboard (`output/full_campaign_dashboard.html`) and bulk Pinterest CSV (`output/pinterest_bulk_queue.csv`):
```bash
python -m src.main --action export-all
```

### 4. Test Discord / Telegram Alerts
```bash
python -m src.main --action test-webhook
```
