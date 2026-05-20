from datetime import datetime

class Message:
    def __init__(self, thread_id, sender_id, body, message_id=None, created_at=None):
        self.message_id = message_id
        self.thread_id = thread_id
        self.sender_id = sender_id
        self.body = body
        self.created_at = created_at or datetime.now()
