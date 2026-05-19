class User:
    def __init__(self,user_id,username,password_hash,email,role,wrong_attempt=0,is_locked=False):
        self.user_id = user_id
        self.username = username
        self.password = password_hash
        self.email = email
        self.role = role
        self.wrong_attempt = wrong_attempt
        self.is_locked = is_locked