from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

class Bill:
    @staticmethod
    def generate_pdf(sale):
        filename = f"reports/Bill_{sale.sale_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height-50, "MEDISTOCK PRO")
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height-80, "Your Trusted Medical Store")

        y = height - 130
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Bill No: " + str(sale.sale_id))
        c.drawString(50, y-20, f"Date: {sale.date}")
        c.drawString(50, y-40, f"Customer: {sale.customer_name}")

        c.line(50, y-70, width-50, y-70)

        y -= 100
        c.drawString(50, y, "Item")
        c.drawString(300, y, "Qty")
        c.drawString(400, y, "Price")
        c.drawString(480, y, "Amount")
        y -= 30

        total = 0
        for item in sale.items:
            batch = item['batch']
            qty = item['qty']
            price = batch.medicine.mrp
            amount = qty * price
            total += amount
            c.drawString(50, y, batch.medicine.name[:30])
            c.drawString(310, y, str(qty))
            c.drawString(400, y, f"₹{price}")
            c.drawString(480, y, f"₹{amount}")
            y -= 25

        c.line(50, y-10, width-50, y-10)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(400, y-40, f"TOTAL: ₹{total}")

        c.drawCentredString(width/2, 50, "Thank You! Visit Again")
        c.save()
        return filename