import customtkinter as ctk
from tkinter import messagebox
from services.job_service import get_available_jobs


class BrowseJobsFrame(ctk.CTkFrame):
    def __init__(self, master, freelancer_id, back_to_dashboard_cb):
        super().__init__(master, fg_color="transparent")
        self.freelancer_id = freelancer_id
        self.back_to_dashboard_cb = back_to_dashboard_cb

        self.label_title = ctk.CTkLabel(self, text="Available Job Openings", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=(20, 10))

        self.btn_back = ctk.CTkButton(self, text="⬅ Back to Dashboard", width=150, height=35,
                                      command=self.back_to_dashboard_cb)
        self.btn_back.pack(pady=(0, 15))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=780, height=460, corner_radius=12)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_available_jobs()

    def load_available_jobs(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        jobs = get_available_jobs()

        if not jobs:
            no_jobs_lbl = ctk.CTkLabel(self.scroll_frame, text="No active job openings available at the moment.",
                                       font=("Arial", 14, "italic"), text_color="gray")
            no_jobs_lbl.pack(pady=40)
            return

        for job in jobs:
            job_id, client_id, title, description, budget, deadline, seniority, status = job

            job_card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, border_width=1, border_color="gray30")
            job_card.pack(fill="x", padx=10, pady=8)

            text_frame = ctk.CTkFrame(job_card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=15, pady=12)

            title_lbl = ctk.CTkLabel(text_frame, text=title, font=("Arial", 16, "bold"), anchor="w")
            title_lbl.pack(fill="x")

            info_lbl = ctk.CTkLabel(text_frame, text=f"Budget: ${budget} | Deadline: {deadline} | Level: {seniority}",
                                    font=("Arial", 12), text_color="#3498DB", anchor="w")
            info_lbl.pack(fill="x", pady=2)

            desc_lbl = ctk.CTkLabel(text_frame, text=description, font=("Arial", 12), text_color="gray", anchor="w",
                                    justify="left", wraplength=500)
            desc_lbl.pack(fill="x", pady=4)

            btn_apply = ctk.CTkButton(job_card, text="📩 Apply", width=90, height=35, font=("Arial", 12, "bold"),
                                      fg_color="#2ECC71", hover_color="#27AE60",
                                      command=lambda j=job_id: self.handle_apply(j))
            btn_apply.pack(side="right", padx=20, pady=12)

    def handle_apply(self, job_id):
        if hasattr(self.master, "load_apply_form"):
            self.master.load_apply_form(job_id)
