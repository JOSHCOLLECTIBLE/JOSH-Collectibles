"""
History and Storage Management Module.
Tracks previously promoted prints so that daily automated runs cycle through all artworks.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class HistoryManager:
    """Manages promotion history to prevent repetition and cycle through all artworks."""

    def __init__(self, history_file_path: str = "output/history.json"):
        self.history_file_path = history_file_path
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

    def pick_next_artwork(self, artworks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Selects the next artwork to promote.
        Prioritizes artworks that have not been promoted yet, or the oldest promoted artwork.
        """
        if not artworks:
            return None

        history = self.load_history()
        promoted_ids = history.get("promoted_ids", [])

        # Find prints that have NEVER been promoted yet
        unpromoted = [art for art in artworks if art.get("id") not in promoted_ids]
        if unpromoted:
            return unpromoted[0]

        # If all have been promoted, reset or cycle from the start
        # Pick the one that was promoted longest ago (first in promoted_ids)
        for old_id in promoted_ids:
            for art in artworks:
                if art.get("id") == old_id:
                    return art

        return artworks[0]

    def record_promotion(self, artwork: Dict[str, Any], campaign: Dict[str, Any]) -> None:
        """Records a completed promotion run into history."""
        history = self.load_history()
        promoted_ids = history.get("promoted_ids", [])
        art_id = artwork.get("id")

        if art_id in promoted_ids:
            promoted_ids.remove(art_id)
        promoted_ids.append(art_id) # Move to end of recently promoted

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
        # Keep last 100 log entries
        history["history_log"] = log_list[-100:]

        self.save_history(history)
