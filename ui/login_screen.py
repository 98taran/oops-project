import customtkinter as ctk
from core.login import LoginManager

def show_login(root, on_success):
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(root, text="MediStock Pro", font=("Arial", 30, "bold")).pack(pady=40)
    ctk.CTkLabel(root, text="Medical Store Management", font=("Arial", 16)).pack(pady=10)

    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=50, ipadx=20, ipady=20)

    ctk.CTkLabel(frame, text="Username:").grid(row=0, column=0, pady=10, padx=10)
    user_entry = ctk.CTkEntry(frame, width=200)
    user_entry.grid(row=0, column=1, pady=10, padx=10)
    user_entry.insert(0, "admin")          # default for testing

    ctk.CTkLabel(frame, text="Password:").grid(row=1, column=0, pady=10, padx=10)
    pass_entry = ctk.CTkEntry(frame, show="*", width=200)
    pass_entry.grid(row=1, column=1, pady=10, padx=10)
    pass_entry.insert(0, "123")            # default password

    def try_login():
        login_mgr = LoginManager()
        user = login_mgr.login(user_entry.get(), pass_entry.get())
        if user:
            on_success(user)               # go to dashboard
        else:
            ctk.CTkLabel(frame, text="Wrong username/password!", text_color="red").grid(row=3, column=0, columnspan=2, pady=10)

    ctk.CTkButton(root, text="LOGIN", width=200, height=40, command=try_login).pack(pady=30)