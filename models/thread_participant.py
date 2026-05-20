from datetime import datetime

class ThreadParticipant:
    def __init__(self, thread_id, user_id, is_archived=0, last_read_at=None):
        self.thread_id = thread_id
        self.user_id = user_id
        self.is_archived = is_archived
        self.last_read_at = last_read_at or datetime.now()
