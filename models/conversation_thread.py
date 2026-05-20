from datetime import datetime

class ConversationThread:
    def __init__(self, client_id, freelancer_id, subject=None, thread_id=None, created_at=None, updated_at=None):
        self.thread_id = thread_id
        self.client_id = client_id
        self.freelancer_id = freelancer_id
        self.subject = subject
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
