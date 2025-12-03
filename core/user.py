from core.person import Person

class User(Person):
    def __init__(self, name, phone, email, username, password, role):
        super().__init__(name, phone, email)
        self.__username = username
        self.__password = password      # In real project use hashing!
        self.role = role                # "Admin", "Pharmacist", "Cashier"

    def get_username(self):
        return self.__username

    def check_password(self, password):
        return self.__password == password

    def __str__(self):
        return f"{super().__str__()} - {self.role}"