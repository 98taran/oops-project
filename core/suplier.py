class Supplier:
    def __init__(self, sup_id, name, phone, address):
        self.sup_id = sup_id
        self.name = name
        self.phone = phone
        self.address = address

    def __str__(self):
        return f"{self.name} - {self.phone}"