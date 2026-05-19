import customtkinter as ctk
from tkinter import messagebox


class PostJobFrame(ctk.CTkFrame):
    def __init__(self, master, client_id, back_to_dashboard_cb, submit_job_cb):
        super().__init__(master, fg_color="transparent")
        self.client_id = client_id
        self.back_to_dashboard_cb = back_to_dashboard_cb
        self.submit_job_cb = submit_job_cb

        self.label_title = ctk.CTkLabel(self, text="Create a New Job Post", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=(20, 15))

        self.entry_title = ctk.CTkEntry(self, placeholder_text="Job Title", width=350)
        self.entry_title.pack(pady=8)

        self.textbox_desc = ctk.CTkTextbox(self, width=350, height=100, border_width=2, corner_radius=8)
        self.textbox_desc.insert("0.0", "Job Description...")
        self.textbox_desc.pack(pady=8)

        self.entry_budget = ctk.CTkEntry(self, placeholder_text="Budget ($)", width=350)
        self.entry_budget.pack(pady=8)

        self.entry_deadline = ctk.CTkEntry(self, placeholder_text="Deadline (YYYY-MM-DD)", width=350)
        self.entry_deadline.pack(pady=8)

        self.label_seniority = ctk.CTkLabel(self, text="Required Seniority Level:", font=("Arial", 12))
        self.label_seniority.pack(pady=(8, 2))

        self.seniority_menu = ctk.CTkOptionMenu(self, values=["Junior", "Medior", "Senior"], width=350)
        self.seniority_menu.pack(pady=4)

        self.btn_submit = ctk.CTkButton(self, text="🚀 Post Job", width=350, height=40, command=self.handle_submit)
        self.btn_submit.pack(pady=20)

        self.btn_back = ctk.CTkButton(self, text="⬅ Cancel & Go Back", fg_color="transparent",
                                      text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                      command=self.back_to_dashboard_cb)
        self.btn_back.pack(pady=5)

    def handle_submit(self):
        title = self.entry_title.get().strip()
        description = self.textbox_desc.get("0.0", "end").strip()
        budget_str = self.entry_budget.get().strip()
        deadline = self.entry_deadline.get().strip()
        seniority = self.seniority_menu.get()

        if not title or not description or description == "Job Description..." or not budget_str or not deadline:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            budget = float(budget_str)
        except ValueError:
            messagebox.showwarning("Input Error", "Budget must be a valid number.")
            return

        self.submit_job_cb(title, description, budget, deadline, seniority)
