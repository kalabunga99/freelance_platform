import customtkinter as ctk
from tkinter import messagebox
from services.auth_service import login_user


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to_register_cb):
        super().__init__(master)
        self.switch_to_register_cb = switch_to_register_cb

        self.label_title = ctk.CTkLabel(self, text="Welcome Back", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=30)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.entry_password.pack(pady=10)

        self.button_login = ctk.CTkButton(self, text="Login", width=250, command=self.handle_login)
        self.button_login.pack(pady=20)

        self.button_switch = ctk.CTkButton(self, text="Don't have an account? Register", fg_color="transparent",
                                           text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           command=self.switch_to_register_cb)
        self.button_switch.pack(pady=10)

    def handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        success, message = login_user(username, password)

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Login Failed", message)
