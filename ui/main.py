import customtkinter as ctk
from ui.login_screen import show_login
from ui.dashboard import show_dashboard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("MediStock Pro")
root.geometry("1000x700")

show_login(root, show_dashboard)

# Create required folders
import os
os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

root.mainloop()