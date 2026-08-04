"""
JOSH¹ Archive Phygital Art Content Generator.
Generates 100% AI-Proof, dash-free captions with clean indentation and spacing,
museum-grade materiality specs, Rarity/Device/Origin metadata, clean CTAs, and 3-4 random hashtags.
"""

import re
from typing import Dict, Any, List, Optional
import random

class ContentGenerator:
    """
    Generates promotional copy formatted in the signature JOSH¹ Archive style:
    - Zero hyphens or dashes anywhere in captions (- or — or –).
    - Clean 2-space indentation and elegant line spacing.
    - 300gsm cotton rag materiality & Solana provenance.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.artist = config.get("artist", {})
        self.promo = config.get("promotion", {})
        self.hashtags_pool = {
            "general": [
                "#PhygitalArt", "#SolanaNFT", "#Industrial", "#BrutalistArchitecture",
                "#ArchitecturalPhotography", "#FineArtPrint", "#JOSHSHOOTPRINTS",
                "#WallArtDecor", "#INPRNT", "#ArtCollector", "#SolanaArt",
                "#UrbanGeometry", "#ContemporaryCollector", "#ArchivalPrint",
                "#MinimalistPhotography", "#StreetPhotography", "#OnChainArt"
            ]
        }

    def _get_random_hashtags(self, count: int = 4) -> str:
        """Returns 3-5 randomly selected unique hashtags to prevent repetition."""
        pool = self.hashtags_pool["general"]
        selected = random.sample(pool, min(count, len(pool)))
        return " ".join(selected)

    def _resolve_highres_image(self, url: str, default_img: str) -> str:
        """Instantly converts INPRNT thumbnail URLs to 1080p (@2x) high-resolution format."""
        if default_img and "@2x" not in default_img and "cdn.inprnt.com" in default_img:
            return re.sub(r"(\.(?:jpg|png|webp))(?:\?.*)?$", r"@2x\1", default_img, flags=re.IGNORECASE)
        return default_img

    def _derive_location(self, title: str) -> str:
        """Derives accurate location coordinates/code from title or returns Rotterdam default."""
        lower = title.lower()
        if "amsterdam" in lower or "van gogh" in lower or "damstraat" in lower:
            return "Amsterdam (AMS) 🇳🇱"
        elif "leeds" in lower:
            return "Leeds (LBA) 🇬🇧"
        elif "waterloo" in lower or "london" in lower or "uk" in lower:
            return "London (LON) 🇬🇧"
        elif "asia" in lower or "mall" in lower or "filipino" in lower or "manila" in lower:
            return "Manila (MNL) 🇵🇭"
        elif "turkey" in lower or "36 hours" in lower or "istanbul" in lower:
            return "Istanbul (IST) 🇹🇷"
        elif "egypt" in lower or "cairo" in lower:
            return "Cairo (CAI) 🇪🇬"
        elif "paris" in lower:
            return "Paris (CDG) 🇫🇷"
        return "Rotterdam (RTM) 🇳🇱"

    def _derive_rarity(self, title: str) -> str:
        """Derives rarity classification from title or returns Common."""
        lower = title.lower()
        if "1/1" in lower or "monolith" in lower or "stars" in lower:
            return "Rare"
        return self.artist.get("default_rarity", "Common")

    def _clean_title_no_dashes(self, title: str) -> str:
        """Removes hyphens and dashes from title so it reads cleanly (e.g. JOSH1 197 • Maritime Museum)."""
        clean = re.sub(r"josh1[- ](\d+)[: -]*", r"JOSH1 \1 • ", title, flags=re.IGNORECASE)
        clean = clean.replace(" - ", " • ").replace(" — ", " • ").replace("–", " • ").replace("-", " ")
        return clean.strip()

    def _derive_human_lines(self, title: str) -> List[str]:
        """
        Returns 3 short, restrained, indented curatorial lines without any hyphens or dashes.
        """
        lower = title.lower()
        if "maritime" in lower:
            return [
                "  Rotterdam Maritime Museum",
                "  Brutalist mass against maritime history",
                "  An archival record of institutional form"
            ]
        elif "damstraat" in lower or "amsterdam" in lower:
            return [
                "  Amsterdam narrow alleyways",
                "  Spatial compression and natural light",
                "  Recorded within the European urban grid"
            ]
        elif "van gogh" in lower or "museum" in lower:
            return [
                "  Institutional architecture and public space",
                "  Structural geometry in natural light",
                "  An archival record of museum form"
            ]
        elif "waterloo" in lower or "station" in lower:
            return [
                "  Urban transit and architectural scale",
                "  Kinetic movement inside modern terminals",
                "  Recorded for architectural permanence"
            ]
        elif "leeds" in lower or "university" in lower:
            return [
                "  Educational brutalism",
                "  Concrete geometry and functional symmetry",
                "  Recorded within the university landscape"
            ]
        elif "kade" in lower or "scheepmaker" in lower or "street" in lower:
            return [
                "  Rotterdam waterfront architecture",
                "  Structural geometry along the urban harbor",
                "  Recorded for archival permanence"
            ]
        return [
            "  Architectural geometry and urban stillness",
            "  Structural symmetry recorded in natural light",
            "  An archival record of institutional form"
        ]

    def generate_campaign(self, artwork: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a complete JOSH¹ Archive Phygital marketing campaign package.
        """
        raw_title = artwork.get("title", "Archival Photograph")
        title_clean = self._clean_title_no_dashes(raw_title)
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", self.artist.get("gallery_url", ""))
        raw_image_url = artwork.get("image_url", "")
        
        image_url = self._resolve_highres_image(url, raw_image_url)
        artwork["image_url"] = image_url

        discount_note = artwork.get("discount_note", self.promo.get("default_discount_note", ""))
        artist_name = self.artist.get("name", "JOSH SHOOT")
        domain = self.artist.get("domain", "joshuadenouden21-hiuos.wordpress.com")
        solana_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")
        drip_url = self.artist.get("drip_url", "https://drip.haus/josh")

        location = self._derive_location(raw_title)
        rarity = self._derive_rarity(raw_title)
        device = self.artist.get("default_device", "iPhone 12")
        lines = self._derive_human_lines(raw_title)

        return {
            "artwork_id": artwork.get("id"),
            "artwork_title": title_clean,
            "artwork_url": url,
            "artwork_image": image_url,
            "price": price,
            "discount_note": discount_note,
            "solana_domain": solana_domain,
            "drip_url": drip_url,
            "location": location,
            "rarity": rarity,
            "device": device,
            "pinterest": self.generate_pinterest(title_clean, url, location, rarity, lines),
            "twitter_bluesky": self.generate_twitter_bluesky(title_clean, url, location, rarity, device, lines),
            "instagram": self.generate_instagram(title_clean, location, rarity, device, lines),
            "github_journal": self.generate_github_journal(title_clean, url, image_url, location, rarity, device, price)
        }

    def generate_pinterest(self, title: str, url: str, location: str, rarity: str, lines: List[str]) -> Dict[str, Any]:
        hashtags = self._get_random_hashtags(4)
        desc_text = " • ".join([l.strip() for l in lines])
        pin_description = (
            f"{desc_text}. {rarity} rarity asset in the JOSH¹ Archive ('{title}'). "
            f"Exclusively available as a limited edition Phygital Art piece, bridging Solana "
            f"blockchain provenance (JOSHSHOOT.SOL) and a gallery quality physical print. "
            f"Captured in {location}. Crafted on museum grade 300gsm 100% cotton rag archival paper "
            f"with custom pigment inks for lifetime color permanence via INPRNT. "
            f"Explore global shipping: {url} • {hashtags}"
        )

        return {
            "title": f"{title} | JOSH¹ Archive Brutalist Photography",
            "description": pin_description.strip(),
            "board": "JOSH¹ Archive // Phygital Photography Prints",
            "link": url,
            "hashtags": hashtags
        }

    def generate_twitter_bluesky(self, title: str, url: str, location: str, rarity: str, device: str, lines: List[str]) -> Dict[str, Any]:
        hashtags = self._get_random_hashtags(4)
        curatorial_block = "\n".join(lines)

        short_post = (
            f"「 {title} 」\n\n"
            f"{curatorial_block}\n\n"
            f"THE JOSH¹ ARCHIVE\n"
            f"Limited Edition Phygital Art Piece\n"
            f"Bridging Solana blockchain provenance to museum grade physical prints.\n\n"
            f"Collect the archive via INPRNT (link in bio)\n\n"
            f"📸 {device}\n"
            f"📍 {location}\n"
            f"💎 Rarity: {rarity}\n"
            f"⚡ On Chain: JOSHSHOOT.SOL\n\n"
            f"{hashtags}"
        )

        thread = [
            (
                f"1/ 🏛️ THE JOSH¹ ARCHIVE // \"{title}\"\n\n"
                f"{curatorial_block}\n\n"
                f"Bridging on chain Solana blockchain provenance (JOSHSHOOT.SOL) to physical tangibility.\n\n"
                f"📸 {device}\n"
                f"📍 {location}\n"
                f"💎 Rarity: {rarity}"
            ),
            (
                f"2/ Exclusively available as a museum grade archival fine art print on 300gsm 100% cotton rag paper.\n\n"
                f"🎉 Collector Release Price: 20% OFF\n"
                f"🌍 Global shipping via @inprnt\n\n"
                f"👉 Collect the physical asset: {url}\n\n"
                f"{hashtags}"
            )
        ]

        return {
            "short_post": short_post,
            "thread": thread,
            "hashtags": hashtags
        }

    def generate_instagram(self, title: str, location: str, rarity: str, device: str, lines: List[str]) -> Dict[str, Any]:
        hashtags = self._get_random_hashtags(4)
        curatorial_block = "\n".join(lines)

        caption = (
            f"{title}\n\n"
            f"{curatorial_block}\n\n"
            f"THE JOSH¹ ARCHIVE\n"
            f"Limited Edition Phygital Art Piece\n"
            f"Edition: 100% Cotton Rag Archival Fine Art Print (300gsm)\n"
            f"Provenance: Solana Blockchain verified (JOSHSHOOT.SOL) to Physical exhibition print via INPRNT\n\n"
            f"Collect the archive via link in bio\n"
            f"📸 {device}\n"
            f"📍 {location}\n"
            f"💎 Rarity: {rarity}\n"
            f"⚡ On Chain: JOSHSHOOT.SOL\n\n"
            f".\n.\n.\n"
            f"{hashtags}"
        )

        carousel_strategy = (
            "📌 CAROUSEL REVIVAL STRATEGY (Algorithmic reach hook):\n"
            "• Slide 1: Full high res photograph ('" + title + "')\n"
            "• Slide 2: Zoomed in crop showing cotton rag texture OR brutalist detail\n"
            "• Slide 3: On chain provenance graphic ('💎 Rarity: " + rarity + " | 📍 " + location + " | JOSHSHOOT.SOL')"
        )

        return {
            "caption": caption,
            "carousel_strategy": carousel_strategy,
            "hashtags": hashtags
        }

    def generate_github_journal(self, title: str, url: str, image_url: str, location: str, rarity: str, device: str, price: str) -> Dict[str, Any]:
        sol_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")
        drip_url = self.artist.get("drip_url", "https://drip.haus/josh")

        md_block = (
            f"## 🏛️ JOSH¹ Archive Featured Asset: \"{title}\"\n\n"
            f"<p align=\"center\">\n"
            f"  <a href=\"{url}\"><img src=\"{image_url}\" alt=\"{title}\" width=\"600\" /></a>\n"
            f"</p>\n\n"
            f"> *This is a **{rarity}** rarity asset in the **JOSH¹ Archive**. Exclusively available as a Limited Edition Phygital Art piece, bridging Solana Blockchain provenance (`{sol_domain}`) to a Gallery Quality physical print.*\n\n"
            f"### 📋 Technical Metadata\n"
            f"| Asset Classification | Metadata Specification |\n"
            f"| :--- | :--- |\n"
            f"| **Title** | `{title}` |\n"
            f"| **Rarity Classification** | `💎 {rarity}` |\n"
            f"| **Capture Device** | `📸 {device}` |\n"
            f"| **Location Origin** | `📍 {location}` |\n"
            f"| **Physical Medium** | `100% Cotton Rag Archival Print via INPRNT` |\n"
            f"| **Collector Release Price** | `{price}` *(20% OFF Limited Offer)* |\n"
            f"| **On Chain Provenance** | `{sol_domain}` &bull; [DRiP Archive]({drip_url}) |\n\n"
            f"🔗 **[Collect the archive via INPRNT &rarr;]({url})**"
        )

        return {
            "markdown": md_block,
            "title": f"JOSH¹ Asset Release: {title}"
        }
