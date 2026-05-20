import customtkinter as ctk
from tkinter import messagebox
from services.message_service import open_conversation_thread, send_message


class ChatFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, thread_id, participant_username, participant_id, back_cb):
        super().__init__(master, corner_radius=15)
        self.user_id = user_id
        self.thread_id = thread_id
        self.participant_username = participant_username
        self.participant_id = participant_id
        self.back_cb = back_cb
        self.last_message_count = 0
        self.is_active = True

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))

        btn_back = ctk.CTkButton(header_frame, text="← Back to Inbox", width=110, height=32,
                                 fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                 command=self.handle_back)
        btn_back.pack(side="left", padx=10, pady=10)

        title_text = f"Chat with: {self.participant_username}"
        lbl_title = ctk.CTkLabel(header_frame, text=title_text, font=("Arial", 16, "bold"))
        lbl_title.pack(side="left", padx=15, pady=10)

        self.chat_container = ctk.CTkScrollableFrame(self, width=740, height=380, corner_radius=12, fg_color="gray15")
        self.chat_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))

        self.txt_message = ctk.CTkEntry(input_frame, placeholder_text="Type a message here...", height=40)
        self.txt_message.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.txt_message.bind("<Return>", lambda event: self.handle_send())

        btn_send = ctk.CTkButton(input_frame, text="Send ➔", width=90, height=40, font=("Arial", 12, "bold"),
                                 fg_color="#2ECC71", hover_color="#27AE60", command=self.handle_send)
        btn_send.pack(side="right")

        self.load_chat_history()
        self.start_auto_refresh()

    def load_chat_history(self):
        if not self.is_active:
            return

        messages = open_conversation_thread(self.thread_id, self.user_id)

        if len(messages) == self.last_message_count:
            return

        self.last_message_count = len(messages)

        for widget in self.chat_container.winfo_children():
            widget.destroy()

        for msg in messages:
            is_me = msg['sender_id'] == self.user_id

            msg_wrapper = ctk.CTkFrame(self.chat_container, fg_color="transparent")
            msg_wrapper.pack(fill="x", pady=4, padx=5)

            card_color = "#3498DB" if is_me else "gray25"
            anchor_side = "right" if is_me else "left"
            align_justify = "right" if is_me else "left"

            bubble = ctk.CTkFrame(msg_wrapper, fg_color=card_color, corner_radius=10)
            bubble.pack(side=anchor_side, padx=5)

            lbl_body = ctk.CTkLabel(bubble, text=msg['body'], font=("Arial", 13), text_color="white",
                                    wraplength=450, justify=align_justify)
            lbl_body.pack(padx=12, pady=8)

        self.master.after(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def start_auto_refresh(self):
        if self.is_active:
            self.load_chat_history()
            self.master.after(2000, self.start_auto_refresh)

    def handle_send(self):
        body = self.txt_message.get().strip()
        if not body:
            return

        response = send_message(sender_id=self.user_id, receiver_id=self.participant_id, body=body)

        if response["success"]:
            self.txt_message.delete(0, "end")
            self.load_chat_history()
        else:
            messagebox.showerror("Error", response["message"])

    def handle_back(self):
        self.is_active = False
        self.back_cb()
