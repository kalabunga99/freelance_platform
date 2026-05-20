import customtkinter as ctk
from tkinter import messagebox
from services.project_service import get_milestones, change_milestone_status, change_project_status


class ContractDetailsFrame(ctk.CTkFrame):
    def __init__(self, master, project_id, job_title, partner_username, project_status, back_cb):
        super().__init__(master, corner_radius=15)
        self.project_id = project_id
        self.job_title = job_title
        self.partner_username = partner_username
        self.project_status = project_status
        self.back_cb = back_cb

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))

        btn_back = ctk.CTkButton(header_frame, text="← Back", width=70, height=30,
                                 fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                 command=back_cb)
        btn_back.pack(side="left")

        self.title_label = ctk.CTkLabel(header_frame, text=job_title, font=("Arial", 18, "bold"))
        self.title_label.pack(side="left", padx=20)

        meta_frame = ctk.CTkFrame(self, fg_color="transparent")
        meta_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 15))

        lbl_partner = ctk.CTkLabel(meta_frame, text=f"Freelancer: {partner_username}", font=("Arial", 13), text_color="gray")
        lbl_partner.pack(side="left")

        status_colors = {"Active": "#3498DB", "Review": "#F1C40F", "Finished": "#2ECC71", "Canceled": "#E74C3C"}
        self.lbl_status = ctk.CTkLabel(meta_frame, text=f" {project_status.upper()} ", font=("Arial", 11, "bold"),
                                       fg_color=status_colors.get(project_status, "gray"), text_color="white", corner_radius=6)
        self.lbl_status.pack(side="right")

        self.list_container = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color="gray15")
        self.list_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 15))

        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 20))

        self.load_contract_phases()

    def load_contract_phases(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()
        for widget in self.footer_frame.winfo_children():
            widget.destroy()

        milestones = get_milestones(self.project_id)

        for m in milestones:
            m_id = m['milestone_id']
            m_title = m['title']
            m_amount = m['amount']
            m_status = m['status']

            card = ctk.CTkFrame(self.list_container, corner_radius=8, fg_color="gray20")
            card.pack(fill="x", pady=5, padx=5)

            m_text = f"• {m_title}  |  Amount: ${m_amount:.2f}  |  Status: {m_status}"
            ctk.CTkLabel(card, text=m_text, font=("Arial", 13)).pack(side="left", padx=15, pady=10)

            if self.project_status in ["Active", "Review"] and m_status == "Review":
                btn_approve = ctk.CTkButton(card, text="Approve & Release", width=130, height=26, font=("Arial", 11, "bold"),
                                            fg_color="#2ECC71", hover_color="#27AE60",
                                            command=lambda m_idx=m_id: self.handle_approve_phase(m_idx))
                btn_approve.pack(side="right", padx=15, pady=10)

        if self.project_status != "Finished" and self.project_status != "Canceled":
            all_finished = all(m['status'] == 'Finished' for m in milestones)
            if all_finished:
                btn_complete = ctk.CTkButton(self.footer_frame, text="🏁 Complete Contract", width=150, height=35, font=("Arial", 12, "bold"),
                                             fg_color="#2ECC71", hover_color="#27AE60",
                                             command=self.handle_complete_project)
                btn_complete.pack(side="right", padx=5)

            btn_cancel = ctk.CTkButton(self.footer_frame, text="❌ Cancel Contract", width=130, height=35, font=("Arial", 11),
                                       fg_color="#E74C3C", hover_color="#C0392B",
                                       command=self.handle_cancel_project)
            btn_cancel.pack(side="right", padx=5)

    def handle_approve_phase(self, milestone_id):
        if change_milestone_status(milestone_id, "Finished", self.project_id):
            milestones = get_milestones(self.project_id)
            if any(m['status'] == 'Review' for m in milestones):
                change_project_status(self.project_id, "Review")
                self.project_status = "Review"
            else:
                change_project_status(self.project_id, "Active")
                self.project_status = "Active"
            self.load_contract_phases()
        else:
            messagebox.showerror("Error", "Failed to release milestone payment. Check client balance.")

    def handle_complete_project(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to successfully close this contract?"):
            from services.project_service import get_user_projects

            active_projects = get_user_projects(self.master.user_id, "Client")
            freelancer_id = None
            for p in active_projects:
                if p['project_id'] == self.project_id:
                    freelancer_id = p['freelancer_id']
                    break

            if freelancer_id:
                from gui.frames.rating_dialog import RatingDialog
                RatingDialog(self, self.project_id, self.master.user_id, freelancer_id, self.back_cb)
            else:
                messagebox.showerror("Error", "Could not resolve freelancer data.")

    def handle_cancel_project(self):
        if messagebox.askyesno("Warning", "Are you sure you want to cancel this contract permanently?"):
            if change_project_status(self.project_id, "Canceled"):
                self.back_cb()
