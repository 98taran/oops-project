# ui/add_medicine.py ← FINAL 100% WORKING VERSION (Back button FIXED!)

import customtkinter as ctk
from core.medicine import Medicine
from core.batch import Batch
from core.inventory import InventoryManager


def show_add_medicine(root, user, on_back=None):
    """
    Shows the Add Medicine screen.
    :param root: Main Tk window
    :param user: Current logged-in user object
    :param on_back: Optional callback to return to previous screen (highly recommended)
    """
    # Clear screen
    for widget in root.winfo_children():
        widget.destroy()

    root.title("MediStock Pro – Add New Medicine / Batch")

    # Header
    ctk.CTkLabel(root, text="Add New Medicine / Batch", font=("Arial", 32, "bold")).pack(pady=30)

    # Form frame
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=100, fill="x")

    entries = {}
    fields = [
        ("Medicine Name", True),
        ("Company", False),
        ("Salt", False),
        ("MRP (₹)", False),
        ("Purchase Price (₹)", False),
        ("Batch No", True),
        ("Expiry (YYYY-MM-DD)", True),
        ("Quantity", True)
    ]

    for i, (field, required) in enumerate(fields):
        label_text = field + (" *" if required else "") + " :"
        ctk.CTkLabel(frame, text=label_text, anchor="w", font=("Arial", 14)).grid(
            row=i, column=0, sticky="w", pady=10, padx=20
        )
        entry = ctk.CTkEntry(frame, width=350, height=40, font=("Arial", 14))
        entry.grid(row=i, column=1, pady=10, padx=20)
        entries[field] = entry

    # Status label
    status_label = ctk.CTkLabel(frame, text="", font=("Arial", 14))
    status_label.grid(row=len(fields), column=0, columnspan=2, pady=15)

    def save_medicine():
        try:
            required = ["Medicine Name", "Batch No", "Expiry (YYYY-MM-DD)", "Quantity", "MRP (₹)", "Purchase Price (₹)"]
            for field in required:
                if not entries[field].get().strip():
                    raise ValueError(f"{field} is required!")

            name = entries["Medicine Name"].get().strip()
            mrp = float(entries["MRP (₹)"].get().strip())
            purchase = float(entries["Purchase Price (₹)"].get().strip())
            qty = int(entries["Quantity"].get().strip())

            if mrp <= 0 or purchase <= 0 or qty <= 0:
                raise ValueError("MRP, Purchase Price and Quantity must be positive")

            # Create Medicine & Batch objects
            med = Medicine(
                med_id="M" + "".join(w[0] for w in name.split()[:3]).upper(),
                name=name,
                company=entries["Company"].get().strip(),
                salt=entries["Salt"].get().strip(),
                mrp=mrp,
                purchase_price=purchase
            )

            batch = Batch(
                batch_no=entries["Batch No"].get().strip().upper(),
                medicine=med,
                expiry_date=entries["Expiry (YYYY-MM-DD)"].get().strip(),
                quantity=qty,
                purchase_price=purchase
            )

            # Save to persistent inventory
            InventoryManager().add_batch(batch)

            status_label.configure(text="Medicine & Batch Added Successfully!", text_color="#00ff00")

            # Clear form
            for entry in entries.values():
                entry.delete(0, "end")

        except ValueError as ve:
            status_label.configure(text=f"Error: {ve}", text_color="#ff5555")
        except Exception as e:
            status_label.configure(text=f"Unexpected Error: {str(e)}", text_color="#ff5555")

    # SAVE BUTTON
    ctk.CTkButton(
        root,
        text="SAVE MEDICINE",
        width=300,
        height=50,
        fg_color="#00aa00",
        hover_color="#007700",
        font=("Arial", 18, "bold"),
        command=save_medicine
    ).pack(pady=25)

    # BACK BUTTON – 100% RELIABLE (uses on_back callback if provided)
    def go_back():
        if on_back:
            on_back()
        else:
            # Safe fallback – import only when needed
            from ui.dashboard import show_dashboard
            show_dashboard(root, user)

    ctk.CTkButton(
        root,
        text="Back to Dashboard",
        width=240,
        height=48,
        fg_color="#555555",
        hover_color="#444444",
        font=("Arial", 15, "bold"),
        corner_radius=12,
        command=go_back
    ).pack(pady=15)