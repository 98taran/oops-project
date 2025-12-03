from core.user import User

class Admin(User):
    def __init__(self, name, phone, email, username, password):
        super().__init__(name, phone, email, username, password, "Admin")

    # Admin can do everything
    def welcome(self):
        return "Welcome Admin! You have full access."