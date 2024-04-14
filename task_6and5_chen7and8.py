import pickle
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.now()
        upcoming_birthdays = []
        for name, record in self.records.items():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=today.year)
                if 0 <= (birthday_date - today).days < 7:
                    upcoming_birthdays.append(name)
        return upcoming_birthdays

def input_error(func):
    def wrapper(book, *args):
        try:
            return func(book, *args)
        except Exception as e:
            return str(e)
    return wrapper

@input_error
def add_contact(book, name, phone):
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message

@input_error
def change_phone(book, name, phone):
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.phones = [Phone(phone)]
    return "Phone number updated."

@input_error
def show_phone(book, name):
    record = book.find(name)
    if not record or not record.phones:
        return "No phone number found."
    phones = ', '.join(phone.value for phone in record.phones)
    return f"{name}: {phones}"

@input_error
def show_all_contacts(book):
    if not book.records:
        return "Address book is empty."
    return '\n'.join(f"{name}: {', '.join(phone.value for phone in record.phones)}"
                     for name, record in book.records.items())

@input_error
def add_birthday(book, name, birthday):
    record = book.find(name)
    if not record:
        return f"No contact with name {name}."
    record.add_birthday(birthday)
    return f"Birthday for {name} set to {birthday}."

@input_error
def show_birthday(book, name):
    record = book.find(name)
    if not record or not record.birthday:
        return f"No birthday set for {name}."
    return f"{name}'s birthday is on {record.birthday.value}."

@input_error
def birthdays_this_week(book):
    birthdays = book.get_upcoming_birthdays()
    if not birthdays:
        return "No birthdays coming up this week."
    return "Birthdays this week: " + ", ".join(birthdays)

def parse_input(user_input):
    return user_input.split(maxsplit=2)

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(book, *args))
        elif command == "change":
            print(change_phone(book, *args))
        elif command == "phone":
            print(show_phone(book, *args[0]))
        elif command == "all":
            print(show_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(book, *args))
        elif command == "show-birthday":
            print(show_birthday(book, *args[0]))
        elif command == "birthdays":
            print(birthdays_this_week(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
