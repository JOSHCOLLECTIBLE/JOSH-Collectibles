"""
JOSHSHOOT PRINTS Editorial Content Generator for INPRNT Artworks.
Generates avant-garde, curatorial, high-fashion editorial prose that bridges
on-chain provenance (JOSHSHOOT.SOL) with physical museum-grade archival prints.
"""

from typing import Dict, Any, List, Optional
import random

class ContentGenerator:
    """
    Generates promotional campaigns styled after high-luxury editorial copy:
    architectural, elevated, tactile, and linked to JOSHSHOOT.SOL.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.artist = config.get("artist", {})
        self.promo = config.get("promotion", {})
        self.hashtags = self.promo.get("hashtags", {})

    def generate_campaign(self, artwork: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a complete JOSHSHOOT PRINTS editorial multi-channel marketing campaign package.
        """
        title = artwork.get("title", "Archival Photograph")
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", self.artist.get("gallery_url", ""))
        image_url = artwork.get("image_url", "")
        discount_note = artwork.get("discount_note", self.promo.get("default_discount_note", ""))
        artist_name = self.artist.get("name", "JOSH SHOOT")
        solana_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")
        drip_url = self.artist.get("drip_url", "https://drip.haus/josh")
        twitter_handle = self.artist.get("twitter_handle", "@joshuadenouden")

        return {
            "artwork_id": artwork.get("id"),
            "artwork_title": title,
            "artwork_url": url,
            "artwork_image": image_url,
            "price": price,
            "discount_note": discount_note,
            "solana_domain": solana_domain,
            "drip_url": drip_url,
            "pinterest": self.generate_pinterest(artwork),
            "twitter_bluesky": self.generate_twitter_bluesky(artwork),
            "instagram": self.generate_instagram(artwork),
            "reddit": self.generate_reddit(artwork),
            "newsletter": self.generate_newsletter(artwork)
        }

    def generate_pinterest(self, artwork: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates JOSHSHOOT PRINTS Pinterest copy: minimalist, architectural,
        SEO-optimized for high-end interior aesthetics and art collectors.
        """
        title = artwork.get("title", "Archival Photograph")
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", "")
        artist_name = self.artist.get("name", "JOSH SHOOT")
        sol_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")

        pin_title = f"{title} | Archival Brutalist Photography & Fine Art Print by {artist_name}"
        if len(pin_title) > 100:
            pin_title = f"{title} | Archival Fine Art Print — {artist_name}"

        pin_description = (
            f"An exploration of architectural geometry and kinetic stillness. "
            f"'{title}' by {artist_name} ({sol_domain}) translates brutalist urban space "
            f"and chromatic depth into museum-grade physical permanence. "
            f"Bridging on-chain provenance with tactile materiality, each print is rendered on "
            f"100% cotton rag archival paper with pigment inks via INPRNT. "
            f"Curated pricing: {price} (20% OFF Limited Archival Release). "
            f"Available in Gallery Art Prints, Canvas, Acrylic, and Custom Framed editions. "
            f"Explore contemporary architectural photography for luxury interiors and collectors. "
            f"On-chain verification: {sol_domain} | {url} • "
            f"{' '.join(self.hashtags.get('pinterest', []))}"
        )

        return {
            "title": pin_title,
            "description": pin_description.strip(),
            "board": "Architectural Photography & Brutalist Art Prints",
            "link": url,
            "hashtags": " ".join(self.hashtags.get("pinterest", []))
        }

    def generate_twitter_bluesky(self, artwork: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates sleek, avant-garde editorial micro-essays and a 2-part curatorial
        thread for Twitter/X and Bluesky.
        """
        title = artwork.get("title", "Archival Photograph")
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", "")
        artist_name = self.artist.get("name", "JOSH SHOOT")
        sol_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")
        drip_url = self.artist.get("drip_url", "https://drip.haus/josh")

        hashtag_str = " ".join(self.hashtags.get("twitter_bluesky", [])[:4])

        # Short avant-garde editorial post
        short_post = (
            f"JOSHSHOOT PRINTS • ARCHIVAL RELEASE\n\n"
            f"🏛️ \"{title}\" — {artist_name} ({sol_domain})\n\n"
            f"Where on-chain provenance meets brutalist materiality. "
            f"Architectural geometry captured in museum-grade physical permanence.\n\n"
            f"✦ Edition Spec: 100% Cotton Rag Archival Print\n"
            f"✦ Collector Pricing: {price} (20% OFF)\n\n"
            f"🔗 Acquire Physical Print: {url}\n"
            f"⚡ On-Chain Archive: {sol_domain}\n\n"
            f"{hashtag_str}"
        )

        # 2-Tweet Editorial Curatorial Thread
        thread = [
            (
                f"1/ 🏛️ THE ARCHIVE CHOREOGRAPHY // \"{title}\"\n\n"
                f"In the architectural work of {artist_name} ({sol_domain}), urban transit and brutalist "
                f"geometry are elevated into monolithic visual records.\n\n"
                f"Bridging digital provenance and physical tangibility—from on-chain archives to tactile museum prints."
            ),
            (
                f"2/ Rendered on 100% cotton rag archival paper with archival pigment inks, "
                f"ensuring chromatic permanence for collectors.\n\n"
                f"✦ Archival Release Pricing: {price} (20% OFF on @inprnt)\n"
                f"✦ Physical Shop: {url}\n"
                f"✦ Web3 Identity: {sol_domain} | {drip_url}\n\n"
                f"{hashtag_str}"
            )
        ]

        return {
            "short_post": short_post,
            "thread": thread,
            "hashtags": hashtag_str
        }

    def generate_instagram(self, artwork: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates high-fashion editorial magazine layout captions for Instagram/Threads/TikTok.
        """
        title = artwork.get("title", "Archival Photograph")
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", "")
        artist_name = self.artist.get("name", "JOSH SHOOT")
        sol_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")

        caption = (
            f"JOSHSHOOT PRINTS // THE PHYGITAL MONOLITH\n\n"
            f"「 {title} 」\n"
            f"Architectural Photography & Archival Fine Art by {artist_name} ({sol_domain})\n\n"
            f"An inquiry into brutalist geometry, urban movement, and tactile permanence. "
            f"Here, the fleeting moments of architectural choreography are frozen into "
            f"archival museum-grade tangibility.\n\n"
            f"CURATORIAL SPECIFICATIONS:\n"
            f"━ Physical Medium: 100% Cotton Rag Archival Fine Art Paper\n"
            f"━ Provenance: On-chain digital archive ({sol_domain}) &rarr; INPRNT Physical Release\n"
            f"━ Available Editions: Standard Print, Gallery Canvas, Acrylic Monolith, Custom Framed\n"
            f"━ Current Collector Pricing: {price} (20% OFF Limited Archival Release)\n"
            f"━ Worldwide Shipping & Packaging via INPRNT\n\n"
            f"🔗 Acquire the physical edition via link in bio or directly:\n"
            f"{url}\n\n"
            f"⚡ Verified On-Chain Identity: {sol_domain}\n\n"
            f".\n.\n.\n"
            f"{' '.join(self.hashtags.get('instagram', []))}"
        )

        return {
            "caption": caption,
            "hashtags": " ".join(self.hashtags.get("instagram", []))
        }

    def generate_reddit(self, artwork: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates an intellectual, curatorial artist showcase for Reddit collector communities,
        framing the print as a physical artifact from an on-chain architectural archive.
        """
        title = artwork.get("title", "Archival Photograph")
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", "")
        artist_name = self.artist.get("name", "JOSH SHOOT")
        sol_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")

        reddit_title = (
            f"[FOR SALE] \"{title}\" — Archival Brutalist Photography & Fine Art Print "
            f"by {artist_name} ({sol_domain}) | {price} (20% OFF on INPRNT)"
        )

        reddit_body = (
            f"### Curatorial Release: \"{title}\" by {artist_name} (`{sol_domain}`)\n\n"
            f"Hello everyone in the collector community. I'm sharing an archival photographic release from my "
            f"studio and on-chain catalog: **\"{title}\"**.\n\n"
            f"#### 🏛️ Editorial & Artistic Focus\n"
            f"My practice as **{artist_name}** (`{sol_domain}`) investigates **architectural geometry, brutalist monoliths, "
            f"and urban stillness**. Rather than viewing digital and physical art as separate realms, my work bridges the gap "
            f"between decentralized on-chain archives and physical, museum-grade tangibility.\n\n"
            f"#### 📐 Physical Print Specifications (INPRNT)\n"
            f"- **Materiality:** 300gsm 100% cotton rag archival fine-art paper with custom pigment inks for lifetime chromatic preservation.\n"
            f"- **Available Formats:** Archival Art Prints, Gallery-Wrapped Canvas, Acrylic, Metal Prints, and Custom Framed Editions.\n"
            f"- **Collector Pricing:** **{price}** *(20% OFF promotional pricing for the archival release)*.\n"
            f"- **Provenance & Verification:** Digital origin verified via **{sol_domain}**; physical exhibition print fulfilled via **INPRNT**.\n\n"
            f"#### 🔗 Links & Acquisition\n"
            f"- **Acquire Physical Print on INPRNT:** [{url}]({url})\n"
            f"- **Browse Complete Archival Gallery:** [https://www.inprnt.com/gallery/joshuadenouden/](https://www.inprnt.com/gallery/joshuadenouden/)\n"
            f"- **Web3 Provenance & Digital Archive:** `{sol_domain}` | [DRiP Archive](https://drip.haus/josh)\n\n"
            f"*Thank you to the independent art collectors supporting tangible archival print releases. I welcome any discussions regarding brutalist photography, sizing, or framing.*"
        )

        return {
            "title": reddit_title,
            "body": reddit_body,
            "target_subreddits": self.config.get("promotion", {}).get("target_subreddits", [])
        }

    def generate_newsletter(self, artwork: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates JOSHSHOOT PRINTS high-fashion editorial newsletter feature in Markdown & HTML.
        """
        title = artwork.get("title", "Archival Photograph")
        price = artwork.get("price", "$12.00")
        url = artwork.get("url", "")
        image_url = artwork.get("image_url", "")
        artist_name = self.artist.get("name", "JOSH SHOOT")
        sol_domain = self.artist.get("solana_domain", "JOSHSHOOT.SOL")
        drip_url = self.artist.get("drip_url", "https://drip.haus/josh")

        md_content = (
            f"## JOSHSHOOT PRINTS // THE ARCHIVE RELEASE\n\n"
            f"### Featured Monolith: \"{title}\"\n\n"
            f"![{title}]({image_url})\n\n"
            f"In this week's curatorial release from the **{artist_name}** (`{sol_domain}`) archive, "
            f"we examine **\"{title}\"**—a study in brutalist architectural geometry and chromatic stillness.\n\n"
            f"Where digital provenance meets museum-grade physical permanence, this piece is rendered on 100% cotton rag archival paper via INPRNT.\n\n"
            f"**Curatorial & Collector Specifications:**\n"
            f"- **Archival Price:** {price} (20% OFF Limited Release)\n"
            f"- **Materiality:** 100% Cotton Rag Fine Art Paper / Pigment Inks\n"
            f"- **On-Chain Provenance:** `{sol_domain}` | [{drip_url}]({drip_url})\n\n"
            f"[**Acquire Museum-Grade Print on INPRNT &rarr;**]({url})"
        )

        html_content = (
            f'<div style="border: 1px solid #1e293b; border-radius: 4px; padding: 32px; max-width: 640px; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; background-color: #ffffff; color: #0f172a;">\n'
            f'  <div style="font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #64748b; font-weight: 700; margin-bottom: 12px;">JOSHSHOOT PRINTS // The Archive Release</div>\n'
            f'  <h2 style="font-size: 26px; font-weight: 800; letter-spacing: -0.5px; color: #0f172a; margin: 0 0 20px 0;">"{title}"</h2>\n'
            f'  <img src="{image_url}" alt="{title}" style="width: 100%; border-radius: 2px; margin-bottom: 24px; border: 1px solid #e2e8f0;" />\n'
            f'  <p style="color: #334155; line-height: 1.7; font-size: 15px; margin-bottom: 16px;">'
            f'    In this week\'s curatorial release from the <strong>{artist_name}</strong> (<code>{sol_domain}</code>) archive, '
            f'    we examine <strong>"{title}"</strong>—a study in brutalist architectural geometry and chromatic stillness.'
            f'  </p>\n'
            f'  <p style="color: #475569; line-height: 1.7; font-size: 14px; margin-bottom: 24px;">'
            f'    Where digital provenance meets museum-grade physical permanence, each print is rendered on 300gsm 100% cotton rag archival paper via INPRNT.'
            f'  </p>\n'
            f'  <div style="background-color: #f8fafc; border-left: 3px solid #0f172a; padding: 16px; margin-bottom: 24px;">\n'
            f'    <div style="font-size: 13px; color: #0f172a;"><strong>Collector Price:</strong> {price} (20% OFF Limited Archival Release)</div>\n'
            f'    <div style="font-size: 13px; color: #475569; margin-top: 4px;"><strong>On-Chain Identity:</strong> {sol_domain} &bull; drip.haus/josh</div>\n'
            f'  </div>\n'
            f'  <a href="{url}" style="display: inline-block; background-color: #0f172a; color: #ffffff; padding: 14px 28px; text-decoration: none; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; font-weight: 700; border-radius: 2px;">Acquire Physical Print &rarr;</a>\n'
            f'</div>'
        )

        return {
            "markdown": md_content,
            "html": html_content
        }
