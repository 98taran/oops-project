# ui/sell_medicine.py ← FINAL 100% WORKING VERSION (supports dict or Batch objects)
import customtkinter as ctk
from tkinter import ttk
from core.inventory import InventoryManager
from core.sale import SaleManager
from datetime import datetime


def show_sell_screen(root, user, on_back=None):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Sell Medicine")
    ctk.set_appearance_mode("dark")

    # Title
    ctk.CTkLabel(root, text="Sell Medicine", font=("Arial", 32, "bold")).pack(pady=30)

    # Search
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(pady=10, fill="x", padx=100)
    ctk.CTkLabel(search_frame, text="Search by Name/Batch:", font=("Arial", 14)).pack(side="left", padx=10)
    search_var = ctk.StringVar()
    ctk.CTkEntry(search_frame, textvariable=search_var, width=500, font=("Arial", 13)).pack(side="left", padx=10, fill="x", expand=True)

    # Treeview frame
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(pady=20, padx=100, fill="both", expand=True)

    columns = ("Name", "Company", "Batch", "Expiry", "Qty", "MRP", "Action")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Style (perfect dark CTk look)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=40,
                    fieldbackground="#2b2b2b", font=("Arial", 12))
    style.configure("Treeview.Heading", background="#1f538d", foreground="white", font=("Arial", 12, "bold"))
    style.map("Treeview", background=[("selected", "#3475aa")])
    tree.tag_configure("odd", background="#2b2b2b")
    tree.tag_configure("even", background="#242424")

    # Columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.column("Name", width=250, anchor="w")
    tree.column("Company", width=150)
    tree.column("Batch", width=120)
    tree.column("Expiry", width=100)
    tree.column("Qty", width=80)
    tree.column("MRP", width=100)
    tree.column("Action", width=100)

    def get_batch_data(batch):
        """Safely extract data whether batch is object or dict"""
        if hasattr(batch, 'medicine'):  # Real Batch object
            med = batch.medicine
            qty = batch.quantity
            batch_no = batch.batch_no
            expiry = batch.expiry_date
        else:  # dict from JSON
            med = batch['medicine']
            qty = batch['quantity']
            batch_no = batch['batch_no']
            expiry = batch.get('expiry_date', 'N/A')
            # Convert string date back to datetime if needed
            if isinstance(expiry, str):
                try:
                    expiry = datetime.strptime(expiry, "%Y-%m-%d")
                except:
                    pass
        return med, qty, batch_no, expiry

    def refresh_stock():
        for item in tree.get_children():
            tree.delete(item)

        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        search = search_var.get().lower()

        for i, batch in enumerate(all_batches):
            try:
                med, qty, batch_no, expiry = get_batch_data(batch)
                if qty <= 0:
                    continue

                name = med.name.lower() if hasattr(med, 'name') else str(med.get('name', '')).lower()
                if search in name or search in batch_no.lower() or not search:
                    expiry_str = expiry.strftime("%m/%Y") if isinstance(expiry, datetime) else str(expiry)[:7]
                    mrp = med.mrp if hasattr(med, 'mrp') else med.get('mrp', 0)

                    tree.insert("", "end", values=(
                        med.name if hasattr(med, 'name') else med.get('name', 'Unknown'),
                        med.company if hasattr(med, 'company') else med.get('company', 'Unknown'),
                        batch_no,
                        expiry_str,
                        qty,
                        f"₹{mrp:.2f}",
                        "SELL"
                    ), tags=(batch_no, "even" if i % 2 == 0 else "odd"))
            except Exception as e:
                print(f"Error loading batch: {e}")

    search_var.trace("w", lambda *_: refresh_stock())

    def sell_batch(event=None):
        sel = tree.selection()
        if not sel:
            return
        batch_no = tree.item(sel[0])["tags"][0]

        # Find the batch (object or dict)
        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        batch = next((b for b in all_batches if 
                     (hasattr(b, 'batch_no') and b.batch_no == batch_no) or 
                     (isinstance(b, dict) and b.get('batch_no') == batch_no)), None)
        if not batch:
            return

        med, qty, batch_no, _ = get_batch_data(batch)

        popup = ctk.CTkToplevel(root)
        popup.title("Sell Medicine")
        popup.geometry("380x280")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text=med.name if hasattr(med, 'name') else med.get('name'), 
                     font=("Arial", 20, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(popup, text=f"Batch: {batch_no} | Stock: {qty}").pack(pady=5)

        ctk.CTkLabel(popup, text="Quantity:", font=("Arial", 13)).pack(pady=(15, 5))
        qty_var = ctk.StringVar(value="1")
        qty_entry = ctk.CTkEntry(popup, textvariable=qty_var, width=80, font=("Arial", 14), justify="center")
        qty_entry.pack()
        qty_entry.focus_force()

        msg = ctk.CTkLabel(popup, text="", text_color="red")
        msg.pack(pady=8)

        def confirm():
            try:
                q = int(qty_var.get())
                if q <= 0 or q > qty:
                    raise ValueError(f"Invalid quantity! Max: {qty}")
                SaleManager().sell_batch(batch, q)  # Works with dict or object
                msg.configure(text=f"Sold {q} items!", text_color="lightgreen")
                refresh_stock()
                popup.after(1000, popup.destroy)
            except Exception as e:
                msg.configure(text=str(e))

        ctk.CTkButton(popup, text="Confirm Sale", fg_color="green", height=40, command=confirm).pack(pady=15)
        popup.bind("<Return>", lambda e: confirm())

    tree.bind("<Double-1>", sell_batch)

    ctk.CTkLabel(root, text="Double-click a row to sell", text_color="#888888").pack(pady=5)
    back_cmd = on_back or (lambda: __import__("ui.dashboard").show_dashboard(root, user))
    ctk.CTkButton(root, text="Back to Dashboard", width=220, height=45,
                  fg_color="#555555", hover_color="#666666", command=back_cmd).pack(pady=20)

    refresh_stock()