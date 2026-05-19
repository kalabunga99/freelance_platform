import customtkinter as ctk
from tkinter import messagebox
from services.user_service import get_profile_data, save_profile_data


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, back_to_dashboard_cb):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id
        self.back_to_dashboard_cb = back_to_dashboard_cb

        self.label_title = ctk.CTkLabel(self, text="Account Profile", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=(20, 5))

        self.label_subtitle = ctk.CTkLabel(self, text="View and update your company details", font=("Arial", 13),
                                           text_color="gray")
        self.label_subtitle.pack(pady=(0, 20))

        self.form_frame = ctk.CTkFrame(self, width=450, height=300, corner_radius=12)
        self.form_frame.pack(pady=10, padx=20)

        self.lbl_username = ctk.CTkLabel(self.form_frame, text="Username: ", font=("Arial", 14, "bold"))
        self.lbl_username.pack(anchor="w", padx=30, pady=(20, 2))

        self.lbl_email = ctk.CTkLabel(self.form_frame, text="Email: ", font=("Arial", 14, "bold"))
        self.lbl_email.pack(anchor="w", padx=30, pady=(5, 15))

        self.lbl_company = ctk.CTkLabel(self.form_frame, text="Company Name:", font=("Arial", 12))
        self.lbl_company.pack(anchor="w", padx=30, pady=(5, 2))
        self.entry_company = ctk.CTkEntry(self.form_frame, width=390)
        self.entry_company.pack(padx=30, pady=(0, 10))

        self.lbl_budget = ctk.CTkLabel(self.form_frame, text="Company Budget ($):", font=("Arial", 12))
        self.lbl_budget.pack(anchor="w", padx=30, pady=(5, 2))
        self.entry_budget = ctk.CTkEntry(self.form_frame, width=390)
        self.entry_budget.pack(padx=30, pady=(0, 10))

        self.lbl_rating = ctk.CTkLabel(self.form_frame, text="Average Rating: 0.00 ★", font=("Arial", 13, "bold"),
                                       text_color="#F1C40F")
        self.lbl_rating.pack(anchor="w", padx=30, pady=(10, 20))

        self.btn_save = ctk.CTkButton(self, text="💾 Save Changes", width=200, height=40, font=("Arial", 14, "bold"),
                                      command=self.handle_save)
        self.btn_save.pack(pady=20)

        self.btn_back = ctk.CTkButton(self, text="⬅ Back to Dashboard", fg_color="transparent",
                                      text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                      command=self.back_to_dashboard_cb)
        self.btn_back.pack(pady=5)

        self.load_profile_info()

    def load_profile_info(self):
        profile = get_profile_data(self.user_id)
        if profile:
            username, email, company_name, budget, average_grade = profile

            self.lbl_username.configure(text=f"Username:  {username}")
            self.lbl_email.configure(text=f"Email:  {email}")
            self.lbl_rating.configure(text=f"Average Rating:  {average_grade:.2f} ★")

            self.entry_company.insert(0, company_name)
            self.entry_budget.insert(0, str(budget))

    def handle_save(self):
        company_name = self.entry_company.get().strip()
        budget_str = self.entry_budget.get().strip()

        if not company_name or not budget_str:
            messagebox.showwarning("Input Error", "All profile fields must be filled.")
            return

        try:
            budget = float(budget_str)
        except ValueError:
            messagebox.showwarning("Input Error", "Budget must be a valid numerical value.")
            return

        if save_profile_data(self.user_id, company_name, budget):
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.back_to_dashboard_cb()
        else:
            messagebox.showerror("Error", "Failed to update profile data in the database.")
