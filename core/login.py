from core.database import DatabaseManager

class LoginManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None

    def login(self, username, password):
        user_data = self.db.verify_login(username, password)
        if user_data and user_data['password'] == password:
            # Create proper object based on role
            role = user_data['role']
            name = user_data['name']
            if role == "Admin":
                from core.admin import Admin
                self.current_user = Admin(name, "000", "a@a.com", username, password)
            elif role == "Pharmacist":
                from core.pharmacist import Pharmacist
                self.current_user = Pharmacist(name, "000", "a@a.com", username, password)
            elif role == "Consumer":
                from core.user import User
                self.current_user = User(name, "000", "c@c.com", username, password, "Consumer")
            else:
                from core.cashier import Cashier
                self.current_user = Cashier(name, "000", "a@a.com", username, password)
            return self.current_user
        return None