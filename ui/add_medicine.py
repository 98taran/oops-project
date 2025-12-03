# ui/add_medicine.py – IMPROVED WITH BETTER UI & VALIDATION

import customtkinter as ctk
from core.medicine import Medicine
from core.batch import Batch
from core.inventory import InventoryManager
from datetime import datetime


def show_add_medicine(root, user, on_back=None):
    """
    Shows the Add Medicine screen with enhanced validation and UI.
    :param root: Main Tk window
    :param user: Current logged-in user object
    :param on_back: Optional callback to return to previous screen
    """
    # Clear screen
    for widget in root.winfo_children():
        widget.destroy()

    root.title("MediStock Pro – Add New Medicine / Batch")

    # Header
    header_frame = ctk.CTkFrame(root, fg_color="#1f538d")
    header_frame.pack(fill="x", pady=(0, 20))
    ctk.CTkLabel(header_frame, text="➕ Add New Medicine / Batch", font=("Arial", 28, "bold"), text_color="white").pack(pady=15)

    # Main form frame with scrolling
    main_frame = ctk.CTkScrollableFrame(root)
    main_frame.pack(pady=10, padx=50, fill="both", expand=True)

    entries = {}
    fields = [
        ("Medicine Name", True),
        ("Company", False),
        ("Salt Composition", False),
        ("MRP (₹)", False),
        ("Purchase Price (₹)", False),
        ("Batch Number", True),
        ("Expiry Date (YYYY-MM-DD)", True),
        ("Quantity", True)
    ]

    for i, (field, required) in enumerate(fields):
        label_text = field + (" *" if required else "")
        ctk.CTkLabel(
            main_frame, text=label_text, font=("Arial", 13, "bold" if required else "normal")
        ).pack(anchor="w", pady=(15, 5), padx=20)
        
        entry = ctk.CTkEntry(main_frame, width=400, height=40, font=("Arial", 12))
        entry.pack(anchor="w", padx=20, pady=(0, 10), fill="x")
        entries[field] = entry

    # Status label
    status_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 13, "bold"))
    status_label.pack(pady=15)

    def save_medicine():
        try:
            # Validate required fields
            required_fields = [
                ("Medicine Name", True),
                ("Batch Number", True),
                ("Expiry Date (YYYY-MM-DD)", True),
                ("Quantity", True),
                ("MRP (₹)", True),
                ("Purchase Price (₹)", True)
            ]
            
            for field_name, _ in required_fields:
                if not entries[field_name].get().strip():
                    raise ValueError(f"❌ {field_name} is required!")

            # Extract and validate values
            name = entries["Medicine Name"].get().strip()
            if len(name) < 2:
                raise ValueError("❌ Medicine name must be at least 2 characters")
                
            try:
                mrp = float(entries["MRP (₹)"].get().strip())
                purchase = float(entries["Purchase Price (₹)"].get().strip())
                qty = int(entries["Quantity"].get().strip())
            except ValueError:
                raise ValueError("❌ MRP, Purchase Price must be numbers and Quantity must be an integer")

            if mrp <= 0 or purchase <= 0 or qty <= 0:
                raise ValueError("❌ MRP, Purchase Price and Quantity must be positive")
            
            if purchase > mrp:
                raise ValueError("❌ Purchase Price cannot be greater than MRP")

            # Validate expiry date
            expiry_str = entries["Expiry Date (YYYY-MM-DD)"].get().strip()
            try:
                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
                if expiry_date < datetime.now():
                    raise ValueError("❌ Expiry date must be in the future")
            except ValueError as e:
                if "time data" in str(e):
                    raise ValueError("❌ Expiry date must be in format YYYY-MM-DD")
                raise

            # Create Medicine & Batch objects
            med = Medicine(
                med_id="M" + "".join(w[0] for w in name.split()[:3]).upper(),
                name=name,
                company=entries["Company"].get().strip(),
                salt=entries["Salt Composition"].get().strip(),
                mrp=mrp,
                purchase_price=purchase
            )

            batch = Batch(
                batch_no=entries["Batch Number"].get().strip().upper(),
                medicine=med,
                expiry_date=expiry_str,
                quantity=qty,
                purchase_price=purchase
            )

            # Save to persistent inventory
            InventoryManager().add_batch(batch)

            status_label.configure(text="✅ Medicine & Batch Added Successfully!", text_color="#00ff00")

            # Clear form
            for entry in entries.values():
                entry.delete(0, "end")
            
            # Reset focus
            entries["Medicine Name"].focus()

        except ValueError as ve:
            status_label.configure(text=str(ve), text_color="#ff5555")
        except Exception as e:
            status_label.configure(text=f"❌ Unexpected Error: {str(e)}", text_color="#ff5555")

    # Bottom action buttons
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=20, fill="x", padx=20)

    # SAVE BUTTON
    ctk.CTkButton(
        button_frame,
        text="💾 SAVE MEDICINE",
        width=280,
        height=50,
        fg_color="#00aa00",
        hover_color="#007700",
        font=("Arial", 15, "bold"),
        corner_radius=10,
        command=save_medicine
    ).pack(side="left", padx=10)

    # BACK BUTTON – with improved error handling
    def go_back():
        if on_back:
            on_back()
        else:
            # Safe fallback
            from ui.dashboard import show_dashboard
            show_dashboard(root, user)

    ctk.CTkButton(
        button_frame,
        text="← Back to Dashboard",
        width=280,
        height=50,
        fg_color="#555555",
        hover_color="#666666",
        font=("Arial", 15, "bold"),
        corner_radius=10,
        command=go_back
    ).pack(side="right", padx=10)