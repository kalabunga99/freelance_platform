import customtkinter as ctk
from services.app_service import get_freelancer_proposals
from services.project_service import get_user_projects, get_milestones, change_milestone_status, change_project_status


class MyProposalsFrame(ctk.CTkFrame):
    def __init__(self, master, freelancer_id, back_to_dashboard_cb):
        super().__init__(master, fg_color="transparent")
        self.freelancer_id = freelancer_id
        self.back_to_dashboard_cb = back_to_dashboard_cb

        self.label_title = ctk.CTkLabel(self, text="My Submitted Proposals & Active Work", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=(20, 10))

        self.btn_back = ctk.CTkButton(self, text="⬅ Back to Dashboard", width=150, height=35,
                                      command=self.back_to_dashboard_cb)
        self.btn_back.pack(pady=(0, 15))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=780, height=460, corner_radius=12)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_proposals()

    def load_proposals(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        proposals = get_freelancer_proposals(self.freelancer_id)
        active_projects = get_user_projects(self.freelancer_id, "Freelancer")
        project_map = {p['job_id']: p for p in active_projects}

        if not proposals:
            no_props_lbl = ctk.CTkLabel(self.scroll_frame, text="You haven't submitted any proposals yet.",
                                        font=("Arial", 14, "italic"), text_color="gray")
            no_props_lbl.pack(pady=40)
            return

        for prop in proposals:
            job_id = prop['job_id']
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, border_width=1, border_color="gray30")
            card.pack(fill="x", padx=10, pady=8)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(fill="x", padx=15, pady=12)

            title_lbl = ctk.CTkLabel(text_frame, text=prop['job_title'], font=("Arial", 16, "bold"), anchor="w")
            title_lbl.pack(fill="x")

            status = prop['job_status']
            status_color = "#2ECC71" if status == "Open" else ("#F1C40F" if status == "Paused" else "#3498DB")

            info_text = f"Job Status: {status}  |  My Price: ${prop['proposed_price']:.2f}  |  Delivery: {prop['proposed_deadline']} days"
            info_lbl = ctk.CTkLabel(text_frame, text=info_text, font=("Arial", 12), text_color=status_color, anchor="w")
            info_lbl.pack(fill="x", pady=2)

            desc_lbl = ctk.CTkLabel(text_frame, text=prop['cover_letter'], font=("Arial", 12), text_color="gray",
                                    anchor="w",
                                    justify="left", wraplength=650)
            desc_lbl.pack(fill="x", pady=4)

            if status == "In Progress" and job_id in project_map:
                project_data = project_map[job_id]
                p_id = project_data['project_id']
                p_status = project_data['status']

                milestones_frame = ctk.CTkFrame(card, fg_color="gray15", corner_radius=8)
                milestones_frame.pack(fill="x", padx=15, pady=(5, 10))

                ctk.CTkLabel(milestones_frame, text="Project Milestones & Tracking:", font=("Arial", 12, "bold"),
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

                    if p_status == "Active" and m_status == "Active":
                        btn_submit = ctk.CTkButton(m_row, text="Submit Work", width=110, height=24, font=("Arial", 10),
                                                   fg_color="#F1C40F", hover_color="#D4AC0D", text_color="black",
                                                   command=lambda m_idx=m_id, p_idx=p_id: self.handle_submit_work(m_idx,
                                                                                                                  p_idx))
                        btn_submit.pack(side="right", padx=5)

    def handle_submit_work(self, milestone_id, project_id):
        if change_milestone_status(milestone_id, "Review"):
            change_project_status(project_id, "Review")
            self.load_proposals()
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "Failed to submit work for review.")
