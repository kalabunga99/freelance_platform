import customtkinter as ctk
from tkinter import messagebox
from services.project_service import get_user_projects, get_milestones, change_project_status, change_milestone_status


class ProjectsFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, role, back_cb):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id
        self.role = role
        self.back_cb = back_cb

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))

        btn_back = ctk.CTkButton(header_frame, text="← Back", width=70, height=32,
                                 fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                 command=back_cb)
        btn_back.pack(side="left")

        self.title_label = ctk.CTkLabel(header_frame, text="Project Management Tracker", font=("Arial", 20, "bold"))
        self.title_label.pack(side="left", padx=20)

        self.scroll_container = ctk.CTkScrollableFrame(self, width=740, height=480, corner_radius=12)
        self.scroll_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 15))

        self.load_projects_data()

    def load_projects_data(self):
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        projects = get_user_projects(self.user_id, self.role)

        if not projects:
            lbl_empty = ctk.CTkLabel(self.scroll_container, text="No contracts or projects found.",
                                     font=("Arial", 14, "italic"), text_color="gray")
            lbl_empty.pack(pady=50)
            return

        for proj in projects:
            p_id = proj['project_id']
            title = proj['job_title']
            partner = proj['partner_username']
            status = proj['status']

            card = ctk.CTkFrame(self.scroll_container, corner_radius=10, border_width=1, border_color="gray30")
            card.pack(fill="x", padx=10, pady=8)

            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=15, pady=(10, 5))

            partner_role = "Freelancer" if self.role == "Client" else "Client"
            lbl_title = ctk.CTkLabel(top_row, text=f"📋 {title}", font=("Arial", 15, "bold"), anchor="w")
            lbl_title.pack(side="left")

            status_colors = {"Active": "#3498DB", "Review": "#F1C40F", "Finished": "#2ECC71", "Canceled": "#E74C3C"}
            lbl_status = ctk.CTkLabel(top_row, text=f" {status.upper()} ", font=("Arial", 11, "bold"),
                                      fg_color=status_colors.get(status, "gray"), text_color="white", corner_radius=6)
            lbl_status.pack(side="right", padx=5)

            lbl_partner = ctk.CTkLabel(card, text=f"{partner_role}: {partner}", font=("Arial", 12), text_color="gray",
                                       anchor="w")
            lbl_partner.pack(fill="x", padx=15, pady=(0, 5))

            milestones_frame = ctk.CTkFrame(card, fg_color="gray15", corner_radius=8)
            milestones_frame.pack(fill="x", padx=15, pady=8)

            ctk.CTkLabel(milestones_frame, text="Project Milestones & Phases:", font=("Arial", 12, "bold"),
                         text_color="gray70").pack(anchor="w", padx=10, pady=5)

            milestones = get_milestones(p_id)
            for m in milestones:
                m_id = m['milestone_id']
                m_title = m['title']
                m_amount = m['amount']
                m_status = m['status']

                m_row = ctk.CTkFrame(milestones_frame, fg_color="transparent")
                m_row.pack(fill="x", padx=10, pady=4)

                m_text = f"• {m_title} (${m_amount:.2f})  -  Status: {m_status}"
                ctk.CTkLabel(m_row, text=m_text, font=("Arial", 12)).pack(side="left")

                if status == "Active":
                    if self.role == "Freelancer" and m_status == "Active":
                        btn_submit = ctk.CTkButton(m_row, text="Submit for Review", width=110, height=24,
                                                   font=("Arial", 10),
                                                   fg_color="#F1C40F", hover_color="#D4AC0D", text_color="black",
                                                   command=lambda m_id=m_id, p_id=p_id: self.handle_milestone_update(
                                                       m_id, p_id, "Review"))
                        btn_submit.pack(side="right", padx=5)

                    elif self.role == "Client" and m_status == "Review":
                        btn_approve = ctk.CTkButton(m_row, text="Approve & Release", width=110, height=24,
                                                    font=("Arial", 10),
                                                    fg_color="#2ECC71", hover_color="#27AE60",
                                                    command=lambda m_id=m_id, p_id=p_id: self.handle_milestone_update(
                                                        m_id, p_id, "Finished"))
                        btn_approve.pack(side="right", padx=5)

            if status == "Active" and self.role == "Client":
                actions_row = ctk.CTkFrame(card, fg_color="transparent")
                actions_row.pack(fill="x", padx=15, pady=(5, 10))

                btn_cancel = ctk.CTkButton(actions_row, text="❌ Cancel Project", width=120, height=28,
                                           font=("Arial", 11),
                                           fg_color="#E74C3C", hover_color="#C0392B",
                                           command=lambda p_id=p_id: self.handle_project_status(p_id, "Canceled"))
                btn_cancel.pack(side="right", padx=5)

                all_finished = all(m['status'] == 'Finished' for m in milestones)
                if all_finished:
                    btn_complete = ctk.CTkButton(actions_row, text="🏁 Complete Project", width=130, height=28,
                                                 font=("Arial", 11, "bold"),
                                                 fg_color="#2ECC71", hover_color="#27AE60",
                                                 command=lambda p_id=p_id: self.handle_project_status(p_id, "Finished"))
                    btn_complete.pack(side="right", padx=5)

    def handle_milestone_update(self, milestone_id, project_id, new_status):
        if change_milestone_status(milestone_id, new_status):
            if new_status == "Review":
                change_project_status(project_id, "Review")
            self.load_projects_data()
        else:
            messagebox.showerror("Error", "Failed to update milestone phase status.")

    def handle_project_status(self, project_id, new_status):
        if messagebox.askyesno("Confirm", f"Are you sure you want to mark this project as {new_status}?"):
            if change_project_status(project_id, new_status):
                self.load_projects_data()
            else:
                messagebox.showerror("Error", "Failed to update project status.")
