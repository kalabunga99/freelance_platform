class ProjectMilestone:
    def __init__(self, project_id, title, amount, status='Active', due_date=None, milestone_id=None, completed_at=None):
        self.milestone_id = milestone_id
        self.project_id = project_id
        self.title = title
        self.amount = amount
        self.status = status
        self.due_date = due_date
        self.completed_at = completed_at