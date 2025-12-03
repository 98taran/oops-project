# core/inventory.py ← FINAL PERSISTENT VERSION WITH PROPER OBJECT LOADING

import json
import os
from typing import List, Dict
from datetime import datetime, timedelta
from core.batch import Batch
from core.medicine import Medicine

class InventoryManager:
    _instance = None
    DB_FILE = "data/inventory.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.batches = cls._instance._load_from_disk()
        return cls._instance

    def _dict_to_batch(self, data: Dict) -> Batch:
        """Convert dict from JSON back to Batch object"""
        try:
            med_data = data.get("medicine", {})
            medicine = Medicine(
                med_id=med_data.get("med_id", ""),
                name=med_data.get("name", ""),
                company=med_data.get("company", ""),
                salt=med_data.get("salt", ""),
                mrp=float(med_data.get("mrp", 0)),
                purchase_price=float(med_data.get("purchase_price", 0))
            )
            batch = Batch(
                batch_no=data.get("batch_no", ""),
                medicine=medicine,
                expiry_date=data.get("expiry_date", ""),
                quantity=int(data.get("quantity", 0)),
                purchase_price=float(data.get("purchase_price", 0))
            )
            # Restore original added_date if exists
            if "added_date" in data:
                batch.added_date = data["added_date"]
            return batch
        except Exception as e:
            print(f"Error converting batch data: {e}")
            return None

    def _load_from_disk(self) -> List[Batch]:
        """Load batches from JSON and convert to Batch objects"""
        if not os.path.exists(self.DB_FILE):
            return []
        try:
            with open(self.DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                batches = []
                for item in data:
                    batch = self._dict_to_batch(item)
                    if batch:
                        batches.append(batch)
                print(f"[OK] Loaded {len(batches)} batches from disk.")
                return batches
        except Exception as e:
            print(f"[ERROR] Error loading inventory: {e}")
            return []

    def _save_to_disk(self):
        """Save all batches to JSON"""
        os.makedirs("data", exist_ok=True)
        try:
            data = [batch.to_dict() for batch in self.batches]
            with open(self.DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            print(f"[OK] SAVED {len(self.batches)} batches to {self.DB_FILE}")
        except Exception as e:
            print(f"[ERROR] FAILED to save inventory: {e}")

    def add_batch(self, batch: Batch):
        """Add a new batch to inventory"""
        self.batches.append(batch)
        self._save_to_disk()

    def get_all_batches(self) -> List[Batch]:
        """Return all batches as Batch objects"""
        return self.batches

    def get_low_stock(self, threshold=10) -> List[Batch]:
        """Get batches with stock below threshold"""
        return [b for b in self.batches if b.quantity <= threshold]

    def get_near_expiry(self, months=3) -> List[Batch]:
        """Get batches expiring soon"""
        cutoff = (datetime.now().date().replace(day=1) + timedelta(days=months*30))
        return [b for b in self.batches if datetime.strptime(b.expiry_date, "%Y-%m-%d").date() <= cutoff]

    def get_expired_batches(self) -> List[Batch]:
        """Get all expired batches"""
        return [b for b in self.batches if b.is_expired()]

    def remove_expired_batches(self):
        """Remove expired batches from inventory"""
        self.batches = [b for b in self.batches if not b.is_expired()]
        self._save_to_disk()