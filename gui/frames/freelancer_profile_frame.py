import customtkinter as ctk
from tkinter import messagebox
from services.user_service import (
    get_free_profile_data, save_free_profile_data,
    get_skills, save_new_skill,
    get_languages, save_new_language,
    get_portfolio, save_new_portfolio, get_history
)


class FreelancerProfileFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, back_to_dashboard_cb):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id
        self.back_to_dashboard_cb = back_to_dashboard_cb

        # Izmenjen glavni naslov na vrhu u "My Profile"
        self.label_title = ctk.CTkLabel(self, text="My Profile", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=(15, 2))

        self.label_subtitle = ctk.CTkLabel(self, text="Manage your identity, expertise and languages",
                                           font=("Arial", 13), text_color="gray")
        self.label_subtitle.pack(pady=(0, 15))

        self.main_scroll = ctk.CTkScrollableFrame(self, width=740, height=540, corner_radius=12, fg_color="gray10")
        self.main_scroll.pack(padx=20, pady=10, fill="both", expand=True)

        self.setup_general_section()
        self.setup_skills_section()
        self.setup_languages_section()
        self.setup_portfolio_section()
        self.setup_history_section()

        self.btn_back = ctk.CTkButton(self, text="⬅ Back to Dashboard", width=180, height=38, fg_color="gray30",
                                      hover_color="gray40", command=self.back_to_dashboard_cb)
        self.btn_back.pack(pady=15)

        self.load_all_profile_data()

    def setup_general_section(self):
        section = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(section, text="👤 Personal Details", font=("Arial", 15, "bold")).pack(anchor="w", pady=(0, 10))

        row1 = ctk.CTkFrame(section, fg_color="transparent")
        row1.pack(fill="x", pady=2)
        self.lbl_username = ctk.CTkLabel(row1, text="User: ", font=("Arial", 13, "bold"))
        self.lbl_username.pack(side="left")
        self.lbl_rating = ctk.CTkLabel(row1, text="Rating: 0.00 ★", font=("Arial", 13, "bold"), text_color="#F1C40F")
        self.lbl_rating.pack(side="right")

        row2 = ctk.CTkFrame(section, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 10))
        self.lbl_email = ctk.CTkLabel(row2, text="Email: ", font=("Arial", 13), text_color="gray")
        self.lbl_email.pack(anchor="w")

        self.entry_name = ctk.CTkEntry(section, placeholder_text="Full Name", width=650)
        self.entry_name.pack(pady=5)

        row3 = ctk.CTkFrame(section, fg_color="transparent")
        row3.pack(fill="x", pady=5)
        self.entry_experience = ctk.CTkEntry(row3, placeholder_text="Years of Experience", width=490)
        self.entry_experience.pack(side="left")
        ctk.CTkButton(row3, text="💾 Save Changes", width=140, font=("Arial", 12, "bold"),
                      command=self.handle_save).pack(side="right")

        ctk.CTkLabel(self.main_scroll, text="─" * 70, text_color="gray30").pack(pady=10)

    def setup_skills_section(self):
        section = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(section, text="🛠️ Core Skills", font=("Arial", 15, "bold")).pack(anchor="w", pady=(0, 5))
        self.skills_area = ctk.CTkFrame(section, fg_color="gray15", corner_radius=8)
        self.skills_area.pack(fill="x", pady=5)

        row = ctk.CTkFrame(section, fg_color="transparent")
        row.pack(fill="x", pady=5)
        self.entry_skill = ctk.CTkEntry(row, placeholder_text="Add new skill...", width=540)
        self.entry_skill.pack(side="left")
        ctk.CTkButton(row, text="➕ Add", width=100, command=self.handle_add_skill).pack(side="right")

        ctk.CTkLabel(self.main_scroll, text="─" * 70, text_color="gray30").pack(pady=10)

    def setup_languages_section(self):
        section = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(section, text="🌐 Languages Spoken", font=("Arial", 15, "bold")).pack(anchor="w", pady=(0, 5))
        self.languages_area = ctk.CTkFrame(section, fg_color="gray15", corner_radius=8)
        self.languages_area.pack(fill="x", pady=5)

        row = ctk.CTkFrame(section, fg_color="transparent")
        row.pack(fill="x", pady=5)
        self.entry_language = ctk.CTkEntry(row, placeholder_text="Add new language...", width=540)
        self.entry_language.pack(side="left")
        ctk.CTkButton(row, text="➕ Add", width=100, command=self.handle_add_language).pack(side="right")

        ctk.CTkLabel(self.main_scroll, text="─" * 70, text_color="gray30").pack(pady=10)

    def setup_portfolio_section(self):
        section = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(section, text="🔗 Portfolio Links", font=("Arial", 15, "bold")).pack(anchor="w", pady=(0, 5))
        self.portfolio_area = ctk.CTkFrame(section, fg_color="gray15", corner_radius=8)
        self.portfolio_area.pack(fill="x", pady=5)

        row = ctk.CTkFrame(section, fg_color="transparent")
        row.pack(fill="x", pady=5)
        self.entry_portfolio = ctk.CTkEntry(row, placeholder_text="Add link (e.g. ://github.com)", width=540)
        self.entry_portfolio.pack(side="left")
        ctk.CTkButton(row, text="➕ Add", width=100, command=self.handle_add_portfolio).pack(side="right")

        ctk.CTkLabel(self.main_scroll, text="─" * 70, text_color="gray30").pack(pady=10)

    def setup_history_section(self):
        section = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(section, text="🏆 Job History & Earnings", font=("Arial", 15, "bold")).pack(anchor="w", pady=(0, 5))
        self.history_area = ctk.CTkFrame(section, fg_color="gray15", corner_radius=8)
        self.history_area.pack(fill="x", pady=5)

    def load_all_profile_data(self):
        profile = get_free_profile_data(self.user_id)
        if profile:
            username, email, name, years_of_experience, rating = profile
            self.lbl_username.configure(text=f"User: {username}")
            self.lbl_email.configure(text=f"Email: {email}")
            self.lbl_rating.configure(text=f"Rating: {rating:.2f} ★")
            self.entry_name.delete(0, "end")
            self.entry_name.insert(0, name)
            self.entry_experience.delete(0, "end")
            self.entry_experience.insert(0, str(years_of_experience))

        self.load_list_tags(get_skills(self.user_id), self.skills_area, "✔️")
        self.load_list_tags(get_languages(self.user_id), self.languages_area, "🌐")
        self.load_list_tags(get_portfolio(self.user_id), self.portfolio_area, "🔗")
        self.load_history_data()

    def load_list_tags(self, data, target_frame, prefix):
        for widget in target_frame.winfo_children(): widget.destroy()
        if not data:
            ctk.CTkLabel(target_frame, text="No items listed yet.", font=("Arial", 12, "italic"),
                         text_color="gray").pack(pady=10, padx=15, anchor="w")
            return
        for item in data:
            name = item if isinstance(item, tuple) else item
            lbl = ctk.CTkLabel(target_frame, text=f"{prefix} {name}", font=("Arial", 13), anchor="w")
            lbl.pack(fill="x", padx=15, pady=3)

    def load_history_data(self):
        for widget in self.history_area.winfo_children(): widget.destroy()
        history = get_history(self.user_id)
        if not history:
            ctk.CTkLabel(self.history_area, text="No completed projects recorded.", font=("Arial", 12, "italic"),
                         text_color="gray").pack(pady=10, padx=15, anchor="w")
            return
        for job in history:
            title, earnings = job
            ctk.CTkLabel(self.history_area, text=f"⭐ {title} (Earned: ${earnings})", font=("Arial", 13),
                         text_color="#2ECC71", anchor="w").pack(fill="x", padx=15, pady=3)

    def handle_save(self):
        name, exp_str = self.entry_name.get().strip(), self.entry_experience.get().strip()
        if not name or not exp_str: return
        try:
            if save_free_profile_data(self.user_id, name, int(exp_str)):
                messagebox.showinfo("Success", "Profile details updated successfully!")
        except:
            messagebox.showwarning("Error", "Invalid input format.")

    def handle_add_skill(self):
        val = self.entry_skill.get().strip()
        if val and save_new_skill(self.user_id, val):
            self.entry_skill.delete(0, "end");
            self.load_list_tags(get_skills(self.user_id), self.skills_area, "✔️")

    def handle_add_language(self):
        val = self.entry_language.get().strip()
        if val and save_new_language(self.user_id, val):
            self.entry_language.delete(0, "end");
            self.load_list_tags(get_languages(self.user_id), self.languages_area, "🌐")

    def handle_add_portfolio(self):
        val = self.entry_portfolio.get().strip()
        if val and save_new_portfolio(self.user_id, val):
            self.entry_portfolio.delete(0, "end");
            self.load_list_tags(get_portfolio(self.user_id), self.portfolio_area, "🔗")
