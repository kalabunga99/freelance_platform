import customtkinter as ctk
from tkinter import messagebox
from gui.frames.post_job_frame import PostJobFrame
from gui.frames.my_jobs_frame import MyJobsFrame
from gui.frames.profile_frame import ProfileFrame
from gui.frames.app_frame import ApplicationsFrame
from gui.frames.inbox_frame import InboxFrame
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
                                         height=35, command=self.load_my_jobs_list)
        self.btn_my_jobs.pack(side="left", padx=10)

        self.btn_inbox = ctk.CTkButton(self.topbar, text="Messages", fg_color="transparent",
                                       text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), width=100,
                                       height=35, command=self.load_inbox_screen)
        self.btn_inbox.pack(side="left", padx=10)

        self.btn_profile = ctk.CTkButton(self.topbar, text="Profile", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), width=100,
                                         height=35, command=self.load_profile_screen)
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
        from services.analytics_service import get_client_dashboard_stats, get_platform_statistics_service

        try:
            my_stats = get_client_dashboard_stats(self.user_id)
            global_stats = get_platform_statistics_service()
        except Exception as e:
            print(f"Error loading stats: {e}")
            my_stats = {'total_posts': 0, 'hire_success_rate': 0.0, 'total_spent': 0.00}
            global_stats = {'total_jobs': 0, 'hire_success_rate': 0.0, 'avg_fill_time_days': 0.0, 'top_skills': [],
                            'monthly_revenue': 0.00, 'top_freelancers': []}

        self.content_area = ctk.CTkFrame(self, corner_radius=15)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        welcome_label = ctk.CTkLabel(self.content_area, text="Welcome, Client!", font=("Arial", 22, "bold"))
        welcome_label.pack(anchor="w", padx=30, pady=(25, 5))

        sub_label = ctk.CTkLabel(self.content_area, text="Manage your projects and discover top talent.",
                                 font=("Arial", 14), text_color="gray")
        sub_label.pack(anchor="w", padx=30, pady=(0, 15))

        stats_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        stats_frame.pack(fill="x", padx=25, pady=5)

        card1 = ctk.CTkFrame(stats_frame, width=220, height=85, corner_radius=10)
        card1.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(card1, text="My Total Job Posts", font=("Arial", 12), text_color="gray").pack(pady=(12, 2))
        ctk.CTkLabel(card1, text=str(my_stats.get('total_posts', 0)), font=("Arial", 20, "bold")).pack()

        card2 = ctk.CTkFrame(stats_frame, width=220, height=85, corner_radius=10)
        card2.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(card2, text="My Hire Success Rate", font=("Arial", 12), text_color="gray").pack(pady=(12, 2))
        ctk.CTkLabel(card2, text=f"{my_stats.get('hire_success_rate', 0.0)}%", font=("Arial", 20, "bold"),
                     text_color="#2ECC71").pack()

        card3 = ctk.CTkFrame(stats_frame, width=220, height=85, corner_radius=10)
        card3.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(card3, text="Platform Avg Fill Duration", font=("Arial", 12), text_color="gray").pack(pady=(12, 2))
        ctk.CTkLabel(card3, text=f"{global_stats.get('avg_fill_time_days', 0.0)} Days", font=("Arial", 20, "bold"),
                     text_color="#3498DB").pack()

        card4 = ctk.CTkFrame(self.content_area, corner_radius=10, height=70)
        card4.pack(fill="x", pady=15, padx=30)
        ctk.CTkLabel(card4, text="Total Budget Invested", font=("Arial", 12), text_color="gray").pack(pady=(8, 1))
        ctk.CTkLabel(card4, text=f"${my_stats.get('total_spent', 0.00):.2f}", font=("Arial", 22, "bold"),
                     text_color="#E67E22").pack(pady=(0, 8))

        skills_box = ctk.CTkFrame(self.content_area, corner_radius=10)
        skills_box.pack(fill="x", padx=30, pady=(5, 20))
        ctk.CTkLabel(skills_box, text="🔥 Most Demanded Market Skills", font=("Arial", 13, "bold")).pack(pady=(8, 10))

        skills_list = global_stats.get('top_skills', [])
        if not skills_list:
            ctk.CTkLabel(skills_box, text="No metrics recorded yet.", font=("Arial", 12, "italic"),
                         text_color="gray").pack(pady=10)
        else:
            max_count = max([s['skill_count'] for s in skills_list]) if skills_list else 1
            for s in skills_list:
                row = ctk.CTkFrame(skills_box, fg_color="transparent")
                row.pack(fill="x", padx=30, pady=4)

                lbl_name = ctk.CTkLabel(row, text=s['skill_name'], font=("Arial", 12), width=180, anchor="w")
                lbl_name.pack(side="left")

                progress_val = s['skill_count'] / max_count
                progress = ctk.CTkProgressBar(row, width=280, height=8, fg_color="gray30", progress_color="#3498DB")
                progress.pack(side="left", padx=10, pady=8)
                progress.set(progress_val)

                lbl_count = ctk.CTkLabel(row, text=f"{s['skill_count']} jobs", font=("Arial", 11), text_color="gray")
                lbl_count.pack(side="right")

    def load_post_job_form(self):
        self.clear_content_area()
        self.content_area = PostJobFrame(self, self.user_id, self.load_main_dashboard, self.process_job_submission)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_my_jobs_list(self):
        self.clear_content_area()
        self.content_area = MyJobsFrame(self, self.user_id, self.load_main_dashboard)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_profile_screen(self):
        self.clear_content_area()
        self.content_area = ProfileFrame(self, self.user_id, self.load_main_dashboard)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_job_applications(self, job_id):
        self.clear_content_area()
        self.content_area = ApplicationsFrame(self, job_id, self.load_my_jobs_list)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_inbox_screen(self):
        self.clear_content_area()
        self.content_area = InboxFrame(self, self.user_id, self.load_chat_screen, self.load_main_dashboard)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_chat_screen(self, thread_id, participant_username, participant_id):
        self.clear_content_area()
        from gui.frames.chat_frame import ChatFrame
        self.content_area = ChatFrame(self, self.user_id, thread_id, participant_username, participant_id,
                                      self.load_inbox_screen)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_contract_details(self, project_id, job_title, partner_username, project_status):
        self.clear_content_area()
        from gui.frames.contract_details_frame import ContractDetailsFrame
        self.content_area = ContractDetailsFrame(self, project_id, job_title, partner_username, project_status,
                                                 self.load_my_jobs_list)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def process_job_submission(self, title, description, budget, deadline, seniority):
        if post_new_job(self.user_id, title, description, budget, deadline, seniority):
            messagebox.showinfo("Success", "Job vacancy posted successfully!")
            self.load_main_dashboard()
        else:
            messagebox.showerror("Database Error", "Failed to post the job vacancy. Check your database connection.")
