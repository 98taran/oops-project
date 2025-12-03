# ui/dashboard.py ← ULTIMATE FINAL VERSION (Perfect & Bug-Free)

import customtkinter as ctk
from ui.add_medicine import show_add_medicine
from ui.sell_medicine import show_sell_screen
from ui.view_stock import show_stock_screen
from ui.login_screen import show_login


def show_dashboard(root, current_user):
    # Clear window
    for widget in root.winfo_children():
        widget.destroy()

    root.title(f"MediStock Pro – Dashboard ({current_user.role.capitalize()})")

    # Header
    ctk.CTkLabel(root, text=f"Welcome, {current_user.get_name()}!",
                 font=("Arial", 32, "bold")).pack(pady=40)

    ctk.CTkLabel(root, text=f"Role: {current_user.role.capitalize()}",
                 font=("Arial", 18), text_color="#aaaaaa").pack(pady=5)

    # Main buttons frame
    btn_frame = ctk.CTkFrame(root)
    btn_frame.pack(pady=30)

    # Reusable back callback
    back_to_dashboard = lambda: show_dashboard(root, current_user)

    # === BUTTONS ===
    ctk.CTkButton(
        btn_frame, text="Add New Medicine", width=340, height=70,
        font=("Arial", 18, "bold"), fg_color="#0066cc", hover_color="#004499",
        command=lambda: show_add_medicine(root, current_user, on_back=back_to_dashboard)
    ).grid(row=0, column=0, pady=18, padx=40)

    ctk.CTkButton(
        btn_frame, text="Sell Medicine", width=340, height=70,
        font=("Arial", 18, "bold"), fg_color="#00aa00", hover_color="#007700",
        command=lambda: show_sell_screen(root, current_user, on_back=back_to_dashboard)
    ).grid(row=1, column=0, pady=18, padx=40)

    ctk.CTkButton(
        btn_frame, text="View Stock & Expiry Alert", width=340, height=70,
        font=("Arial", 18, "bold"), fg_color="#ff8800", hover_color="#cc6600",
        command=lambda: show_stock_screen(root, current_user, on_back=back_to_dashboard)
    ).grid(row=2, column=0, pady=18, padx=40)

    # Logout Button
    ctk.CTkButton(
        root, text="LOGOUT", width=220, height=55,
        fg_color="#cc0000", hover_color="#aa0000",
        font=("Arial", 18, "bold"),
        command=lambda: show_login(root, show_dashboard)
    ).pack(pady=50)

    # Footer
    ctk.CTkLabel(
        root, text="MediStock Pro – Pharmacy Management System © 2025",
        font=("Arial", 11), text_color="gray"
    ).pack(side="bottom", pady=15)