import customtkinter as ctk
from tkinter import messagebox
from repositories.user_repository import add_user
from models.client import Client
from models.freelancer import Freelancer
from services.auth_service import hash_password


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to_login_cb):
        super().__init__(master)
        self.switch_to_login_cb = switch_to_login_cb

        self.label_title = ctk.CTkLabel(self, text="Create Account", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.entry_username.pack(pady=8)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email", width=250)
        self.entry_email.pack(pady=8)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.entry_password.pack(pady=8)

        self.role_menu = ctk.CTkOptionMenu(self, values=["Freelancer", "Client"], width=250,
                                           command=self.update_role_placeholder)
        self.role_menu.pack(pady=8)

        self.entry_extra = ctk.CTkEntry(self, placeholder_text="Full Name", width=250)
        self.entry_extra.pack(pady=8)

        self.button_register = ctk.CTkButton(self, text="Register", width=250, command=self.handle_register)
        self.button_register.pack(pady=20)

        self.button_switch = ctk.CTkButton(self, text="Already have an account? Login", fg_color="transparent",
                                           text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           command=self.switch_to_login_cb)
        self.button_switch.pack(pady=5)

    def update_role_placeholder(self, choice):
        if choice == "Freelancer":
            self.entry_extra.configure(placeholder_text="Full Name")
        else:
            self.entry_extra.configure(placeholder_text="Company Name")

    def handle_register(self):
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        role = self.role_menu.get()
        extra_info = self.entry_extra.get().strip()

        if not username or not email or not password or not extra_info:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        pwd_hash = hash_password(password)

        if role == "Freelancer":
            new_user = Freelancer(None, username, pwd_hash, email, extra_info)
        else:
            new_user = Client(None, username, pwd_hash, email, extra_info)

        if add_user(new_user):
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.switch_to_login_cb()
        else:
            messagebox.showerror("Error", "Registration failed. Username or email might be taken.")
