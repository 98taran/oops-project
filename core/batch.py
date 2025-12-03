# core/batch.py ← FINAL PERFECT VERSION

from datetime import datetime

class Batch:
    def __init__(self, batch_no, medicine, expiry_date, quantity, purchase_price):
        self.batch_no = batch_no.upper().strip()
        self.medicine = medicine
        self.expiry_date = expiry_date.strip()  # "2026-12-31"
        self.quantity = int(quantity)
        self.purchase_price = float(purchase_price)
        self.added_date = datetime.now().strftime("%Y-%m-%d")  # auto-set

    def is_expired(self):
        today = datetime.today().date()
        exp = datetime.strptime(self.expiry_date, '%Y-%m-%d').date()
        return today > exp

    def is_near_expiry(self, days=90):  # 90 days = 3 months (more realistic)
        exp = datetime.strptime(self.expiry_date, '%Y-%m-%d').date()
        delta = exp - datetime.today().date()
        return 0 < delta.days <= days

    def get_status(self):
        if self.is_expired():
            return "EXPIRED!", "red"
        if self.is_near_expiry():
            return "NEAR EXPIRY", "orange"
        return "OK", "lightgreen"

    def __str__(self):
        status, _ = self.get_status()
        return f"Batch: {self.batch_no} | Qty: {self.quantity} | Exp: {self.expiry_date} [{status}]"

    # ←←← THIS WAS MISSING A COLON! ←←←
    def to_dict(self) -> dict:
        return {
            "batch_no": self.batch_no,
            "medicine": self.medicine.to_dict(),
            "expiry_date": self.expiry_date,
            "quantity": self.quantity,
            "purchase_price": self.purchase_price,
            "added_date": self.added_date
        }