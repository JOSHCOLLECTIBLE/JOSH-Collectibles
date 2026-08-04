import json
import re
import yaml
from src.content_generator import ContentGenerator
from src.main import generate_html_report

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

with open('output/all_prints_cache.json', 'r', encoding='utf-8') as f:
    all_prints = json.load(f)

def get_num(title):
    m = re.search(r'josh1[- ](\d+)', title, flags=re.IGNORECASE)
    return int(m.group(1)) if m else -1

found = []
for p in all_prints:
    n = get_num(p['title'])
    if 188 <= n <= 197:
        found.append((n, p))

# Sort descending from 197 down to 188
found.sort(key=lambda x: x[0], reverse=True)

gen = ContentGenerator(config)
campaigns = []
md_lines = ["# 🏛️ The JOSH¹ Archive: First 10 Examples (#197 to #188 Descending)\n\n"]
md_lines.append("**Purpose:** Inspect and fine-tune copywriting quality, architectural hooks, clean CTAs (no long URLs or brackets), and 3-5 random hashtags before deploying sequential Instagram automation.\n\n---\n\n")

for n, p in found:
    camp = gen.generate_campaign(p)
    campaigns.append(camp)
    
    md_lines.append(f"## #{n} — {camp['artwork_title']}\n")
    md_lines.append(f"- **INPRNT Link:** [{camp['artwork_url']}]({camp['artwork_url']})\n")
    md_lines.append(f"- **Origin:** `📍 {camp['location']}` | **Rarity:** `💎 {camp['rarity']}` | **Device:** `📸 {camp['device']}`\n\n")
    md_lines.append(f'<p align="center"><a href="{camp["artwork_url"]}"><img src="{camp["artwork_image"]}" alt="{camp["artwork_title"]}" width="400" /></a></p>\n\n')
    
    md_lines.append("### 📸 Instagram / Threads Caption (@joshuadenouden)\n```text\n" + camp['instagram']['caption'] + "\n```\n\n")
    md_lines.append("### 🐦 Twitter / X Post (@Joshtakesphoto)\n```text\n" + camp['twitter_bluesky']['short_post'] + "\n```\n\n")
    md_lines.append("### 📌 Pinterest Pin Copy\n- **Title:** `" + camp['pinterest']['title'] + "`\n")
    md_lines.append("- **Description:**\n```text\n" + camp['pinterest']['description'] + "\n```\n\n---\n\n")

with open('output/first_10_examples_197_to_188.md', 'w', encoding='utf-8') as f:
    f.write(''.join(md_lines))

generate_html_report(
    campaigns,
    'JOSH¹ Archive — First 10 Examples (#197 to #188 Descending)',
    'output/first_10_examples_197_to_188.html',
    config
)
print("Successfully generated Markdown and HTML inspection reports for #197 down to #188!")
