from tinydb import TinyDB, Query
import os

class DatabaseManager:
    def __init__(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        self.users_db = TinyDB('data/users.json')
        self.medicines_db = TinyDB('data/medicines.json')
        self.batches_db = TinyDB('data/batches.json')
        self.sales_db = TinyDB('data/sales.json')

        # Create default admin if not exists
        User = Query()
        if not self.users_db.search(User.username == 'admin'):
            from core.admin import Admin
            admin = Admin("Super Admin", "9876543210", "admin@medistock.com", "admin", "123")
            self.users_db.insert({
                'name': admin.get_name(),
                'username': admin.get_username(),
                'password': '123',
                'role': 'Admin'
            })

        # Create default consumer if not exists
        if not self.users_db.search(User.username == 'consumer'):
            self.users_db.insert({
                'name': 'Test Consumer',
                'username': 'consumer',
                'password': '123',
                'role': 'Consumer'
            })

    def verify_login(self, username, password):
        User = Query()
        result = self.users_db.search(User.username == username)
        if result:
            return result[0]
        return None