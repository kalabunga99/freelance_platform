import customtkinter as ctk
from tkinter import messagebox
from gui.frames.post_job_frame import PostJobFrame
from services.job_service import post_new_job


class ClientDashboard(ctk.CTkFrame):
    def __init__(self, master, user_id, logout_cb):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id
        self.logout_cb = logout_cb

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.topbar = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        self.logo_label = ctk.CTkLabel(self.topbar, text="💼 Client Hub", font=("Arial", 18, "bold"))
        self.logo_label.pack(side="left", padx=20, pady=15)

        self.btn_post_job = ctk.CTkButton(self.topbar, text="Post Job", fg_color="transparent",
                                          text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), width=100,
                                          height=35, command=self.load_post_job_form)
        self.btn_post_job.pack(side="left", padx=10)

        self.btn_my_jobs = ctk.CTkButton(self.topbar, text="My Posts", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), width=100,
                                         height=35, command=self.load_main_dashboard)
        self.btn_my_jobs.pack(side="left", padx=10)

        self.btn_profile = ctk.CTkButton(self.topbar, text="Profile", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), width=100,
                                         height=35)
        self.btn_profile.pack(side="left", padx=10)

        self.btn_logout = ctk.CTkButton(self.topbar, text="Logout", fg_color="#E74C3C", hover_color="#C0392B",
                                        text_color="white", width=80, height=30, command=logout_cb)
        self.btn_logout.pack(side="right", padx=20)

        self.content_area = None
        self.load_main_dashboard()

    def clear_content_area(self):
        if self.content_area is not None:
            self.content_area.destroy()

    def load_main_dashboard(self):
        self.clear_content_area()

        self.content_area = ctk.CTkFrame(self, corner_radius=15)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        welcome_label = ctk.CTkLabel(self.content_area, text="Welcome, Client!", font=("Arial", 22, "bold"))
        welcome_label.pack(anchor="w", padx=30, pady=(30, 10))

        sub_label = ctk.CTkLabel(self.content_area, text="Manage your projects and discover top talent.",
                                 font=("Arial", 14), text_color="gray")
        sub_label.pack(anchor="w", padx=30, pady=(0, 20))

        stats_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=10)

        card1 = ctk.CTkFrame(stats_frame, width=150, height=80, corner_radius=10)
        card1.pack(side="left", expand=True, fill="both", padx=(0, 10))
        card1_title = ctk.CTkLabel(card1, text="Active Jobs", font=("Arial", 12), text_color="gray")
        card1_title.pack(pady=(10, 2))
        card1_val = ctk.CTkLabel(card1, text="0", font=("Arial", 20, "bold"))
        card1_val.pack(pady=(0, 10))

        card2 = ctk.CTkFrame(stats_frame, width=150, height=80, corner_radius=10)
        card2.pack(side="left", expand=True, fill="both", padx=10)
        card2_title = ctk.CTkLabel(card2, text="Total Spent", font=("Arial", 12), text_color="gray")
        card2_title.pack(pady=(10, 2))
        card2_val = ctk.CTkLabel(card2, text="$0.00", font=("Arial", 20, "bold"))
        card2_val.pack(pady=(0, 10))

    def load_post_job_form(self):
        self.clear_content_area()
        self.content_area = PostJobFrame(self, self.user_id, self.load_main_dashboard, self.process_job_submission)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def process_job_submission(self, title, description, budget, deadline, seniority):
        if post_new_job(self.user_id, title, description, budget, deadline, seniority):
            messagebox.showinfo("Success", "Job vacancy posted successfully!")
            self.load_main_dashboard()
        else:
            messagebox.showerror("Database Error", "Failed to post the job vacancy. Check your database connection.")
