import customtkinter as ctk


class FreelancerDashboard(ctk.CTkFrame):
    def __init__(self, master, user_id, logout_cb):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.topbar = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        self.logo_label = ctk.CTkLabel(self.topbar, text="🚀 Freelancer Hub", font=("Arial", 18, "bold"))
        self.logo_label.pack(side="left", padx=20, pady=15)

        self.btn_browse_jobs = ctk.CTkButton(self.topbar, text="Find Jobs", fg_color="transparent",
                                             text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             width=100, height=35)
        self.btn_browse_jobs.pack(side="left", padx=10)

        self.btn_my_proposals = ctk.CTkButton(self.topbar, text="Proposals", fg_color="transparent",
                                              text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                              width=100, height=35)
        self.btn_my_proposals.pack(side="left", padx=10)

        self.btn_profile = ctk.CTkButton(self.topbar, text="My Profile", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), width=100,
                                         height=35)
        self.btn_profile.pack(side="left", padx=10)

        self.btn_logout = ctk.CTkButton(self.topbar, text="Logout", fg_color="#E74C3C", hover_color="#C0392B",
                                        text_color="white", width=80, height=30, command=logout_cb)
        self.btn_logout.pack(side="right", padx=20)

        self.content_area = ctk.CTkFrame(self, corner_radius=15)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.welcome_label = ctk.CTkLabel(self.content_area, text="Welcome, Freelancer!", font=("Arial", 22, "bold"))
        self.welcome_label.pack(anchor="w", padx=30, pady=(30, 10))

        self.sub_label = ctk.CTkLabel(self.content_area, text="Browse new jobs and track your earnings.",
                                      font=("Arial", 14), text_color="gray")
        self.sub_label.pack(anchor="w", padx=30, pady=(0, 20))

        self.stats_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=30, pady=10)

        self.card1 = ctk.CTkFrame(self.stats_frame, width=150, height=80, corner_radius=10)
        self.card1.pack(side="left", expand=True, fill="both", padx=(0, 10))
        self.card1_title = ctk.CTkLabel(self.card1, text="Rating", font=("Arial", 12), text_color="gray")
        self.card1_title.pack(pady=(10, 2))
        self.card1_val = ctk.CTkLabel(self.card1, text="0.0 ★", font=("Arial", 20, "bold"), text_color="#F1C40F")
        self.card1_val.pack(pady=(0, 10))

        self.card2 = ctk.CTkFrame(self.stats_frame, width=150, height=80, corner_radius=10)
        self.card2.pack(side="left", expand=True, fill="both", padx=10)
        self.card2_title = ctk.CTkLabel(self.card2, text="Earnings", font=("Arial", 12), text_color="gray")
        self.card2_title.pack(pady=(10, 2))
        self.card2_val = ctk.CTkLabel(self.card2, text="$0.00", font=("Arial", 20, "bold"))
        self.card2_val.pack(pady=(0, 10))
