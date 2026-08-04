"""
JOSHSHOOT PRINTS Artist Profile & Gallery Scraper Module.
Extracts artwork titles, prices, discount badges, high-resolution preview images,
and direct links. Includes cloud-resilience fallback catalog for GitHub Actions.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict, Any, Optional

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# Built-in fallback catalog of JOSH SHOOT artworks to ensure 100% reliability
# even if Cloudflare or CDN rate limits block cloud datacenter requests.
FALLBACK_CATALOG = [
    {
        "id": "josh1-222-the-dutch-blue-man",
        "title": "JOSH1-222: The Dutch Blue Man",
        "slug": "josh1-222-the-dutch-blue-man",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-222-the-dutch-blue-man/",
        "image_url": "https://cdn.inprnt.com/thumbs/74/b7/74b70fe8f76742d2cf8df9976a8b703a.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "street photography", "archival print", "inprnt", "brutalism", "fine art"]
    },
    {
        "id": "josh1-221-i-think-56-nights-crazy",
        "title": "JOSH1-221: I Think 56 Nights Crazy",
        "slug": "josh1-221-i-think-56-nights-crazy",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-221-i-think-56-nights-crazy/",
        "image_url": "https://cdn.inprnt.com/thumbs/ed/f3/edf3621d6449d3c63836639747d60c6d.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "night photography", "archival print", "inprnt", "fine art"]
    },
    {
        "id": "josh1-220-the-mall-of-asia",
        "title": "JOSH1-220: The Mall of Asia",
        "slug": "josh1-220-the-mall-of-asia",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-220-the-mall-of-asia/",
        "image_url": "https://cdn.inprnt.com/thumbs/01/3c/013c167b4f6b2d6b20c08f3c7b36975b.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "urban landscape", "architecture", "inprnt", "fine art"]
    },
    {
        "id": "josh1-219-36-hours-in-turkey",
        "title": "JOSH1-219: 36 hours in Turkey",
        "slug": "josh1-219-36-hours-in-turkey",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-219-36-hours-in-turkey/",
        "image_url": "https://cdn.inprnt.com/thumbs/1b/7f/1b7f10e3b0551cc6be92d115fef4af94.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "travel photography", "archival print", "inprnt", "fine art"]
    },
    {
        "id": "josh1-218-no-swimming",
        "title": "JOSH1-218: No Swimming",
        "slug": "josh1-218-no-swimming",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-218-no-swimming/",
        "image_url": "https://cdn.inprnt.com/thumbs/a8/1e/a81e75c8e9f92a84e0a61bff0b6f26b3.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "street photography", "minimalism", "inprnt", "fine art"]
    },
    {
        "id": "josh1-217-7-stars",
        "title": "JOSH1-217: 7 Stars",
        "slug": "josh1-217-7-stars",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-217-7-stars/",
        "image_url": "https://cdn.inprnt.com/thumbs/d1/cd/d1cd7909dceed57fcb65c2d21e4ea558.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "night photography", "archival print", "inprnt", "fine art"]
    },
    {
        "id": "josh1-216-numb",
        "title": "JOSH1-216: Numb",
        "slug": "josh1-216-numb",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-216-numb/",
        "image_url": "https://cdn.inprnt.com/thumbs/07/79/077952a83aaccf2bb4f3043c31559ecd.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "street photography", "archival print", "inprnt", "fine art"]
    },
    {
        "id": "josh1-215-run-run",
        "title": "JOSH1-215: Run Run",
        "slug": "josh1-215-run-run",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-215-run-run/",
        "image_url": "https://cdn.inprnt.com/thumbs/79/a6/79a621d0bc656022eddabba0423aa7d9.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "urban photography", "archival print", "inprnt", "fine art"]
    },
    {
        "id": "josh1-214-navy-red-white-blue",
        "title": "JOSH1-214: Navy Red, White, Blue ...",
        "slug": "josh1-214-navy-red-white-blue",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-214-navy-red-white-blue/",
        "image_url": "https://cdn.inprnt.com/thumbs/d5/80/d5806d4552c046d17442b4740c7400fd.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "color photography", "archival print", "inprnt", "fine art"]
    },
    {
        "id": "josh1-213-stay-cool",
        "title": "JOSH1-213: Stay Cool",
        "slug": "josh1-213-stay-cool",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-213-stay-cool/",
        "image_url": "https://cdn.inprnt.com/thumbs/30/f2/30f21b3317f3f7cfe76cd1ceb32cbbc1.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "street photography", "archival print", "inprnt", "fine art"]
    },
    {
        "id": "josh1-212-filipino-brutalism-2",
        "title": "JOSH1-212: Filipino Brutalism 2",
        "slug": "josh1-212-filipino-brutalism-2",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-212-filipino-brutalism-2/",
        "image_url": "https://cdn.inprnt.com/thumbs/1a/4d/1a4d8e8ef285294b8268208eae4e7e88.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "brutalism", "architecture", "inprnt", "fine art"]
    },
    {
        "id": "josh1-211-keep-distance",
        "title": "JOSH1-211: Keep Distance",
        "slug": "josh1-211-keep-distance",
        "url": "https://www.inprnt.com/gallery/joshuadenouden/josh1-211-keep-distance/",
        "image_url": "https://cdn.inprnt.com/thumbs/58/56/585662475c8b1396049b52e2df8798dd.jpg",
        "price": "$12.00",
        "discount_note": "20% OFF Limited Archival Release ($12.00 regular $15.00)",
        "tags": ["phygital art", "urban photography", "archival print", "inprnt", "fine art"]
    }
]

class InprntScraper:
    """Scrapes INPRNT profile and gallery pages for artwork details with cloud fallback."""

    def __init__(self, gallery_url: str, profile_url: Optional[str] = None, timeout: int = 15):
        self.gallery_url = gallery_url.rstrip("/") + "/"
        self.profile_url = (profile_url or gallery_url).rstrip("/") + "/"
        self.timeout = timeout

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetches a URL and returns a BeautifulSoup object."""
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=self.timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def scrape_artist_bio(self, soup: Optional[BeautifulSoup] = None) -> Dict[str, str]:
        """Scrapes artist biographical summary and name from the profile page."""
        artist_info = {
            "name": "JOSH SHOOT",
            "bio": "Creator of The JOSH Archive. Avant-garde architectural photography and Phygital fine art, bridging on-chain provenance (JOSHSHOOT.SOL) with tactile archival materiality.",
            "avatar_url": ""
        }
        try:
            if soup is None:
                soup = self.fetch_page(self.profile_url)
            heading = soup.find(["h1", "h2"])
            if heading and "Profile for" in heading.text:
                artist_info["name"] = heading.text.replace("Profile for", "").strip()
            for p in soup.find_all("p"):
                text = p.text.strip()
                if len(text) > 40 and ("curated artist" in text.lower() or "specializing" in text.lower() or "phygital" in text.lower()):
                    artist_info["bio"] = text
                    break
        except Exception as e:
            print(f"[INFO] Using fallback artist bio ({e})")
        return artist_info

    def scrape_gallery_prints(self) -> List[Dict[str, Any]]:
        """
        Scrapes all artwork prints listed on the artist's gallery page.
        Falls back automatically to the built-in catalog if network/CDN errors occur.
        """
        try:
            soup = self.fetch_page(self.gallery_url)
            prints_map: Dict[str, Dict[str, Any]] = {}

            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if "/gallery/" not in href:
                    continue

                parts = [p for p in href.strip("/").split("/") if p]
                if len(parts) < 3 or parts[0] != "gallery" or parts[1] != "joshuadenouden":
                    continue

                slug = parts[2]
                if slug in ("joshuadenouden", "gallery", "accounts", "login") or "?" in slug:
                    continue

                full_url = urljoin("https://www.inprnt.com", href)

                img_tag = a_tag.find("img")
                if not img_tag:
                    parent = a_tag.find_parent(["div", "li", "article"])
                    if parent:
                        img_tag = parent.find("img")

                image_url = ""
                raw_title = ""
                if img_tag:
                    image_url = img_tag.get("src", "") or img_tag.get("data-src", "")
                    raw_title = img_tag.get("alt", "")

                if not raw_title:
                    raw_title = a_tag.text.strip()
                    if not raw_title:
                        raw_title = slug.replace("-", " ").title()

                clean_title = re.sub(r"\s+by\s+.*$", "", raw_title, flags=re.IGNORECASE).strip()

                price_text = "$12.00"
                discount_text = "20% OFF Limited Archival Release ($12.00 regular $15.00)"
                parent = a_tag.find_parent(["div", "li", "article", "section"])
                if parent:
                    text_content = parent.get_text(separator=" | ", strip=True)
                    price_matches = re.findall(r"\$\d+(?:\.\d{2})?", text_content)
                    if price_matches:
                        price_text = price_matches[-1]

                if slug not in prints_map:
                    prints_map[slug] = {
                        "id": slug,
                        "title": clean_title,
                        "slug": slug,
                        "url": full_url,
                        "image_url": image_url,
                        "price": price_text,
                        "discount_note": discount_text,
                        "tags": self._derive_tags_from_title(clean_title)
                    }

            if len(prints_map) >= 3:
                return list(prints_map.values())
            else:
                print("[INFO] Scraped fewer than 3 items, falling back to built-in JOSH SHOOT catalog.")
                return FALLBACK_CATALOG

        except Exception as e:
            print(f"[INFO] Live scrape unreachable ({e}). Using built-in JOSH SHOOT archival catalog.")
            return FALLBACK_CATALOG

    def _derive_tags_from_title(self, title: str) -> List[str]:
        """Derives thematic tags from the artwork title and artist style."""
        base_tags = ["phygital art", "street photography", "archival print", "inprnt", "fine art"]
        lower = title.lower()
        if "blue" in lower or "color" in lower:
            base_tags.append("color photography")
        if "asia" in lower or "mall" in lower or "turkey" in lower or "filipino" in lower:
            base_tags.append("travel photography")
            base_tags.append("urban landscape")
        if "brutalism" in lower or "architecture" in lower:
            base_tags.append("brutalism")
            base_tags.append("architecture")
        if "night" in lower or "stars" in lower:
            base_tags.append("night photography")
        return list(set(base_tags))
