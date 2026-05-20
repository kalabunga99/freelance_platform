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

        self.label_title = ctk.CTkLabel(self, text="My Profile", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=(15, 2))

        self.label_subtitle = ctk.CTkLabel(self, text="Manage your identity, expertise and achievements",
                                           font=("Arial", 13), text_color="gray")
        self.label_subtitle.pack(pady=(0, 15))

        self.tabview = ctk.CTkTabview(self, width=740, height=480)
        self.tabview.pack(padx=20, pady=5, fill="both", expand=True)

        self.tab_general = self.tabview.add("Personal Details")
        self.tab_skills_lang = self.tabview.add("Skills & Languages")
        self.tab_portfolio_history = self.tabview.add("Portfolio & History")

        self.setup_general_section()
        self.setup_skills_languages_section()
        self.setup_portfolio_history_section()

        self.btn_back = ctk.CTkButton(self, text="⬅ Back to Dashboard", width=180, height=38, fg_color="gray30",
                                      hover_color="gray40", command=self.back_to_dashboard_cb)
        self.btn_back.pack(pady=15)

        self.load_all_profile_data()

    def setup_general_section(self):
        self.lbl_username = ctk.CTkLabel(self.tab_general, text="User: ", font=("Arial", 14, "bold"))
        self.lbl_username.pack(anchor="w", padx=30, pady=(20, 5))

        self.lbl_email = ctk.CTkLabel(self.tab_general, text="Email: ", font=("Arial", 14), text_color="gray")
        self.lbl_email.pack(anchor="w", padx=30, pady=5)

        self.lbl_rating = ctk.CTkLabel(self.tab_general, text="Rating: 0.00 ★", font=("Arial", 14, "bold"), text_color="#F1C40F")
        self.lbl_rating.pack(anchor="w", padx=30, pady=5)

        ctk.CTkLabel(self.tab_general, text="Full Name:", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(20, 2))
        self.entry_name = ctk.CTkEntry(self.tab_general, width=650)
        self.entry_name.pack(padx=30, pady=(0, 10))

        ctk.CTkLabel(self.tab_general, text="Years of Experience:", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(10, 2))
        self.entry_experience = ctk.CTkEntry(self.tab_general, width=650)
        self.entry_experience.pack(padx=30, pady=(0, 20))

        self.btn_save_general = ctk.CTkButton(self.tab_general, text="💾 Save Changes", width=200, height=35,
                                              font=("Arial", 13, "bold"), command=self.handle_save)
        self.btn_save_general.pack(pady=10)

    def setup_skills_languages_section(self):
        self.skills_scroll = ctk.CTkScrollableFrame(self.tab_skills_lang, width=320, height=280, label_text="🛠️ Core Skills")
        self.skills_scroll.pack(side="left", padx=15, pady=10, fill="both", expand=True)

        row_skill = ctk.CTkFrame(self.skills_scroll, fg_color="transparent")
        row_skill.pack(fill="x", pady=5)
        self.entry_skill = ctk.CTkEntry(row_skill, placeholder_text="Add skill...", width=180)
        self.entry_skill.pack(side="left", padx=(0, 5))
        ctk.CTkButton(row_skill, text="➕", width=40, command=self.handle_add_skill).pack(side="left")

        self.skills_area = ctk.CTkFrame(self.skills_scroll, fg_color="gray15", corner_radius=8)
        self.skills_area.pack(fill="x", pady=5)

        self.lang_scroll = ctk.CTkScrollableFrame(self.tab_skills_lang, width=320, height=280, label_text="🌐 Languages Spoken")
        self.lang_scroll.pack(side="right", padx=15, pady=10, fill="both", expand=True)

        row_lang = ctk.CTkFrame(self.lang_scroll, fg_color="transparent")
        row_lang.pack(fill="x", pady=5)
        self.entry_language = ctk.CTkEntry(row_lang, placeholder_text="Add language...", width=180)
        self.entry_language.pack(side="left", padx=(0, 5))
        ctk.CTkButton(row_lang, text="➕", width=40, command=self.handle_add_language).pack(side="left")

        self.languages_area = ctk.CTkFrame(self.lang_scroll, fg_color="gray15", corner_radius=8)
        self.languages_area.pack(fill="x", pady=5)

    def setup_portfolio_history_section(self):
        self.portfolio_scroll = ctk.CTkScrollableFrame(self.tab_portfolio_history, width=320, height=280, label_text="🔗 Portfolio Links")
        self.portfolio_scroll.pack(side="left", padx=15, pady=10, fill="both", expand=True)

        row_port = ctk.CTkFrame(self.portfolio_scroll, fg_color="transparent")
        row_port.pack(fill="x", pady=5)
        self.entry_portfolio = ctk.CTkEntry(row_port, placeholder_text="Add link...", width=180)
        self.entry_portfolio.pack(side="left", padx=(0, 5))
        ctk.CTkButton(row_port, text="➕", width=40, command=self.handle_add_portfolio).pack(side="left")

        self.portfolio_area = ctk.CTkFrame(self.portfolio_scroll, fg_color="gray15", corner_radius=8)
        self.portfolio_area.pack(fill="x", pady=5)

        self.history_scroll = ctk.CTkScrollableFrame(self.tab_portfolio_history, width=320, height=280, label_text="🏆 Job History")
        self.history_scroll.pack(side="right", padx=15, pady=10, fill="both", expand=True)

        self.history_area = ctk.CTkFrame(self.history_scroll, fg_color="gray15", corner_radius=8)
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
            name = item if isinstance(item, str) else item
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
            ctk.CTkLabel(self.history_area, text=f"⭐ {title}\n  Earned: ${earnings}", font=("Arial", 12),
                         text_color="#2ECC71", anchor="w", justify="left").pack(fill="x", padx=15, pady=5)

    def handle_save(self):
        name = self.entry_name.get().strip()
        exp_str = self.entry_experience.get().strip()
        if not name or not exp_str:
            messagebox.showwarning("Warning", "Name and experience are required.")
            return
        try:
            exp = int(exp_str)
        except ValueError:
            messagebox.showerror("Error", "Experience must be an integer.")
            return
        if save_free_profile_data(self.user_id, name, exp):
            messagebox.showinfo("Success", "Personal details updated.")
            self.load_all_profile_data()
        else:
            messagebox.showerror("Error", "Failed to update details.")

    def handle_add_skill(self):
        skill = self.entry_skill.get().strip()
        if skill and save_new_skill(self.user_id, skill):
            self.entry_skill.delete(0, "end")
            self.load_all_profile_data()

    def handle_add_language(self):
        lang = self.entry_language.get().strip()
        if lang and save_new_language(self.user_id, lang):
            self.entry_language.delete(0, "end")
            self.load_all_profile_data()

    def handle_add_portfolio(self):
        link = self.entry_portfolio.get().strip()
        if link and save_new_portfolio(self.user_id, link):
            self.entry_portfolio.delete(0, "end")
            self.load_all_profile_data()
