from datetime import datetime

class Application:
    def __init__(self, job_id, freelancer_id, cover_letter, proposed_price, proposed_deadline, application_id=None, created_at=None):
        self.application_id = application_id
        self.job_id = job_id
        self.freelancer_id = freelancer_id
        self.cover_letter = cover_letter
        self.proposed_price = proposed_price
        self.proposed_deadline = proposed_deadline
        self.created_at = created_at or datetime.now()
