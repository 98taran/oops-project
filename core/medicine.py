# core/medicine.py

class Medicine:
    def __init__(self, med_id, name, company="", salt="", mrp=0.0, purchase_price=0.0):
        self.med_id = med_id.upper()
        self.name = name.strip().title()
        self.company = company.strip()
        self.salt = salt.strip()
        self.mrp = float(mrp)
        self.purchase_price = float(purchase_price)

    def to_dict(self) -> dict:
        return {
            "med_id": self.med_id,
            "name": self.name,
            "company": self.company,
            "salt": self.salt,
            "mrp": self.mrp,
            "purchase_price": self.purchase_price
        }

    def __str__(self):
        return f"{self.name} ({self.company}) - ₹{self.mrp}"