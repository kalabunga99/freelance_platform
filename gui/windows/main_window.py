import customtkinter as ctk
from gui.frames.login_frame import LoginFrame
from gui.frames.register_frame import RegisterFrame
from gui.frames.client_dashboard import ClientDashboard
from gui.frames.freelancer_dashboard import FreelancerDashboard


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Freelance Platform")
        self.geometry("500x600")
        self.resizable(False, False)

        self.current_frame = None
        self.show_login()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginFrame(self, self.show_register, self.show_dashboard)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_register(self):
        self.clear_frame()
        self.current_frame = RegisterFrame(self, self.show_login)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_dashboard(self, user_id, role):
        self.clear_frame()
        self.geometry("850x650")

        if role == "Client":
            self.current_frame = ClientDashboard(self, user_id, self.trigger_logout)
        elif role == "Freelancer":
            self.current_frame = FreelancerDashboard(self, user_id, self.trigger_logout)

        self.current_frame.pack(fill="both", expand=True, padx=0, pady=0)

    def trigger_logout(self):
        self.geometry("500x600")
        self.show_login()
