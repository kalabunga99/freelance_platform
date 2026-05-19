from models.user import User

class Client(User):
    def __init__(self, user_id, username, password_hash, email, company_name, wrong_attempt=0, is_locked=False):

        super().__init__(user_id, username, password_hash, email, "Client", wrong_attempt, is_locked)

        self.company_name = company_name
        self.budget = 0.0
        self.posting_history = []
        self.average_grade = 0.0
