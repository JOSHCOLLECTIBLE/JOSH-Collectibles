"""
JOSH¹ Archive Phygital Art Content Generator.
Generates concise, human, curatorial copy (100% AI-buzzword-free) with museum-grade
materiality specs, Rarity/Device/Origin metadata, clean CTAs, and 3-5 random hashtags.
"""

from typing import Dict, Any, List, Optional
import random

class ContentGenerator:
    """
    Generates promotional copy formatted in the signature JOSH¹ Archive style:
    restrained human curatorial notes, 300gsm cotton rag materiality, Solana provenance,
    clean bio links, and 3-5 random non-repeating hashtags.
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

    def _derive_human_note(self, title: str) -> str:
        """
        Generates clean, restrained human curatorial notes without AI buzzwords
        (no 'study in', no 'delve', no 'testament', no 'seamless').
        """
        lower = title.lower()
        if "maritime" in lower:
            return "Rotterdam's Maritime Museum. Brutalist mass against maritime history—an archival record of institutional form."
        elif "damstraat" in lower or "amsterdam" in lower:
            return "Amsterdam's narrow alleyways. Spatial compression and natural light in the European urban grid."
        elif "van gogh" in lower or "museum" in lower:
            return "Institutional architecture and public space. Structural geometry recorded in natural light."
        elif "waterloo" in lower or "station" in lower:
            return "Urban transit and architectural scale. Kinetic movement recorded inside modern transport terminals."
        elif "leeds" in lower or "university" in lower:
            return "Educational brutalism. Concrete geometry and functional symmetry in the university landscape."
        elif "kade" in lower or "scheepmaker" in lower or "street" in lower:
            return "Rotterdam waterfront architecture. Structural geometry along the urban harbor."
        elif "party" in lower or "mono" in lower or "praise" in lower or "night" in lower:
            return "Monochromatic depth and low-light atmosphere. Structural brutalism recorded after dark."
        return "Architectural geometry and urban stillness. Recorded for archival permanence."

    def generate_campaign(self, artwork: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a complete JOSH¹ Archive Phygital marketing campaign package.
        """
        title = artwork.get("title", "Archival Photograph")
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", self.artist.get("gallery_url", ""))
        image_url = artwork.get("image_url", "")
        discount_note = artwork.get("discount_note", self.promo.get("default_discount_note", ""))
        artist_name = self.artist.get("name", "JOSH SHOOT")
        domain = self.artist.get("domain", "joshuadenouden21-hiuos.wordpress.com")
        solana_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")
        drip_url = self.artist.get("drip_url", "https://drip.haus/josh")

        location = self._derive_location(title)
        rarity = self._derive_rarity(title)
        device = self.artist.get("default_device", "iPhone 12")
        note = self._derive_human_note(title)

        return {
            "artwork_id": artwork.get("id"),
            "artwork_title": title,
            "artwork_url": url,
            "artwork_image": image_url,
            "price": price,
            "discount_note": discount_note,
            "solana_domain": solana_domain,
            "drip_url": drip_url,
            "location": location,
            "rarity": rarity,
            "device": device,
            "pinterest": self.generate_pinterest(artwork, location, rarity, note),
            "twitter_bluesky": self.generate_twitter_bluesky(artwork, location, rarity, device, note),
            "instagram": self.generate_instagram(artwork, location, rarity, device, note),
            "github_journal": self.generate_github_journal(artwork, location, rarity, device)
        }

    def generate_pinterest(self, artwork: Dict[str, Any], location: str, rarity: str, note: str) -> Dict[str, Any]:
        """
        Generates Pinterest copy optimized for organic interior decor discovery
        with concise human descriptions and materiality terms.
        """
        title = artwork.get("title", "Archival Photograph")
        url = artwork.get("url", "")
        hashtags = self._get_random_hashtags(4)

        pin_title = f"{title} | JOSH¹ Archive Brutalist Photography & Fine Art Print"
        if len(pin_title) > 100:
            pin_title = f"{title} | JOSH¹ Archive Art Print"

        pin_description = (
            f"{note} {rarity} rarity asset in the JOSH¹ Archive ('{title}'). "
            f"Exclusively available as a limited edition Phygital Art piece, bridging Solana "
            f"blockchain provenance (JOSHSHOOT.SOL) and a gallery-quality physical print. "
            f"Captured in {location}. Crafted on museum-grade 300gsm 100% cotton rag archival paper "
            f"with custom pigment inks for lifetime color permanence via INPRNT. "
            f"Explore global shipping: {url} • {hashtags}"
        )

        return {
            "title": pin_title,
            "description": pin_description.strip(),
            "board": "JOSH¹ Archive // Phygital Photography Prints",
            "link": url,
            "hashtags": hashtags
        }

    def generate_twitter_bluesky(self, artwork: Dict[str, Any], location: str, rarity: str, device: str, note: str) -> Dict[str, Any]:
        """
        Generates punchy Web3/Solana collector posts and threads for Twitter/X and Bluesky.
        """
        title = artwork.get("title", "Archival Photograph")
        url = artwork.get("url", "")
        hashtags = self._get_random_hashtags(4)

        short_post = (
            f"「 {title} 」\n"
            f"{note}\n\n"
            f"JOSH¹ Archive — Limited Edition Phygital Art Piece\n"
            f"Bridging Solana blockchain provenance & museum-grade physical prints.\n\n"
            f"Collect the archive via INPRNT (link in bio)\n\n"
            f"📸 {device}\n"
            f"📍 {location}\n"
            f"💎 Rarity: {rarity}\n"
            f"⚡ On-Chain: JOSHSHOOT.SOL\n\n"
            f"{hashtags}"
        )

        thread = [
            (
                f"1/ 🏛️ THE JOSH¹ ARCHIVE // \"{title}\"\n\n"
                f"{note}\n\n"
                f"Bridging on-chain Solana blockchain provenance (JOSHSHOOT.SOL) and physical tangibility.\n\n"
                f"📸 {device}\n"
                f"📍 {location}\n"
                f"💎 Rarity: {rarity}"
            ),
            (
                f"2/ Exclusively available as a museum-grade archival fine art print on 300gsm 100% cotton rag paper.\n\n"
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

    def generate_instagram(self, artwork: Dict[str, Any], location: str, rarity: str, device: str, note: str) -> Dict[str, Any]:
        """
        Generates Instagram captions formatted like a human art monograph:
        restrained curatorial notes, clear materiality specs, clean bio link, and 3-5 random hashtags.
        """
        title = artwork.get("title", "Archival Photograph")
        hashtags = self._get_random_hashtags(4)

        caption = (
            f"{title}\n"
            f"{note}\n\n"
            f"JOSH¹ Archive — Limited Edition Phygital Art Piece\n"
            f"Edition: 100% Cotton Rag Archival Fine-Art Print (300gsm)\n"
            f"Provenance: Solana Blockchain verified (JOSHSHOOT.SOL) -> Physical exhibition print via INPRNT\n\n"
            f"Collect the archive via link in bio\n"
            f"📸 {device}\n"
            f"📍 {location}\n"
            f"💎 Rarity: {rarity}\n"
            f"⚡ On-Chain: JOSHSHOOT.SOL\n\n"
            f".\n.\n.\n"
            f"{hashtags}"
        )

        carousel_strategy = (
            "📌 CAROUSEL REVIVAL STRATEGY (Algorithmic reach hook):\n"
            "• Slide 1: Full high-res photograph ('" + title + "')\n"
            "• Slide 2: Zoomed-in crop showing cotton rag texture OR brutalist detail\n"
            "• Slide 3: On-chain provenance graphic ('💎 Rarity: " + rarity + " | 📍 " + location + " | JOSHSHOOT.SOL')"
        )

        return {
            "caption": caption,
            "carousel_strategy": carousel_strategy,
            "hashtags": hashtags
        }

    def generate_github_journal(self, artwork: Dict[str, Any], location: str, rarity: str, device: str) -> Dict[str, Any]:
        """
        Generates a GitHub Markdown block ready to be embedded in your JOSH-Collectibles
        repository README or featured as a GitHub Release.
        """
        title = artwork.get("title", "Archival Photograph")
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", "")
        image_url = artwork.get("image_url", "")
        sol_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")
        drip_url = self.artist.get("drip_url", "https://drip.haus/josh")

        md_block = (
            f"## 🏛️ JOSH¹ Archive Featured Asset: \"{title}\"\n\n"
            f"<p align=\"center\">\n"
            f"  <a href=\"{url}\"><img src=\"{image_url}\" alt=\"{title}\" width=\"600\" /></a>\n"
            f"</p>\n\n"
            f"> *This is a **{rarity}** rarity asset in the **JOSH¹ Archive**. Exclusively available as a Limited Edition Phygital Art piece, bridging Solana Blockchain provenance (`{sol_domain}`) and a Gallery-Quality physical print.*\n\n"
            f"### 📋 Technical Metadata\n"
            f"| Asset Classification | Metadata Specification |\n"
            f"| :--- | :--- |\n"
            f"| **Title** | `{title}` |\n"
            f"| **Rarity Classification** | `💎 {rarity}` |\n"
            f"| **Capture Device** | `📸 {device}` |\n"
            f"| **Location Origin** | `📍 {location}` |\n"
            f"| **Physical Medium** | `100% Cotton Rag Archival Print via INPRNT` |\n"
            f"| **Collector Release Price** | `{price}` *(20% OFF Limited Offer)* |\n"
            f"| **On-Chain Provenance** | `{sol_domain}` &bull; [DRiP Archive]({drip_url}) |\n\n"
            f"🔗 **[Collect the archive via INPRNT &rarr;]({url})**"
        )

        return {
            "markdown": md_block,
            "title": f"JOSH¹ Asset Release: {title}"
        }
