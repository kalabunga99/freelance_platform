import customtkinter as ctk
from tkinter import messagebox
from services.project_service import leave_freelancer_review, change_project_status


class RatingDialog(ctk.CTkToplevel):
    def __init__(self, master, project_id, client_id, freelancer_id, success_cb):
        super().__init__(master)
        self.project_id = project_id
        self.client_id = client_id
        self.freelancer_id = freelancer_id
        self.success_cb = success_cb

        self.title("Leave a Review")
        self.geometry("400x320")
        self.resizable(False, False)
        self.lift()
        self.grab_set()

        ctk.CTkLabel(self, text="🏆 Contract Completed!", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(self, text="Please rate the freelancer's work:", font=("Arial", 12), text_color="gray").pack(pady=(0, 15))

        self.rating_option = ctk.CTkOptionMenu(self, values=["5 ★★★★★", "4 ★★★★", "3 ★★★", "2 ★★", "1 ★"], width=150)
        self.rating_option.pack(pady=5)

        ctk.CTkLabel(self, text="Feedback Comment (Optional):", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(10, 2))
        self.txt_comment = ctk.CTkTextbox(self, height=80, width=340, corner_radius=8)
        self.txt_comment.pack(padx=30, pady=(0, 15))

        self.btn_submit = ctk.CTkButton(self, text="Submit Review & Close", height=35, fg_color="#2ECC71", hover_color="#27AE60",
                                        command=self.process_review)
        self.btn_submit.pack(pady=10)

    def process_review(self):
        rating_str = self.rating_option.get()
        rating = int(rating_str[0])
        comment = self.txt_comment.get("1.0", "end-1c")

        if leave_freelancer_review(self.project_id, self.client_id, self.freelancer_id, rating, comment):
            change_project_status(self.project_id, "Finished")
            messagebox.showinfo("Success", "Thank you! Your review has been submitted and the contract is officially closed.")
            self.grab_release()
            self.destroy()
            self.success_cb()
        else:
            messagebox.showerror("Error", "Failed to submit review. Check database connection.")
