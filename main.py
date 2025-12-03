# main.py ← FINAL WORKING VERSION

import customtkinter as ctk
import os

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("MediStock Pro – Medical Store Management")
root.geometry("1200x800")
# root.state('zoomed')  # optional: full screen

# Import screens
from ui.login_screen import show_login
from ui.dashboard import show_dashboard

# ←←← THIS IS THE FIX ←←←
def go_to_dashboard(current_user):
    show_dashboard(root, current_user)   # pass both root and the logged-in user

# Start app
show_login(root, go_to_dashboard)   # pass the wrapper function

root.mainloop()