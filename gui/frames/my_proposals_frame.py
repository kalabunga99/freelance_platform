import customtkinter as ctk
from services.app_service import get_freelancer_proposals


class MyProposalsFrame(ctk.CTkFrame):
    def __init__(self, master, freelancer_id, back_to_dashboard_cb):
        super().__init__(master, fg_color="transparent")
        self.freelancer_id = freelancer_id
        self.back_to_dashboard_cb = back_to_dashboard_cb

        self.label_title = ctk.CTkLabel(self, text="My Submitted Proposals", font=("Arial", 22, "bold"))
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

        if not proposals:
            no_props_lbl = ctk.CTkLabel(self.scroll_frame, text="You haven't submitted any proposals yet.",
                                        font=("Arial", 14, "italic"), text_color="gray")
            no_props_lbl.pack(pady=40)
            return

        for prop in proposals:
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, border_width=1, border_color="gray30")
            card.pack(fill="x", padx=10, pady=8)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=15, pady=12)

            title_lbl = ctk.CTkLabel(text_frame, text=prop['job_title'], font=("Arial", 16, "bold"), anchor="w")
            title_lbl.pack(fill="x")

            status = prop['job_status']
            status_color = "#2ECC71" if status == "Open" else ("#F1C40F" if status == "Paused" else "#E74C3C")
            info_text = f"Job Status: {status}  |  My Price: ${prop['proposed_price']:.2f}  |  Delivery: {prop['proposed_deadline']} days"

            info_lbl = ctk.CTkLabel(text_frame, text=info_text, font=("Arial", 12), text_color=status_color, anchor="w")
            info_lbl.pack(fill="x", pady=2)

            desc_lbl = ctk.CTkLabel(text_frame, text=prop['cover_letter'], font=("Arial", 12), text_color="gray",
                                    anchor="w",
                                    justify="left", wraplength=650)
            desc_lbl.pack(fill="x", pady=4)
