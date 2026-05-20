import customtkinter as ctk
from gui.frames.browse_jobs_frame import BrowseJobsFrame
from gui.frames.freelancer_profile_frame import FreelancerProfileFrame
from gui.frames.apply_job_frame import ApplyJobFrame
from gui.frames.my_proposals_frame import MyProposalsFrame
from gui.frames.inbox_frame import InboxFrame


class FreelancerDashboard(ctk.CTkFrame):
    def __init__(self, master, user_id, logout_cb):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id
        self.logout_cb = logout_cb

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.topbar = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        self.logo_label = ctk.CTkLabel(self.topbar, text="🚀 Freelancer Hub", font=("Arial", 18, "bold"))
        self.logo_label.pack(side="left", padx=20, pady=15)

        self.btn_browse_jobs = ctk.CTkButton(self.topbar, text="Find Jobs", fg_color="transparent",
                                             text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             width=100, height=35, command=self.load_browse_jobs_screen)
        self.btn_browse_jobs.pack(side="left", padx=10)

        self.btn_my_proposals = ctk.CTkButton(self.topbar, text="Proposals", fg_color="transparent",
                                              text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                              width=100, height=35, command=self.load_my_proposals_screen)
        self.btn_my_proposals.pack(side="left", padx=10)

        self.btn_inbox = ctk.CTkButton(self.topbar, text="Messages", fg_color="transparent",
                                       text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), width=100,
                                       height=35, command=self.load_inbox_screen)
        self.btn_inbox.pack(side="left", padx=10)

        self.btn_profile = ctk.CTkButton(self.topbar, text="My Profile", fg_color="transparent",
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
        from services.analytics_service import get_freelancer_dashboard_stats, get_platform_statistics_service
        from services.user_service import get_free_profile_data

        try:
            my_stats = get_freelancer_dashboard_stats(self.user_id)
            global_stats = get_platform_statistics_service()
            profile = get_free_profile_data(self.user_id)
            rating = float(profile[4]) if profile and len(profile) > 4 else 0.0
        except Exception as e:
            print(f"Error loading stats: {e}")
            my_stats = {'active_projects': 0, 'total_earnings': 0.00}
            global_stats = {'total_jobs': 0, 'hire_success_rate': 0.0, 'avg_fill_time_days': 0.0, 'top_skills': [],
                            'monthly_revenue': 0.00, 'top_freelancers': []}
            rating = 0.0

        self.content_area = ctk.CTkFrame(self, corner_radius=15)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        welcome_label = ctk.CTkLabel(self.content_area, text="Welcome, Freelancer!", font=("Arial", 22, "bold"))
        welcome_label.pack(anchor="w", padx=30, pady=(25, 5))

        sub_label = ctk.CTkLabel(self.content_area, text="Browse new jobs and track your earnings.", font=("Arial", 14),
                                 text_color="gray")
        sub_label.pack(anchor="w", padx=30, pady=(0, 15))

        stats_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        stats_frame.pack(fill="x", padx=25, pady=5)

        card1 = ctk.CTkFrame(stats_frame, width=220, height=85, corner_radius=10)
        card1.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(card1, text="My Active Projects", font=("Arial", 12), text_color="gray").pack(pady=(12, 2))
        ctk.CTkLabel(card1, text=str(my_stats.get('active_projects', 0)), font=("Arial", 20, "bold"),
                     text_color="#3498DB").pack()

        card2 = ctk.CTkFrame(stats_frame, width=220, height=85, corner_radius=10)
        card2.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(card2, text="My Public Rating", font=("Arial", 12), text_color="gray").pack(pady=(12, 2))
        ctk.CTkLabel(card2, text=f"{rating:.2f} ★", font=("Arial", 20, "bold"), text_color="#F1C40F").pack()

        card3 = ctk.CTkFrame(stats_frame, width=220, height=85, corner_radius=10)
        card3.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(card3, text="Platform 30-Day Volume", font=("Arial", 12), text_color="gray").pack(pady=(12, 2))
        ctk.CTkLabel(card3, text=f"${global_stats.get('monthly_revenue', 0.00):.2f}", font=("Arial", 20, "bold"),
                     text_color="#E67E22").pack()

        card4 = ctk.CTkFrame(self.content_area, corner_radius=10, height=70)
        card4.pack(fill="x", pady=15, padx=30)
        ctk.CTkLabel(card4, text="My Lifetime Net Earnings", font=("Arial", 12), text_color="gray").pack(pady=(8, 1))
        ctk.CTkLabel(card4, text=f"${my_stats.get('total_earnings', 0.00):.2f}", font=("Arial", 22, "bold"),
                     text_color="#2ECC71").pack(pady=(0, 8))

        leaderboard_box = ctk.CTkFrame(self.content_area, corner_radius=10)
        leaderboard_box.pack(fill="x", padx=30, pady=(5, 20))
        ctk.CTkLabel(leaderboard_box, text="🏆 Top Rated Platform Freelancers", font=("Arial", 13, "bold")).pack(pady=8)

        freelancers_list = global_stats.get('top_freelancers', [])
        if not freelancers_list:
            ctk.CTkLabel(leaderboard_box, text="No leaderboard data recorded yet.", font=("Arial", 12, "italic"),
                         text_color="gray").pack(pady=5)
        else:
            for f in freelancers_list:
                ctk.CTkLabel(leaderboard_box, text=f"⭐ {f['name']} (Rating: {float(f['rating']):.2f} ★)",
                             font=("Arial", 12)).pack(anchor="w", padx=25, pady=3)

    def load_browse_jobs_screen(self):
        self.clear_content_area()
        self.content_area = BrowseJobsFrame(self, self.user_id, self.load_main_dashboard)
        self.grid_rowconfigure(1, weight=1)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_profile_screen(self):
        self.clear_content_area()
        self.content_area = FreelancerProfileFrame(self, self.user_id, self.load_main_dashboard)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_apply_form(self, job_id):
        self.clear_content_area()
        self.content_area = ApplyJobFrame(self, self.user_id, job_id, self.load_browse_jobs_screen)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    def load_my_proposals_screen(self):
        self.clear_content_area()
        self.content_area = MyProposalsFrame(self, self.user_id, self.load_main_dashboard)
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
