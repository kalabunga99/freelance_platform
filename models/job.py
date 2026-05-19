class Job:
    def __init__(self, job_id=None, client_id=None, title="", description="", budget=0.0, deadline=None, seniority="Junior", status="Open"):
        self.job_id = job_id
        self.client_id = client_id
        self.title = title
        self.description = description
        self.budget = budget
        self.deadline = deadline
        self.seniority = seniority
        self.status = status
        self.required_skills = []
