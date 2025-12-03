import customtkinter as ctk
from core.login import LoginManager

def show_login(root, on_success):
    """Login screen with improved UI and error handling."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("MediStock Pro – Login")
    
    # Header
    header_frame = ctk.CTkFrame(root, fg_color="#1f538d")
    header_frame.pack(fill="x", pady=(0, 30))
    ctk.CTkLabel(header_frame, text="🏥 MediStock Pro", font=("Arial", 32, "bold"), text_color="white").pack(pady=20)
    ctk.CTkLabel(header_frame, text="Medical Store Management System", font=("Arial", 14), text_color="#cccccc").pack(pady=(0, 15))

    # Login frame
    frame = ctk.CTkFrame(root)
    frame.pack(pady=40, padx=50, fill="both", expand=True)

    # Username
    ctk.CTkLabel(frame, text="Username:", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=15, padx=20, sticky="w")
    user_entry = ctk.CTkEntry(frame, width=280, height=40, font=("Arial", 13), placeholder_text="Enter username")
    user_entry.grid(row=0, column=1, pady=15, padx=20)
    user_entry.insert(0, "admin")

    # Password
    ctk.CTkLabel(frame, text="Password:", font=("Arial", 14, "bold")).grid(row=1, column=0, pady=15, padx=20, sticky="w")
    pass_entry = ctk.CTkEntry(frame, show="*", width=280, height=40, font=("Arial", 13), placeholder_text="Enter password")
    pass_entry.grid(row=1, column=1, pady=15, padx=20)
    pass_entry.insert(0, "123")

    # Error message label
    error_label = ctk.CTkLabel(frame, text="", text_color="#ff5555", font=("Arial", 12))
    error_label.grid(row=2, column=0, columnspan=2, pady=10)

    def try_login():
        """Validate credentials and proceed to dashboard."""
        username = user_entry.get().strip()
        password = pass_entry.get()
        
        if not username or not password:
            error_label.configure(text="⚠ Username and password are required!")
            return
            
        try:
            login_mgr = LoginManager()
            user = login_mgr.login(username, password)
            if user:
                error_label.configure(text="")
                on_success(user)
            else:
                error_label.configure(text="❌ Invalid username or password!")
        except Exception as e:
            error_label.configure(text=f"❌ Login Error: {str(e)}")

    # Login button
    ctk.CTkButton(
        frame, text="LOGIN", width=280, height=45,
        font=("Arial", 16, "bold"),
        fg_color="#0066cc", hover_color="#004499",
        command=try_login
    ).grid(row=3, column=0, columnspan=2, pady=30)

    # Allow Enter key to submit
    user_entry.bind("<Return>", lambda e: try_login())
    pass_entry.bind("<Return>", lambda e: try_login())

    # Footer
    ctk.CTkLabel(root, text="© 2025 MediStock Pro. All rights reserved.", font=("Arial", 10), text_color="gray").pack(side="bottom", pady=15)