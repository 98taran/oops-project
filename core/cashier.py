from core.user import User

class Cashier(User):
    def __init__(self, name, phone, email, username, password):
        super().__init__(name, phone, email, username, password, "Cashier")

    def welcome(self):
        return "Welcome Cashier! Create bills quickly."