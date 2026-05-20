import customtkinter as ctk
from tkinter import messagebox
from services.app_service import submit_application


class ApplyJobFrame(ctk.CTkFrame):
    def __init__(self, master, freelancer_id, job_id, back_cb):
        super().__init__(master, corner_radius=15)
        self.freelancer_id = freelancer_id
        self.job_id = job_id
        self.back_cb = back_cb

        self.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        btn_back = ctk.CTkButton(header_frame, text="← Back", width=70, height=30,
                                 fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                 command=back_cb)
        btn_back.pack(side="left")

        title_label = ctk.CTkLabel(header_frame, text="Submit Your Proposal", font=("Arial", 20, "bold"))
        title_label.pack(side="left", padx=20)

        form_frame = ctk.CTkFrame(self, corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        lbl_letter = ctk.CTkLabel(form_frame, text="Cover Letter / Motivation Message:", font=("Arial", 13, "bold"))
        lbl_letter.pack(anchor="w", padx=20, pady=(15, 5))

        self.txt_cover_letter = ctk.CTkTextbox(form_frame, height=150, corner_radius=8)
        self.txt_cover_letter.pack(fill="x", padx=20, pady=(0, 10))

        pricing_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        pricing_frame.pack(fill="x", padx=20, pady=10)

        price_sub = ctk.CTkFrame(pricing_frame, fg_color="transparent")
        price_sub.pack(side="left", expand=True, fill="x", padx=(0, 10))
        lbl_price = ctk.CTkLabel(price_sub, text="Proposed Price ($):", font=("Arial", 13, "bold"))
        lbl_price.pack(anchor="w", pady=(0, 5))
        self.ent_price = ctk.CTkEntry(price_sub, placeholder_text="e.g. 150.00", height=35)
        self.ent_price.pack(fill="x")

        deadline_sub = ctk.CTkFrame(pricing_frame, fg_color="transparent")
        deadline_sub.pack(side="left", expand=True, fill="x", padx=(10, 0))
        lbl_deadline = ctk.CTkLabel(deadline_sub, text="Estimated Delivery (Days):", font=("Arial", 13, "bold"))
        lbl_deadline.pack(anchor="w", pady=(0, 5))
        self.ent_deadline = ctk.CTkEntry(deadline_sub, placeholder_text="e.g. 5", height=35)
        self.ent_deadline.pack(fill="x")

        self.btn_submit = ctk.CTkButton(form_frame, text="Send Application 🚀", height=40, font=("Arial", 14, "bold"),
                                        fg_color="#2ECC71", hover_color="#27AE60", command=self.process_application)
        self.btn_submit.pack(fill="x", padx=20, pady=25)

    def process_application(self):
        cover_letter = self.txt_cover_letter.get("1.0", "end-1c")
        price_str = self.ent_price.get().strip()
        deadline_str = self.ent_deadline.get().strip()

        if not price_str or not deadline_str:
            messagebox.showwarning("Warning", "All fields are required.")
            return

        try:
            price = float(price_str)
            deadline = int(deadline_str)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and deadline must be an integer.")
            return

        response = submit_application(self.job_id, self.freelancer_id, cover_letter, price, deadline)

        if response["success"]:
            messagebox.showinfo("Success", response["message"])
            self.back_cb()
        else:
            messagebox.showerror("Error", response["message"])
