# ui/dashboard.py – IMPROVED & ENHANCED

import customtkinter as ctk
from ui.add_medicine import show_add_medicine
from ui.sell_medicine import show_sell_screen
from ui.view_stock import show_stock_screen
from ui.login_screen import show_login
from ui.consumer_store import show_consumer_store, show_my_purchases


def show_dashboard(root, current_user):
    """Main dashboard with role-based features and improved styling."""
    # Clear window
    for widget in root.winfo_children():
        widget.destroy()

    root.title(f"MediStock Pro – Dashboard ({current_user.role.capitalize()})")

    # Header with background
    header_frame = ctk.CTkFrame(root, fg_color="#1f538d")
    header_frame.pack(fill="x", pady=(0, 30))
    
    ctk.CTkLabel(
        header_frame, text=f"Welcome, {current_user.get_name()}! 👋",
        font=("Arial", 28, "bold"), text_color="white"
    ).pack(pady=(20, 5))

    ctk.CTkLabel(
        header_frame, text=f"Role: {current_user.role.capitalize()} | MediStock Pro",
        font=("Arial", 13), text_color="#cccccc"
    ).pack(pady=(0, 20))

    # Main buttons frame
    btn_frame = ctk.CTkFrame(root)
    btn_frame.pack(pady=20, fill="both", expand=True)

    # Reusable back callback
    back_to_dashboard = lambda: show_dashboard(root, current_user)

    # === MAIN FEATURE BUTTONS - ROLE BASED ===
    if current_user.role.lower() == "consumer":
        # Consumer can buy medicines
        button_config = [
            ("🛒 Browse & Buy Medicines", "#00aa00", "#007700", lambda: show_consumer_store(root, current_user, on_back=back_to_dashboard)),
            ("📦 My Purchases", "#0066cc", "#004499", lambda: show_my_purchases(root, current_user, on_back=back_to_dashboard)),
        ]
    else:
        # Admin/Staff can manage medicines
        button_config = [
            ("➕ Add New Medicine", "#0066cc", "#004499", lambda: show_add_medicine(root, current_user, on_back=back_to_dashboard)),
            ("💊 Sell Medicine", "#00aa00", "#007700", lambda: show_sell_screen(root, current_user, on_back=back_to_dashboard)),
            ("📦 View Stock & Expiry Alert", "#ff8800", "#cc6600", lambda: show_stock_screen(root, current_user, on_back=back_to_dashboard)),
        ]

    for i, (label, fg_color, hover_color, command) in enumerate(button_config):
        ctk.CTkButton(
            btn_frame, text=label, width=360, height=65,
            font=("Arial", 16, "bold"), fg_color=fg_color, hover_color=hover_color,
            command=command, corner_radius=10
        ).pack(pady=15, padx=20)

    # Bottom action buttons frame
    bottom_frame = ctk.CTkFrame(root)
    bottom_frame.pack(fill="x", pady=20, padx=20)

    # Logout Button
    ctk.CTkButton(
        bottom_frame, text="🚪 LOGOUT", width=220, height=50,
        fg_color="#cc0000", hover_color="#aa0000",
        font=("Arial", 15, "bold"), corner_radius=8,
        command=lambda: show_login(root, show_dashboard)
    ).pack(side="right", padx=10)

    # Info label
    ctk.CTkLabel(
        bottom_frame, text="Select an option above to proceed",
        font=("Arial", 12), text_color="#888888"
    ).pack(side="left", padx=10)

    # Footer
    ctk.CTkLabel(
        root, text="MediStock Pro – Pharmacy Management System © 2025",
        font=("Arial", 10), text_color="gray"
    ).pack(side="bottom", pady=12)