"""
History and Storage Management Module.
Tracks previously promoted prints and sequences artworks sequentially
(e.g., from JOSH1 #197 / #199 onwards) for Instagram automation.
"""

import os
import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class HistoryManager:
    """Manages promotion history and sequential JOSH¹ Archive numbering."""

    def __init__(self, history_file_path: str = "output/history.json", config: Optional[Dict[str, Any]] = None):
        self.history_file_path = history_file_path
        self.config = config or {}
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensures that the directory for the history file exists."""
        directory = os.path.dirname(self.history_file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def load_history(self) -> Dict[str, Any]:
        """Loads promotion history from disk."""
        if not os.path.exists(self.history_file_path):
            return {
                "promoted_ids": [],
                "last_promoted_date": None,
                "history_log": []
            }
        try:
            with open(self.history_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Could not load history file ({e}), returning empty history.")
            return {
                "promoted_ids": [],
                "last_promoted_date": None,
                "history_log": []
            }

    def save_history(self, history_data: Dict[str, Any]) -> None:
        """Saves updated history to disk."""
        with open(self.history_file_path, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)

    def _extract_archive_number(self, title: str) -> int:
        """Extracts the numeric sequence number from a JOSH¹ title (e.g., JOSH1-199 -> 199)."""
        match = re.search(r"josh1[- ](\d+)", title, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0

    def pick_next_artwork(self, artworks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Selects the next artwork to promote.
        Prioritizes sequential JOSH¹ archive ordering (e.g., from #197 or #199 onwards).
        """
        if not artworks:
            return None

        history = self.load_history()
        promoted_ids = history.get("promoted_ids", [])

        # Sort artworks by their JOSH1-# number
        promo_config = self.config.get("promotion", {})
        start_num = int(promo_config.get("start_from_number", 199))
        direction = promo_config.get("sequence_direction", "ascending").lower()

        sorted_artworks = sorted(
            artworks,
            key=lambda a: self._extract_archive_number(a.get("title", "")),
            reverse=(direction == "descending")
        )

        # Filter for artworks that meet the starting sequence target
        eligible = []
        for art in sorted_artworks:
            num = self._extract_archive_number(art.get("title", ""))
            if direction == "descending" and num <= start_num:
                eligible.append(art)
            elif direction == "ascending" and num >= start_num:
                eligible.append(art)

        # If no artworks matched the filter, fallback to all sorted artworks
        pool = eligible if eligible else sorted_artworks

        # Find the first artwork in sequence that has NOT been promoted yet
        unpromoted = [art for art in pool if art.get("id") not in promoted_ids]
        if unpromoted:
            return unpromoted[0]

        # If all in pool have been promoted, pick the oldest promoted one
        for old_id in promoted_ids:
            for art in pool:
                if art.get("id") == old_id:
                    return art

        return pool[0]

    def record_promotion(self, artwork: Dict[str, Any], campaign: Dict[str, Any]) -> None:
        """Records a completed promotion run into history."""
        history = self.load_history()
        promoted_ids = history.get("promoted_ids", [])
        art_id = artwork.get("id")

        if art_id in promoted_ids:
            promoted_ids.remove(art_id)
        promoted_ids.append(art_id)

        history["promoted_ids"] = promoted_ids
        history["last_promoted_date"] = datetime.now().isoformat()
        
        log_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "artwork_id": art_id,
            "title": artwork.get("title"),
            "url": artwork.get("url"),
            "image_url": artwork.get("image_url")
        }
        
        log_list = history.get("history_log", [])
        log_list.append(log_entry)
        history["history_log"] = log_list[-100:]

        self.save_history(history)
