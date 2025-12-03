# ui/consumer_store.py - Consumer Shopping Interface

import customtkinter as ctk
from tkinter import ttk
from core.inventory import InventoryManager
from core.sale import SaleManager
from datetime import datetime


def show_consumer_store(root, user, on_back=None):
    """Consumer store screen - browse and buy medicines."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("MediStock Pro – Shop")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Header
    header_frame = ctk.CTkFrame(root, fg_color="#1f538d")
    header_frame.pack(fill="x", pady=(0, 15))
    ctk.CTkLabel(header_frame, text="🛒 Welcome to MediStock Shop", font=("Arial", 28, "bold"), text_color="white").pack(pady=15)

    # Search bar
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(pady=10, fill="x", padx=50)

    ctk.CTkLabel(search_frame, text="Search Medicine:", font=("Arial", 14)).pack(side="left", padx=10)
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, width=400, font=("Arial", 13))
    search_entry.pack(side="left", padx=10, fill="x", expand=True)

    # Treeview container
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(pady=20, padx=50, fill="both", expand=True)

    # ttk.Treeview for medicines
    columns = ("Name", "Company", "Price", "Available", "Status", "Action")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Styling
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    rowheight=40,
                    fieldbackground="#2b2b2b",
                    font=("Arial", 12))
    style.configure("Treeview.Heading",
                    background="#1f538d",
                    foreground="white",
                    font=("Arial", 12, "bold"))
    style.map("Treeview", background=[("selected", "#3475aa")])

    # Column setup
    tree.heading("Name", text="Medicine Name")
    tree.heading("Company", text="Company")
    tree.heading("Price", text="Price (₹)")
    tree.heading("Available", text="Available")
    tree.heading("Status", text="Status")
    tree.heading("Action", text="Action")

    tree.column("Name", width=200, anchor="w")
    tree.column("Company", width=130)
    tree.column("Price", width=100)
    tree.column("Available", width=100)
    tree.column("Status", width=100)
    tree.column("Action", width=100)

    # Row coloring
    tree.tag_configure("oddrow", background="#2b2b2b")
    tree.tag_configure("evenrow", background="#242424")
    tree.tag_configure("expired", background="#3d1f1f", foreground="#ff4444")
    tree.tag_configure("near_expiry", background="#3d3d1f", foreground="#ffaa00")
    tree.tag_configure("low_stock", background="#3d3d1f", foreground="#ffff00")
    tree.tag_configure("ok", background="#2b2b2b", foreground="#00ff00")

    def refresh_store():
        """Load available medicines (not expired)"""
        tree.delete(*tree.get_children())

        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        search = search_var.get().lower()

        for i, batch in enumerate(all_batches):
            # Skip expired and out-of-stock items
            if batch.quantity <= 0 or batch.is_expired():
                continue

            # Apply search
            name = batch.medicine.name.lower()
            if search and search not in name and search not in batch.medicine.company.lower():
                continue

            # Get status
            status_text, _ = batch.get_status()
            
            row_tag = ("evenrow" if i % 2 else "oddrow")
            if batch.is_near_expiry():
                row_tag = ("evenrow" if i % 2 else "oddrow", "near_expiry")
            elif batch.quantity <= 10:
                row_tag = ("evenrow" if i % 2 else "oddrow", "low_stock")
            else:
                row_tag = ("evenrow" if i % 2 else "oddrow", "ok")

            tree.insert("", "end", values=(
                batch.medicine.name,
                batch.medicine.company,
                f"₹{batch.medicine.mrp:.2f}",
                batch.quantity,
                status_text,
                "BUY"
            ), tags=(batch.batch_no,) + row_tag)

    search_var.trace("w", lambda *_: refresh_store())

    # Buy medicine popup
    def buy_medicine(event=None):
        sel = tree.selection()
        if not sel:
            return
        
        item = tree.item(sel[0])
        batch_no = item["tags"][0] if item["tags"] else None
        if not batch_no:
            return

        batch = next((b for b in InventoryManager().get_all_batches() if b.batch_no == batch_no), None)
        if not batch or batch.quantity == 0 or batch.is_expired():
            return

        # Buy popup
        popup = ctk.CTkToplevel(root)
        popup.title("Buy Medicine")
        popup.geometry("400x350")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text=batch.medicine.name, font=("Arial", 20, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(popup, text=f"Company: {batch.medicine.company}", font=("Arial", 12)).pack(pady=5)
        ctk.CTkLabel(popup, text=f"Price: ₹{batch.medicine.mrp:.2f}", font=("Arial", 14, "bold")).pack(pady=5)
        ctk.CTkLabel(popup, text=f"Available: {batch.quantity} units", font=("Arial", 12)).pack(pady=5)
        
        status_text, _ = batch.get_status()
        ctk.CTkLabel(popup, text=f"Status: {status_text}", font=("Arial", 11)).pack(pady=5)

        ctk.CTkLabel(popup, text="Quantity to Buy:", font=("Arial", 13)).pack(pady=(15, 5))
        qty_var = ctk.StringVar(value="1")
        qty_entry = ctk.CTkEntry(popup, textvariable=qty_var, width=100, font=("Arial", 14), justify="center")
        qty_entry.pack()
        qty_entry.focus_force()

        msg_label = ctk.CTkLabel(popup, text="", text_color="red")
        msg_label.pack(pady=8)

        def confirm_purchase():
            try:
                qty = int(qty_var.get())
                if qty <= 0:
                    raise ValueError("Enter positive quantity")
                if qty > batch.quantity:
                    raise ValueError(f"Only {batch.quantity} available!")
                if batch.is_expired():
                    raise ValueError("Medicine is expired!")
                
                # Record purchase
                SaleManager().sell_batch(batch, qty)
                msg_label.configure(text=f"✅ Purchase successful! {qty} units ordered.", text_color="lightgreen")
                refresh_store()
                popup.after(1500, popup.destroy)
            except ValueError as e:
                msg_label.configure(text=str(e), text_color="red")

        ctk.CTkButton(popup, text="Confirm Purchase", fg_color="green", height=40, command=confirm_purchase).pack(pady=15)
        popup.bind("<Return>", lambda e: confirm_purchase())

    tree.bind("<Double-1>", buy_medicine)

    # Stats frame
    stats_frame = ctk.CTkFrame(root, fg_color="#242424")
    stats_frame.pack(fill="x", pady=10, padx=50)

    stats_label = ctk.CTkLabel(stats_frame, text="", font=("Arial", 11), text_color="#aaaaaa")
    stats_label.pack(side="left", padx=10, pady=8)

    def update_stats():
        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        available = len([b for b in all_batches if b.quantity > 0 and not b.is_expired()])
        
        stats_label.configure(text=f"Available Medicines: {available}")

    # Bottom buttons frame
    bottom_frame = ctk.CTkFrame(root)
    bottom_frame.pack(fill="x", pady=15, padx=50)

    ctk.CTkLabel(bottom_frame, text="💡 Double-click any medicine to buy", text_color="#888888", font=("Arial", 11)).pack(side="left", padx=10)

    def go_back():
        if on_back:
            on_back()
        else:
            from ui.dashboard import show_dashboard
            show_dashboard(root, user)

    ctk.CTkButton(
        bottom_frame, text="← Back to Dashboard", width=220, height=40,
        fg_color="#555555", hover_color="#666666", font=("Arial", 13, "bold"),
        corner_radius=8, command=go_back
    ).pack(side="right", padx=10)

    # Initial load
    refresh_store()
    update_stats()


def show_my_purchases(root, user, on_back=None):
    """Show consumer's purchase history."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("MediStock Pro – My Purchases")
    ctk.set_appearance_mode("dark")

    # Header
    header_frame = ctk.CTkFrame(root, fg_color="#1f538d")
    header_frame.pack(fill="x", pady=(0, 15))
    ctk.CTkLabel(header_frame, text="📦 My Purchase History", font=("Arial", 28, "bold"), text_color="white").pack(pady=15)

    # Info frame
    info_frame = ctk.CTkFrame(root)
    info_frame.pack(pady=20, padx=50, fill="both", expand=True)

    ctk.CTkLabel(
        info_frame, 
        text="Your purchases will be tracked here.\nCurrent purchases from this session are saved.",
        font=("Arial", 14)
    ).pack(pady=20)

    # Back button frame
    bottom_frame = ctk.CTkFrame(root)
    bottom_frame.pack(fill="x", pady=15, padx=50)

    def go_back():
        if on_back:
            on_back()
        else:
            from ui.dashboard import show_dashboard
            show_dashboard(root, user)

    ctk.CTkButton(
        bottom_frame, text="← Back to Dashboard", width=220, height=40,
        fg_color="#555555", hover_color="#666666", font=("Arial", 13, "bold"),
        corner_radius=8, command=go_back
    ).pack(side="right", padx=10)
