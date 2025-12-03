from core.user import User

class Pharmacist(User):
    def __init__(self, name, phone, email, username, password):
        super().__init__(name, phone, email, username, password, "Pharmacist")

    def welcome(self):
        return "Welcome Pharmacist! Manage stock & sales."