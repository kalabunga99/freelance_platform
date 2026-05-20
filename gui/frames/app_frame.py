import customtkinter as ctk
from tkinter import messagebox
from services.app_service import get_sorted_applications_for_client, hire_freelancer_service


class ApplicationsFrame(ctk.CTkFrame):
    def __init__(self, master, job_id, back_cb):
        super().__init__(master, corner_radius=15)
        self.job_id = job_id
        self.back_cb = back_cb

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))

        btn_back = ctk.CTkButton(header_frame, text="← Back", width=70, height=30,
                                 fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                 command=back_cb)
        btn_back.pack(side="left")

        self.title_label = ctk.CTkLabel(header_frame, text="Job Applications", font=("Arial", 20, "bold"))
        self.title_label.pack(side="left", padx=20)

        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))

        sort_label = ctk.CTkLabel(filter_frame, text="Sort by:", font=("Arial", 12))
        sort_label.pack(side="left", padx=(0, 10))

        self.sort_option = ctk.CTkOptionMenu(filter_frame, values=["Default", "cena", "iskustvo", "ocena", "AI score-u"],
                                             width=120, command=self.on_sort_changed)
        self.sort_option.pack(side="left")

        self.list_container = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.list_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))

        self.load_applications("Default")

    def on_sort_changed(self, choice):
        self.load_applications(choice)

    def load_applications(self, criteria):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        apps = get_sorted_applications_for_client(self.job_id, criteria)

        if not apps:
            no_apps_label = ctk.CTkLabel(self.list_container, text="No applications received yet.",
                                         font=("Arial", 14), text_color="gray")
            no_apps_label.pack(pady=40)
            return

        for app in apps:
            card = ctk.CTkFrame(self.list_container, corner_radius=8)
            card.pack(fill="x", pady=5, padx=5)

            info_text = f"👤 {app['freelancer_name']}  |  Exp: {app['years_of_experience']} yrs  |  Rating: ★{app['freelancer_rating']}"
            if 'ai_score' in app:
                info_text += f"  |  🤖 AI Score: {app['ai_score']}%"

            lbl_info = ctk.CTkLabel(card, text=info_text, font=("Arial", 13, "bold"), text_color=("gray10", "gray90"))
            lbl_info.pack(anchor="w", padx=15, pady=(8, 2))

            lbl_letter = ctk.CTkLabel(card, text=app['cover_letter'], font=("Arial", 12), text_color="gray",
                                      wraplength=500, justify="left")
            lbl_letter.pack(anchor="w", padx=15, pady=2)

            details_text = f"💰 Proposed Price: ${app['proposed_price']:.2f}   |   ⏱ Deadline: {app['proposed_deadline']} days"
            lbl_details = ctk.CTkLabel(card, text=details_text, font=("Arial", 12, "italic"), text_color="#3498DB")
            lbl_details.pack(anchor="w", padx=15, pady=(2, 8))

            btn_hire = ctk.CTkButton(card, text="🏆 Hire", width=90, height=30, font=("Arial", 12, "bold"),
                                     fg_color="#2ECC71", hover_color="#27AE60",
                                     command=lambda f_id=app['freelancer_id'], f_name=app['freelancer_name'], p=app['proposed_price']: self.handle_hire(f_id, f_name, p))
            btn_hire.pack(anchor="e", padx=15, pady=(0, 10))

    def handle_hire(self, freelancer_id, freelancer_name, proposed_price):
        confirm = messagebox.askyesno("Confirm Hire", f"Are you sure you want to hire {freelancer_name} for this project?")
        if not confirm:
            return

        job_title = self.title_label.cget("text")

        response = hire_freelancer_service(self.job_id, self.master.user_id, freelancer_id, job_title, proposed_price)
        if response["success"]:
            messagebox.showinfo("Success", "Project tracker and chat have been initialized successfully.")
            self.back_cb()
        else:
            messagebox.showerror("Error", response["message"])
