"""
JOSH¹ ARCHIVE - 100% Automated Bulk 1080x1920 MP4 Zoom-Out Reel Generator
================================================================================
Generates all 222 high-definition vertical MP4 video reels for the entire archive
(or a specified limit) using parallel processing.
- Automatically crops out INPRNT studio mockup borders.
- Renders 1080x1920 (9:16) Parisian Cream Museum Wall cards with 3D embossed typography.
- Applies buttery-smooth cosine-eased 1.15x -> 1.00x zoom-out animation.
"""

import os
import sys
import time
import argparse
from multiprocessing import Pool, cpu_count
from typing import List, Dict, Any

# Ensure root package is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scraper import InprntScraper
from generate_zoom_reel import generate_tiktok_zoom_reel

def process_single_reel(args_tuple):
    num, title, url, output_dir = args_tuple
    clean_title = title.replace("/", "_").replace("\\", "_")
    output_path = os.path.join(output_dir, f"JOSH1_{num:03d}_Zoom_Reel.mp4")
    if os.path.exists(output_path):
        print(f"[SKIP] Reel already exists: {output_path}")
        return output_path
    try:
        generate_tiktok_zoom_reel(num, title, url, output_path)
        return output_path
    except Exception as e:
        print(f"[ERROR] Failed to generate reel for #{num}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Bulk 1080x1920 MP4 Zoom-Out Reel Generator")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of reels to generate (0 = all 222)")
    parser.add_argument("--start-from", type=int, default=197, help="Starting artwork number (default 197)")
    parser.add_argument("--output-dir", default="output/all_reels", help="Output folder for MP4 videos")
    parser.add_argument("--workers", type=int, default=max(1, cpu_count() - 1), help="Number of parallel CPU workers")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    scraper = InprntScraper(gallery_url="https://www.inprnt.com/gallery/joshuadenouden/")
    prints = scraper.scrape_gallery_prints(use_cache=True)

    print(f"============================================================")
    print(f"🎬 JOSH¹ ARCHIVE BULK MP4 REEL GENERATOR")
    print(f"   Total Prints Loaded : {len(prints)}")
    print(f"   Target Output Folder: {args.output_dir}")
    print(f"   Parallel CPU Workers: {args.workers}")
    print(f"============================================================")

    # Prepare tasks in descending order from #222 down to #1
    tasks = []
    for art in prints:
        title = art.get("title", "")
        url = art.get("image_url", "")
        # extract number
        import re
        m = re.search(r"josh1[- ](\d+)", title, flags=re.IGNORECASE)
        if m:
            num = int(m.group(1))
            if num <= args.start_from:
                tasks.append((num, title, url, args.output_dir))

    # Sort descending by artwork number
    tasks.sort(key=lambda x: x[0], reverse=True)

    if args.limit > 0:
        tasks = tasks[:args.limit]
        print(f"[INFO] Applied limit: generating {len(tasks)} reels...")

    t0 = time.time()
    with Pool(processes=args.workers) as pool:
        results = pool.map(process_single_reel, tasks)

    success_count = len([r for r in results if r])
    total_time = round(time.time() - t0, 2)

    print(f"\n✅ COMPLETED BULK REEL GENERATION!")
    print(f"   Successfully Created : {success_count}/{len(tasks)} MP4 Reels")
    print(f"   Total Execution Time : {total_time} seconds ({round(total_time/max(1,success_count), 2)}s per reel)")
    print(f"   Saved inside folder  : {args.output_dir}")

if __name__ == "__main__":
    main()
