# 🏛️ THE JOSH¹ ARCHIVE // OFFICIAL BRAND KIT & CURATORIAL GUIDE
**Artist:** JOSH SHOOT (Joshua den Ouden)  
**On-Chain Provenance:** `JOSHSHOOT.SOL` / DRiP Archive (`drip.haus/josh`)  
**Primary Gallery:** INPRNT (`https://www.inprnt.com/gallery/joshuadenouden/`)  
**Curatorial Voice:** The JOSH¹ Archive — authoritative, minimalist, tactile, museum-grade architectural and brutalist photography.  
**Core Value Proposition:** *Bridging Solana blockchain provenance with gallery-quality physical 300gsm cotton rag fine art prints.*

---

## 01. Typographic & Color Palette System

### 1. Official Color Palette
Designed for a macro slate-to-black dark mode grid architecture combined with Parisian cream exhibition wall cards:
- **Primary Void Black:** `#000000` (RGB `0, 0, 0`)
- **Parisian Cream Museum Plaster Wall:** `#F8F6F0` down to `#E8E4DA` (with subtle overhead track spotlighting)
- **Cotton Rag Mat White:** `#FFFFFF` to `#FBFBF9` (100% cotton rag double-matte)
- **Obsidian Inner Bevel:** `#181818` (1px obsidian accent border)
- **Solana Blue Accent:** `#38BDF8` (On-chain identity highlight)
- **Archive Gold Accent:** `#F59E0B` (Limited edition Phygital badge highlight)
- **Dynamic 3-Color Typographic Palette Extraction:** For every artwork, the engine extracts a color-harmonized 3-color palette (`primary_accent`, `deep_theme_color`, `muted_theme_color`) from the photograph.

### 2. Typographic Hierarchy & Specifications
- **Slide 1 Center Watermark:** `17pt Bold` (`SF Pro Display`, `DejaVu Sans Bold`) — centered straight and square on the photograph in white (`#F5F5F5`) with a subtle 1px dark shadow (`#000000`).
- **Slide 2 Monograph Title:** `34pt Bold` (`SF Pro Display`) — 100% dash-free (`JOSH1 196 BY JOSH SHOOT`) rendered in High-Relief 3D Embossed Typography.
- **Slide 2 INPRNT Gallery Badge:** `28pt Bold` — color-harmonized with the photograph's `primary_accent`.
- **Slide 2 Archival Specification Line:** `19pt Regular` — `300GSM COTTON RAG • ARCHIVAL EDITION` in muted archival tint.
- **Zoom Reel (`1080x1920`) Exhibition Typography:**
  - Top Title (`JOSH1 196 BY JOSH SHOOT`): `64pt Bold`
  - Primary Accent Badge (`JOSH SHOOT | INPRNT`): `52pt Bold`
  - Cotton Rag Specification: `36pt Regular`
  - Archival On-Chain Footer (`THE JOSH¹ ARCHIVE • JOSHSHOOT.SOL`): `44pt Bold`

---

## 02. Visual Deliverables & Grid Architecture

### 1. The 2-Post Release Strategy (2-Slide Carousel)
- **Slide 1 / Post 1 (`1080x1350` Vertical Portrait):**
  - **Full Black Void (`#000000`)** going from the outer edges ALL THE WAY until it reaches a crisp white gallery border (`#FFFFFF`, 22px width) around the pure photograph.
  - Photograph sits inside that white border straight and square (zero roundness, zero INPRNT mockup mat).
  - Designed for a continuous macro 3x3 dark-mode slate-to-black vertical gradient across your Instagram profile grid.
- **Slide 2 / Post 2 (`1080x1350` Museum Monograph Wall Card):**
  - **Parisian Cream Museum Plaster Wall (`#F8F6F0` down to `#E8E4DA`)** with overhead track spotlighting.
  - Gagosian/Hauser & Wirth double-matte framing (16px off-white 100% cotton rag mat `#FBFBF9` + 1px obsidian inner bevel line `#181818`).
  - **4x Supersampled smooth rounded corners (`radius = 20px`)** across photo, border, and mat.
  - High-Relief 3D Embossed Typography color-harmonized with each photograph's unique 3-color palette.

### 2. Cinematic Zoom-Out Reel (`1080x1920` / 9:16 Vertical Video)
- **Motion:** Starts slightly zoomed in (`1.15x` scale, 15% closer to the pure photograph) and applies luxury **cosine easing** to slowly, smoothly zoom out to `1.00x` full frame over 4 seconds, holding perfectly still for 1 second at the end (`30 fps`, 150 frames total).
- **Typography:** Bold Museum Exhibition Scale typography (`64pt` title) that fills out the width of the card and is effortless to read on any mobile device.

### 3. Instagram Profile Grid Math (Verified)
- **Row 1 (Top 3 Spots):** 3 Pinned Reels.
- **Row 2 (First Row of Posts):**
  - Left Column (`Col 0`): Earliest historical post.
  - Middle Column (`Col 1`): Post 143 (`#197: Maritime Museum, Rotterdam` — LIVE).
  - Right Column (`Col 2`): Post 144 (`#196: Damstraatjes, Amsterdam` — NEXT UP).

---

## 03. Editorial Copywriting & Hashtag Rules

### 1. Dash-Free Monograph Caption Template
- **Zero hyphens or dashes (`-`, `—`, `–`, `->`)** anywhere in titles, lines, or captions!
- Use clean 2-space indentation for architectural metadata lines modeled after Paris gallery exhibition catalogs.
- Clean Call to Action: `Collect the archive via link in bio` (zero clunky bracketed URLs in IG captions).
- Use only **3–4 unique, randomly selected non-repeating hashtags** per post.

```text
JOSH1 196 • Damstraatjes, Amsterdam

  Amsterdam Damstraatjes
  Brutalist mass against maritime history
  An archival record of institutional form

THE JOSH¹ ARCHIVE
Limited Edition Phygital Art Piece
Edition: 100% Cotton Rag Archival Fine Art Print (300gsm)
Provenance: Solana Blockchain verified (JOSHSHOOT.SOL) to Physical exhibition print via INPRNT

Collect the archive via link in bio
📸 iPhone 12 / Archival Capture
📍 Amsterdam (AMS) 🇳🇱
💎 Rarity: Common
⚡ On Chain: JOSHSHOOT.SOL

.
.
.
#WallArtDecor #SolanaNFT #JOSHSHOOTPRINTS #INPRNT
```

---

## 04. Automation & Technical Infrastructure

- **Scheduled Execution:** Daily at **16:30 UTC** (`30 16 * * *`) via zero-cost GitHub Actions — the peak global art collector crossover hour (`5:30 PM London | 6:30 PM Amsterdam/Rotterdam | 7:30 PM Cairo | 12:30 PM New York | 9:30 AM Los Angeles`).
- **Anti-Duplicate Safeguard:** 10-attempt HTTP `HEAD` CDN liveness wait loop (`?v={ts}`) before triggering Make.com webhook — guarantees zero duplicate slides and zero wasted free-tier credits.
- **Storage & History Sequencing:** Automatically prioritizes descending order from **`#197`** down to **`#1`**.
