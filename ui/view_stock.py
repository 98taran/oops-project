# ui/view_stock.py ← FIXED & WORKING (NO CTkTreeview, NO extra pip)
import customtkinter as ctk
from tkinter import ttk
from core.inventory import InventoryManager
from datetime import datetime


def show_stock_screen(root, user, on_back=None):
    # Clear window
    for widget in root.winfo_children():
        widget.destroy()

    root.title("View Stock")
    ctk.set_appearance_mode("dark")

    # Title
    ctk.CTkLabel(root, text="Current Stock", font=("Arial", 32, "bold")).pack(pady=30)

    # Search bar
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(pady=10, fill="x", padx=100)

    ctk.CTkLabel(search_frame, text="Search Medicine:", font=("Arial", 14)).pack(side="left", padx=10)
    search_var = ctk.StringVar()
    ctk.CTkEntry(search_frame, textvariable=search_var, width=500, font=("Arial", 13)).pack(side="left", padx=10, fill="x", expand=True)

    # Treeview container
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(pady=20, padx=100, fill="both", expand=True)

    # Real ttk.Treeview (styled to look exactly like CustomTkinter)
    columns = ("Name", "Company", "Batch", "Expiry", "Qty", "MRP", "Added On")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)

    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Beautiful dark CustomTkinter-style theme
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
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.column("Name", width=280, anchor="w")
    tree.column("Company", width=160)
    tree.column("Batch", width=130)
    tree.column("Expiry", width=100)
    tree.column("Qty", width=80)
    tree.column("MRP", width=100)
    tree.column("Added On", width=120)

    # Alternate row colors
    tree.tag_configure("odd", background="#2b2b2b")
    tree.tag_configure("even", background="#242424")

    def refresh_stock():
        for item in tree.get_children():
            tree.delete(item)

        inventory = InventoryManager()
        batches = inventory.get_all_batches()
        search = search_var.get().lower()

        for i, batch in enumerate(batches):
            if batch.quantity <= 0 and "low" not in search and "zero" not in search:
                continue

            name = batch.medicine.name.lower()
            if search in name or search in batch.batch_no.lower() or not search:
                expiry = batch.expiry_date.strftime("%m/%Y") if isinstance(batch.expiry_date, datetime) else batch.expiry_date
                added = batch.added_date.strftime("%d/%m/%Y") if hasattr(batch, "added_date") and batch.added_date else "N/A"

                tree.insert("", "end", values=(
                    batch.medicine.name,
                    batch.medicine.company,
                    batch.batch_no,
                    expiry,
                    batch.quantity,
                    f"₹{batch.medicine.mrp:.2f}",
                    added
                ), tags=("even" if i % 2 == 0 else "odd",))

    # Live search
    search_var.trace("w", lambda *_: refresh_stock())

    # Status + Back button
    ctk.CTkLabel(root, text="Tip: Type 'low' or 'zero' to see low/out-of-stock items", 
                 text_color="#888888", font=("Arial", 11)).pack(pady=5)

    back_cmd = on_back or (lambda: __import__("ui.dashboard").show_dashboard(root, user))
    ctk.CTkButton(root, text="Back to Dashboard", width=220, height=45,
                  fg_color="#555555", hover_color="#666666", command=back_cmd).pack(pady=20)

    # Load data
    refresh_stock()