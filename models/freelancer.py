from models.user import User

class Freelancer(User):
    def __init__(self, user_id, username, password_hash, email, name, wrong_attempt=0, is_locked=False):

        super().__init__(user_id, username, password_hash, email, "Freelancer", wrong_attempt=wrong_attempt,
                         is_locked=is_locked)

        self.name = name
        self.skills = []
        self.years_of_experience = 0
        self.languages = []
        self.portfolio_links = []
        self.job_history = []
        self.rating = 0.0
