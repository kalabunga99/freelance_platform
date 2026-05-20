import customtkinter as ctk
from tkinter import messagebox, simpledialog
from services.job_service import get_client_jobs, pause_job, close_job, extend_job_deadline


class MyJobsFrame(ctk.CTkFrame):
    def __init__(self, master, client_id, back_to_dashboard_cb):
        super().__init__(master, fg_color="transparent")
        self.client_id = client_id
        self.back_to_dashboard_cb = back_to_dashboard_cb

        self.label_title = ctk.CTkLabel(self, text="My Job Vacancies", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=(20, 10))

        self.btn_back = ctk.CTkButton(self, text="⬅ Back to Dashboard", width=150, height=35,
                                      command=self.back_to_dashboard_cb)
        self.btn_back.pack(pady=(0, 15))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=780, height=460, corner_radius=12)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_jobs()

    def load_jobs(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        jobs = get_client_jobs(self.client_id)

        if not jobs:
            no_jobs_lbl = ctk.CTkLabel(self.scroll_frame, text="You haven't posted any job vacancies yet.",
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

            status_color = "#2ECC71" if status == "Open" else ("#F1C40F" if status == "Paused" else "#E74C3C")
            status_lbl = ctk.CTkLabel(text_frame, text=f"● {status} | Budget: ${budget} | Exp: {deadline}",
                                      font=("Arial", 12), text_color=status_color, anchor="w")
            status_lbl.pack(fill="x", pady=2)

            desc_lbl = ctk.CTkLabel(text_frame, text=description, font=("Arial", 12), text_color="gray", anchor="w",
                                    justify="left", wraplength=500)
            desc_lbl.pack(fill="x", pady=4)

            actions_frame = ctk.CTkFrame(job_card, fg_color="transparent")
            actions_frame.pack(side="right", padx=15, pady=12)

            if status in ["Open", "Paused"]:
                btn_apps = ctk.CTkButton(actions_frame, text="👥 Applications", width=75, height=28, font=("Arial", 11),
                                         fg_color="#34495E", hover_color="#2C3E50",
                                         command=lambda j=job_id: self.view_applications(j))
                btn_apps.pack(pady=3)

            if status == "Open":
                btn_pause = ctk.CTkButton(actions_frame, text="⏸ Pause", width=75, height=28, font=("Arial", 11),
                                          fg_color="#F39C12", hover_color="#D35400",
                                          command=lambda j=job_id: self.handle_pause(j))
                btn_pause.pack(pady=3)

            if status != "Closed":
                btn_extend = ctk.CTkButton(actions_frame, text="📅 Extend", width=75, height=28, font=("Arial", 11),
                                           fg_color="#3498DB", hover_color="#2980B9",
                                           command=lambda j=job_id: self.handle_extend(j))
                btn_extend.pack(pady=3)

                btn_close = ctk.CTkButton(actions_frame, text="🛑 Close", width=75, height=28, font=("Arial", 11),
                                          fg_color="#E74C3C", hover_color="#C0392B",
                                          command=lambda j=job_id: self.handle_close(j))
                btn_close.pack(pady=3)

    def view_applications(self, job_id):
        if hasattr(self.master, "load_job_applications"):
            self.master.load_job_applications(job_id)

    def handle_pause(self, job_id):
        if pause_job(job_id):
            self.load_jobs()
        else:
            messagebox.showerror("Error", "Failed to pause the job vacancy.")

    def handle_close(self, job_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to close this job vacancy permanently?"):
            if close_job(job_id):
                self.load_jobs()
            else:
                messagebox.showerror("Error", "Failed to close the job vacancy.")

    def handle_extend(self, job_id):
        new_date = simpledialog.askstring("Extend Deadline", "Enter new deadline date (YYYY-MM-DD):")
        if new_date:
            if extend_job_deadline(job_id, new_date.strip()):
                messagebox.showinfo("Success", "Deadline extended successfully!")
                self.load_jobs()
            else:
                messagebox.showerror("Error", "Failed to extend the deadline. Ensure format is YYYY-MM-DD.")
