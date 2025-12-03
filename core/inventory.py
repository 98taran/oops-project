# core/inventory.py ← FINAL PERSISTENT VERSION

import json
import os
from typing import List, Dict
from core.batch import Batch

class InventoryManager:
    _instance = None
    DB_FILE = "data/inventory.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.batches = cls._instance._load_from_disk()
        return cls._instance

    def _load_from_disk(self) -> List[Dict]:
        if not os.path.exists(self.DB_FILE):
            return []
        try:
            with open(self.DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"Loaded {len(data)} batches from disk.")
                return data
        except Exception as e:
            print(f"Error loading inventory: {e}")
            return []

    def _save_to_disk(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open(self.DB_FILE, "w", encoding="utf-8") as f:
                json.dump(self.batches, f, indent=2, default=str)
            print(f"SAVED {len(self.batches)} batches to {self.DB_FILE}")
        except Exception as e:
            print(f"FAILED to save inventory: {e}")

    def add_batch(self, batch: Batch):
        batch_data = batch.to_dict()  # ← You need this method in Batch class!
        self.batches.append(batch_data)
        self._save_to_disk()  # ← THIS IS THE MAGIC LINE

    def get_all_batches(self) -> List[Dict]:
        return self.batches

    def get_low_stock(self, threshold=10):
        return [b for b in self.batches if b["quantity"] <= threshold]

    def get_near_expiry(self, months=3):
        from datetime import datetime, timedelta
        cutoff = (datetime.now() + timedelta(days=months*30)).date()
        return [b for b in self.batches if datetime.strptime(b["expiry_date"], "%Y-%m-%d").date() <= cutoff]