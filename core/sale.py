# core/sale.py
from datetime import datetime
import json
import os

# --- Existing Sale class ---
class Sale:
    def __init__(self, sale_id, customer_name, items_list, total_amount):
        self.sale_id = sale_id
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.customer_name = customer_name
        self.items = items_list          # list of dicts: {'batch': batch_obj, 'qty': 5}
        self.total_amount = float(total_amount)

    def get_bill_details(self):
        lines = []
        for item in self.items:
            batch = item['batch']
            lines.append(f"{batch.medicine.name} × {item['qty']} = ₹{item['qty'] * batch.medicine.mrp}")
        return lines


# --- ADD THIS NEW CLASS ---
class SaleManager:
    SALES_FILE = "data/sales.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.SALES_FILE):
            with open(self.SALES_FILE, 'w') as f:
                json.dump([], f)

    def get_next_sale_id(self):
        sales = self.load_sales()
        if not sales:
            return 1
        return max(sale["sale_id"] for sale in sales) + 1

    def load_sales(self):
        try:
            with open(self.SALES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []

    def save_sales(self, sales):
        with open(self.SALES_FILE, 'w') as f:
            json.dump(sales, f, indent=2)

    def add_sale(self, sale: Sale):
        sales = self.load_sales()
        # Convert Sale object to dict for saving
        sale_dict = {
            "sale_id": sale.sale_id,
            "date": sale.date,
            "customer_name": sale.customer_name,
            "total_amount": sale.total_amount,
            "items": [
                {
                    "medicine_name": item['batch'].medicine.name,
                    "batch_no": item['batch'].batch_no,
                    "expiry": item['batch'].expiry,
                    "qty": item['qty'],
                    "mrp": item['batch'].medicine.mrp
                }
                for item in sale.items
            ]
        }
        sales.append(sale_dict)
        self.save_sales(sales)

    def get_all_sales(self):
        return self.load_sales()