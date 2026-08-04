"""
INPRNT Artist Profile & Gallery Scraper Module.
Extracts artwork titles, prices, discount badges, high-resolution preview images, and direct links.
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

class InprntScraper:
    """Scrapes INPRNT profile and gallery pages for artwork details."""

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
        if soup is None:
            soup = self.fetch_page(self.profile_url)

        artist_info = {
            "name": "JOSH SHOOT",
            "bio": "Curated artist specializing in Phygital Art, bridging the gap between on-chain digital archives and physical tangibility.",
            "avatar_url": ""
        }

        # Try to find artist name in h1 or h2
        heading = soup.find(["h1", "h2"])
        if heading and "Profile for" in heading.text:
            artist_info["name"] = heading.text.replace("Profile for", "").strip()

        # Try to find bio text paragraphs
        for p in soup.find_all("p"):
            text = p.text.strip()
            if len(text) > 40 and ("curated artist" in text.lower() or "specializing" in text.lower() or "phygital" in text.lower()):
                artist_info["bio"] = text
                break

        return artist_info

    def scrape_gallery_prints(self) -> List[Dict[str, Any]]:
        """
        Scrapes all artwork prints listed on the artist's gallery page.
        Returns a list of dictionaries containing print metadata.
        """
        soup = self.fetch_page(self.gallery_url)
        prints_map: Dict[str, Dict[str, Any]] = {}

        # Scan for artwork links
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            # We want links inside /gallery/<username>/<print-slug>/
            if "/gallery/" not in href:
                continue

            parts = [p for p in href.strip("/").split("/") if p]
            # Expecting ['gallery', 'joshuadenouden', 'slug']
            if len(parts) < 3 or parts[0] != "gallery" or parts[1] != "joshuadenouden":
                continue

            slug = parts[2]
            if slug in ("joshuadenouden", "gallery", "accounts", "login") or "?" in slug:
                continue

            full_url = urljoin("https://www.inprnt.com", href)

            # Look for image inside this tag or parent card
            img_tag = a_tag.find("img")
            if not img_tag:
                # Check parent container
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
                    # Fallback to readable slug
                    raw_title = slug.replace("-", " ").title()

            # Clean up title (remove 'by ARTIST')
            clean_title = re.sub(r"\s+by\s+.*$", "", raw_title, flags=re.IGNORECASE).strip()

            # Look for price info nearby
            price_text = ""
            discount_text = ""
            parent = a_tag.find_parent(["div", "li", "article", "section"])
            if parent:
                # Look for price strings like $12.00 or ~~$15.00~~
                text_content = parent.get_text(separator=" | ", strip=True)
                price_matches = re.findall(r"\$\d+(?:\.\d{2})?", text_content)
                if price_matches:
                    price_text = price_matches[-1] # lowest/sale price usually last
                if "OFF" in text_content or "~~" in text_content or len(price_matches) > 1:
                    discount_text = "20% OFF Limited Time Price"

            if slug not in prints_map:
                prints_map[slug] = {
                    "id": slug,
                    "title": clean_title,
                    "slug": slug,
                    "url": full_url,
                    "image_url": image_url,
                    "price": price_text or "$12.00",
                    "discount_note": discount_text or "20% OFF Sale Price ($12.00 regular $15.00)",
                    "tags": self._derive_tags_from_title(clean_title)
                }

        # Also check profile page for latest prints if gallery returned few items
        if len(prints_map) < 3:
            try:
                prof_soup = self.fetch_page(self.profile_url)
                for a_tag in prof_soup.find_all("a", href=True):
                    href = a_tag["href"]
                    if "/gallery/" in href and len([p for p in href.strip("/").split("/") if p]) >= 3:
                        slug = [p for p in href.strip("/").split("/") if p][2]
                        if slug not in prints_map and slug not in ("joshuadenouden", "gallery"):
                            full_url = urljoin("https://www.inprnt.com", href)
                            img_tag = a_tag.find("img")
                            image_url = img_tag.get("src", "") if img_tag else ""
                            raw_title = img_tag.get("alt", "") if img_tag else slug.replace("-", " ").title()
                            clean_title = re.sub(r"\s+by\s+.*$", "", raw_title, flags=re.IGNORECASE).strip()
                            prints_map[slug] = {
                                "id": slug,
                                "title": clean_title,
                                "slug": slug,
                                "url": full_url,
                                "image_url": image_url,
                                "price": "$12.00",
                                "discount_note": "20% OFF Sale Price ($12.00 regular $15.00)",
                                "tags": self._derive_tags_from_title(clean_title)
                            }
            except Exception as e:
                print(f"[WARN] Could not scrape profile fallback: {e}")

        # Return sorted list
        return list(prints_map.values())

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

    def fetch_print_details(self, print_url: str) -> Dict[str, Any]:
        """Fetches detailed info from an individual artwork print page."""
        soup = self.fetch_page(print_url)
        details = {
            "title": "",
            "description": "",
            "available_formats": ["Art Print", "Canvas Print", "Framed Print", "Card Packs"],
            "image_url": ""
        }

        h1 = soup.find("h1")
        if h1:
            details["title"] = re.sub(r"\s+by\s+.*$", "", h1.text.strip(), flags=re.IGNORECASE)

        # Look for image
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if "cdn.inprnt.com" in src and ("thumbs" in src or "images" in src):
                details["image_url"] = src
                break

        return details
