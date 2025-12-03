# ui/view_stock.py ← IMPROVED WITH EXPIRY STATUS & BETTER DATA HANDLING
import customtkinter as ctk
from tkinter import ttk
from core.inventory import InventoryManager
from datetime import datetime


def show_stock_screen(root, user, on_back=None):
    """View Stock screen with enhanced UI, expiry status, and navigation."""
    # Clear window
    for widget in root.winfo_children():
        widget.destroy()

    root.title("MediStock Pro – View Stock & Inventory")
    ctk.set_appearance_mode("dark")

    # Header
    header_frame = ctk.CTkFrame(root, fg_color="#1f538d")
    header_frame.pack(fill="x", pady=(0, 15))
    ctk.CTkLabel(header_frame, text="📦 Current Stock & Inventory", font=("Arial", 28, "bold"), text_color="white").pack(pady=15)

    # Search and filter bar
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(pady=10, fill="x", padx=50)

    ctk.CTkLabel(search_frame, text="Search Medicine:", font=("Arial", 14)).pack(side="left", padx=10)
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, width=400, font=("Arial", 13))
    search_entry.pack(side="left", padx=10, fill="x", expand=True)

    # Filter buttons
    filter_var = ctk.StringVar(value="all")
    
    ctk.CTkLabel(search_frame, text="Filter:", font=("Arial", 14)).pack(side="left", padx=(20, 10))
    
    ctk.CTkRadioButton(search_frame, text="All", variable=filter_var, value="all", command=lambda: refresh_stock()).pack(side="left", padx=5)
    ctk.CTkRadioButton(search_frame, text="Near Expiry", variable=filter_var, value="near_expiry", command=lambda: refresh_stock()).pack(side="left", padx=5)
    ctk.CTkRadioButton(search_frame, text="Expired", variable=filter_var, value="expired", command=lambda: refresh_stock()).pack(side="left", padx=5)
    ctk.CTkRadioButton(search_frame, text="Low Stock", variable=filter_var, value="low_stock", command=lambda: refresh_stock()).pack(side="left", padx=5)

    # Treeview container
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(pady=20, padx=50, fill="both", expand=True)

    # Real ttk.Treeview (styled to look exactly like CustomTkinter)
    columns = ("Name", "Company", "Batch", "Expiry", "Status", "Qty", "MRP", "Added On")
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
                    font=("Arial", 11))
    style.configure("Treeview.Heading",
                    background="#1f538d",
                    foreground="white",
                    font=("Arial", 12, "bold"))
    style.map("Treeview", background=[("selected", "#3475aa")])

    # Column setup
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.column("Name", width=220, anchor="w")
    tree.column("Company", width=140)
    tree.column("Batch", width=110)
    tree.column("Expiry", width=90)
    tree.column("Status", width=110)
    tree.column("Qty", width=70)
    tree.column("MRP", width=90)
    tree.column("Added On", width=110)

    # Alternate row colors + status colors with BACKGROUND
    tree.tag_configure("odd", background="#2b2b2b", foreground="white")
    tree.tag_configure("even", background="#242424", foreground="white")
    tree.tag_configure("expired", background="#3d1f1f", foreground="#ff4444")  # Dark red background + red text
    tree.tag_configure("near_expiry", background="#3d3d1f", foreground="#ffaa00")  # Dark yellow background + orange text
    tree.tag_configure("low_stock", background="#3d3d1f", foreground="#ffff00")  # Dark yellow background + yellow text

    def refresh_stock():
        """Load and display inventory with filtering"""
        tree.delete(*tree.get_children())

        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        search = search_var.get().lower()
        filter_type = filter_var.get()

        for i, batch in enumerate(all_batches):
            # Apply filter
            if filter_type == "expired" and not batch.is_expired():
                continue
            if filter_type == "near_expiry" and not batch.is_near_expiry():
                continue
            if filter_type == "low_stock" and batch.quantity > 10:
                continue

            # Apply search
            name = batch.medicine.name.lower()
            if search and search not in name and search not in batch.batch_no.lower():
                continue

            # Get expiry status
            status_text, status_color = batch.get_status()
            
            # Format dates
            expiry = batch.expiry_date if isinstance(batch.expiry_date, str) else batch.expiry_date.strftime("%m/%Y")
            added = batch.added_date if isinstance(batch.added_date, str) else batch.added_date.strftime("%d/%m/%Y")

            # Determine tag for coloring
            row_tag = ("even" if i % 2 == 0 else "odd")
            if batch.is_expired():
                row_tag = ("even" if i % 2 == 0 else "odd", "expired")
            elif batch.is_near_expiry():
                row_tag = ("even" if i % 2 == 0 else "odd", "near_expiry")
            elif batch.quantity <= 10:
                row_tag = ("even" if i % 2 == 0 else "odd", "low_stock")

            tree.insert("", "end", values=(
                batch.medicine.name,
                batch.medicine.company,
                batch.batch_no,
                expiry,
                status_text,
                batch.quantity,
                f"₹{batch.medicine.mrp:.2f}",
                added
            ), tags=row_tag)

    # Live search
    search_var.trace("w", lambda *_: refresh_stock())

    # Stats frame
    stats_frame = ctk.CTkFrame(root, fg_color="#242424")
    stats_frame.pack(fill="x", pady=10, padx=50)

    stats_label = ctk.CTkLabel(stats_frame, text="", font=("Arial", 11), text_color="#aaaaaa")
    stats_label.pack(side="left", padx=10, pady=8)

    def update_stats():
        inventory = InventoryManager()
        all_batches = inventory.get_all_batches()
        expired = len(inventory.get_expired_batches())
        near_exp = len(inventory.get_near_expiry())
        low_stock = len(inventory.get_low_stock())
        total_qty = sum(b.quantity for b in all_batches)
        
        stats_label.configure(
            text=f"📊 Total Items: {len(all_batches)} | Total Qty: {total_qty} | Expired: {expired} | Near Expiry: {near_exp} | Low Stock: {low_stock}"
        )

    # Status + Back button frame
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

    # Initial load
    refresh_stock()
    update_stats()