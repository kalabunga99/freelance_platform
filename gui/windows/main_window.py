import customtkinter as ctk
from gui.frames.login_frame import LoginFrame
from gui.frames.register_frame import RegisterFrame

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Freelance Platform")
        self.geometry("450x550")
        self.resizable(False, False)

        self.current_frame = None
        self.show_login()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginFrame(self, self.show_register)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_register(self):
        self.clear_frame()
        self.current_frame = RegisterFrame(self, self.show_login)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
