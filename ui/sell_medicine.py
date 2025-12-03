# ui/sell_medicine.py ← IMPROVED WITH EXPIRY CHECKING & BETTER DATA HANDLING
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from core.inventory import InventoryManager
from core.sale import SaleManager
from datetime import datetime


def show_sell_screen(root, user, on_back=None):
    """Sell Medicine screen with expiry checking, improved UI and navigation."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("MediStock Pro – Sell Medicine")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Header
    header_frame = ctk.CTkFrame(root, fg_color="#1f538d")
    header_frame.pack(fill="x", pady=(0, 15))
    ctk.CTkLabel(header_frame, text="💊 Sell Medicine", font=("Arial", 28, "bold"), text_color="white").pack(pady=15)

    # Search bar
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(pady=10, fill="x", padx=50)

    ctk.CTkLabel(search_frame, text="Search by Name/Batch:", font=("Arial", 14)).pack(side="left", padx=10)
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, width=400, font=("Arial", 13))
    search_entry.pack(side="left", padx=10, fill="x", expand=True)

    # Treeview container
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(pady=20, padx=50, fill="both", expand=True)

    # ttk.Treeview + scrollbar
    columns = ("Name", "Company", "Batch", "Expiry", "Status", "Qty", "MRP", "Action")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Perfect CustomTkinter-like dark style
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    rowheight=40,
                    fieldbackground="#2b2b2b",
                    borderwidth=0,
                    font=("Arial", 12))
    
    style.configure("Treeview.Heading",
                    background="#1f538d",
                    foreground="white",
                    font=("Arial", 12, "bold"),
                    relief="flat")
    
    style.map("Treeview", background=[("selected", "#3475aa")])
    style.map("Treeview.Heading", background=[("active", "#1f6aa5")])

    # Column configuration
    tree.heading("Name", text="Medicine Name")
    tree.heading("Company", text="Company")
    tree.heading("Batch", text="Batch")
    tree.heading("Expiry", text="Expiry")
    tree.heading("Status", text="Status")
    tree.heading("Qty", text="Qty")
    tree.heading("MRP", text="MRP")
    tree.heading("Action", text="Action")

    tree.column("Name", width=200, anchor="w")
    tree.column("Company", width=130)
    tree.column("Batch", width=110)
    tree.column("Expiry", width=90)
    tree.column("Status", width=100)
    tree.column("Qty", width=70)
    tree.column("MRP", width=90)
    tree.column("Action", width=90)

    # Alternate row colors + status colors
    tree.tag_configure("oddrow", background="#2b2b2b")
    tree.tag_configure("evenrow", background="#242424")
    tree.tag_configure("expired", foreground="#ff4444")  # Red
    tree.tag_configure("near_expiry", foreground="#ffaa00")  # Orange
    tree.tag_configure("ok", foreground="#00ff00")  # Green

    def refresh_stock():
        """Load medicines and display (excluding expired ones)"""
        tree.delete(*tree.get_children())

        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        search = search_var.get().lower()

        for i, batch in enumerate(all_batches):
            if batch.quantity <= 0:
                continue
            
            # Skip expired batches but show near-expiry warning
            if batch.is_expired():
                continue

            name = batch.medicine.name.lower()
            if search in name or search in batch.batch_no.lower() or search == "":
                expiry = batch.expiry_date if isinstance(batch.expiry_date, str) else batch.expiry_date.strftime("%m/%Y")
                status_text, _ = batch.get_status()
                
                # Determine row tag
                row_tag = ("evenrow" if i % 2 else "oddrow")
                if batch.is_expired():
                    row_tag = ("evenrow" if i % 2 else "oddrow", "expired")
                elif batch.is_near_expiry():
                    row_tag = ("evenrow" if i % 2 else "oddrow", "near_expiry")
                else:
                    row_tag = ("evenrow" if i % 2 else "oddrow", "ok")

                tree.insert("", "end", values=(
                    batch.medicine.name,
                    batch.medicine.company,
                    batch.batch_no,
                    expiry,
                    status_text,
                    batch.quantity,
                    f"₹{batch.medicine.mrp:.2f}",
                    "SELL"
                ), tags=(batch.batch_no,) + row_tag)

    search_var.trace("w", lambda *_: refresh_stock())

    # Sell popup
    def sell_batch(event=None):
        sel = tree.selection()
        if not sel:
            return
        item = tree.item(sel[0])
        batch_no = item["tags"][0] if item["tags"] else None
        if not batch_no:
            return

        batch = next((b for b in InventoryManager().get_all_batches() if b.batch_no == batch_no), None)
        if not batch or batch.quantity == 0:
            return

        # Check if expired
        if batch.is_expired():
            error_popup = ctk.CTkToplevel(root)
            error_popup.title("❌ Cannot Sell")
            error_popup.geometry("300x150")
            error_popup.grab_set()
            ctk.CTkLabel(error_popup, text="❌ This medicine is expired!", font=("Arial", 14, "bold"), text_color="red").pack(pady=20)
            ctk.CTkLabel(error_popup, text="It cannot be sold.", font=("Arial", 12)).pack(pady=5)
            ctk.CTkButton(error_popup, text="OK", command=error_popup.destroy).pack(pady=10)
            return

        popup = ctk.CTkToplevel(root)
        popup.title("Sell Medicine")
        popup.geometry("380x300")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text=batch.medicine.name, font=("Arial", 20, "bold")).pack(pady=(20, 5))
        
        status_text, _ = batch.get_status()
        ctk.CTkLabel(popup, text=f"Batch: {batch.batch_no} | Stock: {batch.quantity} | Status: {status_text}", font=("Arial", 11)).pack(pady=5)
        ctk.CTkLabel(popup, text=f"Expiry: {batch.expiry_date}", font=("Arial", 11)).pack(pady=5)
        ctk.CTkLabel(popup, text=f"MRP: ₹{batch.medicine.mrp:.2f}", font=("Arial", 11)).pack(pady=5)

        ctk.CTkLabel(popup, text="Quantity to Sell:", font=("Arial", 13)).pack(pady=(15, 5))
        qty_var = ctk.StringVar(value="1")
        qty_entry = ctk.CTkEntry(popup, textvariable=qty_var, width=100, font=("Arial", 14), justify="center")
        qty_entry.pack()
        qty_entry.focus_force()

        msg_label = ctk.CTkLabel(popup, text="", text_color="red")
        msg_label.pack(pady=8)

        def confirm():
            try:
                qty = int(qty_var.get())
                if qty <= 0:
                    raise ValueError("❌ Enter positive quantity")
                if qty > batch.quantity:
                    raise ValueError(f"❌ Only {batch.quantity} available!")
                if batch.is_expired():
                    raise ValueError("❌ Cannot sell expired medicine!")
                    
                SaleManager().sell_batch(batch, qty)
                msg_label.configure(text=f"✅ Sold {qty} items!", text_color="lightgreen")
                refresh_stock()
                popup.after(1000, popup.destroy)
            except ValueError as e:
                msg_label.configure(text=str(e), text_color="red")

        ctk.CTkButton(popup, text="Confirm Sale", fg_color="green", height=40, command=confirm).pack(pady=15)
        popup.bind("<Return>", lambda e: confirm())

    tree.bind("<Double-1>", sell_batch)

    # Stats frame
    stats_frame = ctk.CTkFrame(root, fg_color="#242424")
    stats_frame.pack(fill="x", pady=10, padx=50)

    stats_label = ctk.CTkLabel(stats_frame, text="", font=("Arial", 11), text_color="#aaaaaa")
    stats_label.pack(side="left", padx=10, pady=8)

    def update_stats():
        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        available = len([b for b in all_batches if b.quantity > 0 and not b.is_expired()])
        near_exp = len([b for b in all_batches if b.is_near_expiry()])
        expired = len(inventory.get_expired_batches())
        
        stats_label.configure(
            text=f"📊 Available: {available} | Near Expiry: {near_exp} | Expired: {expired}"
        )

    # Status + Back button frame
    bottom_frame = ctk.CTkFrame(root)
    bottom_frame.pack(fill="x", pady=15, padx=50)

    ctk.CTkLabel(bottom_frame, text="💡 Double-click any row to sell", text_color="#888888", font=("Arial", 11)).pack(side="left", padx=10)
    
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
    refresh_stock()
    update_stats()

    # Sell popup
    def sell_batch(event=None):
        sel = tree.selection()
        if not sel:
            return
        item = tree.item(sel[0])
        batch_no = item["tags"][0] if item["tags"] else None
        if not batch_no:
            return

        batch = next((b for b in InventoryManager().get_all_batches() if b.batch_no == batch_no), None)
        if not batch or batch.quantity == 0:
            return

        popup = ctk.CTkToplevel(root)
        popup.title("Sell Medicine")
        popup.geometry("380x280")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text=batch.medicine.name, font=("Arial", 20, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(popup, text=f"Batch: {batch.batch_no} | Stock: {batch.quantity}", font=("Arial", 11)).pack(pady=5)
        ctk.CTkLabel(popup, text=f"MRP: ₹{batch.medicine.mrp:.2f}", font=("Arial", 11)).pack(pady=5)

        ctk.CTkLabel(popup, text="Quantity:", font=("Arial", 13)).pack(pady=(15, 5))
        qty_var = ctk.StringVar(value="1")
        qty_entry = ctk.CTkEntry(popup, textvariable=qty_var, width=80, font=("Arial", 14), justify="center")
        qty_entry.pack()
        qty_entry.focus_force()

        msg_label = ctk.CTkLabel(popup, text="", text_color="red")
        msg_label.pack(pady=8)

        def confirm():
            try:
                qty = int(qty_var.get())
                if qty <= 0:
                    raise ValueError("Enter positive quantity")
                if qty > batch.quantity:
                    raise ValueError(f"Only {batch.quantity} available!")
                SaleManager().sell_batch(batch, qty)
                msg_label.configure(text=f"Sold {qty} items!", text_color="lightgreen")
                refresh_stock()
                popup.after(1000, popup.destroy)
            except ValueError as e:
                msg_label.configure(text=str(e))

        ctk.CTkButton(popup, text="Confirm Sale", fg_color="green", height=40, command=confirm).pack(pady=15)
        popup.bind("<Return>", lambda e: confirm())

    tree.bind("<Double-1>", sell_batch)

    # Status + Back button frame
    bottom_frame = ctk.CTkFrame(root)
    bottom_frame.pack(fill="x", pady=15, padx=20)

    ctk.CTkLabel(bottom_frame, text="💡 Double-click any row to sell", text_color="#888888", font=("Arial", 11)).pack(side="left", padx=10)
    
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
    refresh_stock()