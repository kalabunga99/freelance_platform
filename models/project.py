from datetime import datetime

class Project:
    def __init__(self, job_id, client_id, freelancer_id, status='Active', project_id=None, created_at=None):
        self.project_id = project_id
        self.job_id = job_id
        self.client_id = client_id
        self.freelancer_id = freelancer_id
        self.status = status
        self.created_at = created_at or datetime.now()