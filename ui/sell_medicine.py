# ui/sell_medicine.py ← FINAL VERSION – NO EXTRA DEPENDENCIES
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from core.inventory import InventoryManager
from core.sale import SaleManager
from datetime import datetime


def show_sell_screen(root, user, on_back=None):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Sell Medicine")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Title
    ctk.CTkLabel(root, text="Sell Medicine", font=("Arial", 32, "bold")).pack(pady=30)

    # Search bar
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(pady=10, fill="x", padx=100)

    ctk.CTkLabel(search_frame, text="Search by Name/Batch:", font=("Arial", 14)).pack(side="left", padx=10)
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, width=500, font=("Arial", 13))
    search_entry.pack(side="left", padx=10, fill="x", expand=True)

    # Treeview container
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(pady=20, padx=100, fill="both", expand=True)

    # ttk.Treeview + scrollbar
    columns = ("Name", "Company", "Batch", "Expiry", "Qty", "MRP", "Action")
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
    tree.heading("Qty", text="Qty")
    tree.heading("MRP", text="MRP")
    tree.heading("Action", text="Action")

    tree.column("Name", width=250, anchor="w")
    tree.column("Company", width=150, anchor="center")
    tree.column("Batch", width=120, anchor="center")
    tree.column("Expiry", width=100, anchor="center")
    tree.column("Qty", width=80, anchor="center")
    tree.column("MRP", width=100, anchor="center")
    tree.column("Action", width=100, anchor="center")

    # Alternate row colors
    tree.tag_configure("oddrow", background="#2b2b2b")
    tree.tag_configure("evenrow", background="#242424")

    def refresh_stock():
        for item in tree.get_children():
            tree.delete(item)

        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        search = search_var.get().lower()

        for i, batch in enumerate(all_batches):
            if batch.quantity <= 0:
                continue
            name = batch.medicine.name.lower()
            if search in name or search in batch.batch_no.lower() or search == "":
                expiry = batch.expiry_date.strftime("%m/%Y") if isinstance(batch.expiry_date, datetime) else batch.expiry_date
                tree.insert("", "end", values=(
                    batch.medicine.name,
                    batch.medicine.company,
                    batch.batch_no,
                    expiry,
                    batch.quantity,
                    f"₹{batch.medicine.mrp:.2f}",
                    "SELL"
                ), tags=(batch.batch_no, "oddrow" if i % 2 else "evenrow"))

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

    # Status + Back button
    ctk.CTkLabel(root, text="Double-click any row to sell", text_color="#888888").pack(pady=5)
    back_cmd = on_back or (lambda: __import__("ui.dashboard").show_dashboard(root, user))
    ctk.CTkButton(root, text="Back to Dashboard", width=220, height=45,
                  fg_color="#555555", hover_color="#666666", command=back_cmd).pack(pady=20)

    # Initial load
    refresh_stock()