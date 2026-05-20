import customtkinter as ctk
from tkinter import messagebox
from services.message_service import get_user_inbox, toggle_archive_thread, search_inbox_messages


class InboxFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, open_chat_cb, back_cb):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id
        self.open_chat_cb = open_chat_cb
        self.back_cb = back_cb
        self.showing_archived = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))

        btn_back = ctk.CTkButton(header_frame, text="← Back", width=70, height=32,
                                 fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                 command=back_cb)
        btn_back.pack(side="left")

        self.title_label = ctk.CTkLabel(header_frame, text="Messages Inbox", font=("Arial", 20, "bold"))
        self.title_label.pack(side="left", padx=20)

        self.btn_archive_toggle = ctk.CTkButton(header_frame, text="Show Archive", width=110, height=32,
                                                text_color="white", fg_color="#34495E", hover_color="#2C3E50",
                                                command=self.toggle_archive_view)
        self.btn_archive_toggle.pack(side="right")

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="Search messages...", height=35)
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_search = ctk.CTkButton(search_frame, text="🔍 Search", width=90, height=35, command=self.handle_search)
        btn_search.pack(side="left", padx=(0, 5))

        btn_clear = ctk.CTkButton(search_frame, text="Clear", width=60, height=35, fg_color="gray40", hover_color="gray50", command=self.clear_search)
        btn_clear.pack(side="left")

        self.scroll_container = ctk.CTkScrollableFrame(self, width=740, height=420, corner_radius=12)
        self.scroll_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 15))

        self.load_inbox_data()

    def load_inbox_data(self):
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        threads = get_user_inbox(self.user_id, self.showing_archived)

        if not threads:
            lbl_empty = ctk.CTkLabel(self.scroll_container, text="No conversations found.", font=("Arial", 14, "italic"), text_color="gray")
            lbl_empty.pack(pady=50)
            return

        for thread in threads:
            t_id = thread['thread_id']
            p_id = thread['participant_id']
            p_username = thread['participant_username']
            subject = thread['subject'] or "Direct Conversation"
            last_msg = thread['last_message'] or "No messages yet."
            unread = thread['unread_count']

            card = ctk.CTkFrame(self.scroll_container, corner_radius=10, border_width=1, border_color="gray30")
            card.pack(fill="x", padx=10, pady=6)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

            title_text = f"👤 {p_username}  ({subject})"
            if unread > 0:
                title_text += f"   🔴 {unread} new"

            lbl_title = ctk.CTkLabel(text_frame, text=title_text, font=("Arial", 14, "bold"), anchor="w")
            lbl_title.pack(fill="x")

            lbl_msg = ctk.CTkLabel(text_frame, text=last_msg, font=("Arial", 12), text_color="gray", anchor="w")
            lbl_msg.pack(fill="x", pady=(2, 0))

            actions_frame = ctk.CTkFrame(card, fg_color="transparent")
            actions_frame.pack(side="right", padx=15, pady=10)

            btn_open = ctk.CTkButton(actions_frame, text="💬 Open", width=75, height=28, font=("Arial", 11, "bold"),
                                     fg_color="#3498DB", hover_color="#2980B9",
                                     command=lambda t=t_id, u=p_username, p=p_id: self.open_chat_cb(t, u, p))
            btn_open.pack(side="left", padx=5)

            archive_btn_text = "📥 Unarchive" if self.showing_archived == 1 else "🗄️ Archive"
            btn_archive = ctk.CTkButton(actions_frame, text=archive_btn_text, width=75, height=28, font=("Arial", 11),
                                        fg_color="gray40", hover_color="gray50",
                                        command=lambda t=t_id: self.handle_archive_toggle(t))
            btn_archive.pack(side="left", padx=5)

    def toggle_archive_view(self):
        if self.showing_archived == 0:
            self.showing_archived = 1
            self.btn_archive_toggle.configure(text="Show Active", fg_color="#27AE60", hover_color="#2196F3")
            self.title_label.configure(text="Archived Messages")
        else:
            self.showing_archived = 0
            self.btn_archive_toggle.configure(text="Show Archive", fg_color="#34495E", hover_color="#2C3E50")
            self.title_label.configure(text="Messages Inbox")
        self.load_inbox_data()

    def handle_archive_toggle(self, thread_id):
        new_status = True if self.showing_archived == 0 else False
        response = toggle_archive_thread(thread_id, self.user_id, new_status)
        if response["success"]:
            self.load_inbox_data()
        else:
            messagebox.showerror("Error", "Failed to change archive status.")

    def handle_search(self):
        keyword = self.entry_search.get().strip()
        if not keyword:
            self.load_inbox_data()
            return

        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        results = search_inbox_messages(self.user_id, keyword)

        if not results:
            lbl_empty = ctk.CTkLabel(self.scroll_container, text="No matching messages found.", font=("Arial", 14, "italic"), text_color="gray")
            lbl_empty.pack(pady=50)
            return

        for msg in results:
            card = ctk.CTkFrame(self.scroll_container, corner_radius=10, border_width=1, border_color="gray30")
            card.pack(fill="x", padx=10, pady=6)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

            lbl_title = ctk.CTkLabel(text_frame, text=f"From: {msg['sender_username']} | Topic: {msg['subject'] or 'Direct'}", font=("Arial", 13, "bold"), anchor="w")
            lbl_title.pack(fill="x")

            lbl_body = ctk.CTkLabel(text_frame, text=msg['body'], font=("Arial", 12), text_color="gray", anchor="w")
            lbl_body.pack(fill="x", pady=2)

            btn_open = ctk.CTkButton(card, text="➡️ Go to Chat", width=90, height=28, font=("Arial", 11),
                                     command=lambda t=msg['thread_id'], u=msg['sender_username'], p=msg['sender_id']: self.open_chat_cb(t, u, p))
            btn_open.pack(side="right", padx=15, pady=10)

    def clear_search(self):
        self.entry_search.delete(0, "end")
        self.load_inbox_data()
