from abc import ABC

class Person(ABC):
    def __init__(self, name, phone, email):
        self.__name = name
        self.__phone = phone
        self.__email = email

    # Getters
    def get_name(self):
        return self.__name
    def get_phone(self):
        return self.__phone
    def get_email(self):
        return self.__email

    # For display
    def __str__(self):
        return f"{self.__name} ({self.__phone})"