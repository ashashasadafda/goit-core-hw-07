#dz_07

from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("номер телефону повинен будти 10-ти значним!")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, edited_phone):
        for i, p in enumerate(self.phones):
            if str(p) == old_phone:
                self.phones[i] = Phone(edited_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return str(p)
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday set"

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = self.show_birthday() if self.birthday else "No birthday set"
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                next_birthday_year = today.year

                if birthday < today:
                    next_birthday_year += 1

                next_birthday = datetime(next_birthday_year, birthday.month, birthday.day).date()
                
                if (next_birthday - today <= timedelta(days=30)) and (next_birthday - today >= timedelta(days=0)):
                    if next_birthday.weekday() in [5, 6]:
                        next_birthday += timedelta(days=(7 - next_birthday.weekday()))

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": next_birthday.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

def change_phone(args, book):
    name, phone = args
    record = book.find(name)
    if record is None:
        return f"Уонтакту з ім'ям {name} не знайдено"
    record.change_phone(phone)
    return f"Комер для контаку {name} змінено на {phone} =)"

def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Уонтакту з ім'ям {name} не знайдено"
    return f"Номер контакта {name}: {record.show_phone()}"

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments provided."
        except Exception as e:
            return str(e)
    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return f"No contact with name {name} found."
    record.add_birthday(birthday)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"No contact with name {name} found."
    return f"Birthday for {name}: {record.show_birthday()}"

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next 30 days."
    return "\n".join([f"{user['name']}: {user['congratulation_date']}" for user in upcoming_birthdays])

def parse_input(user_input):
    parts = user_input.split()
    command = parts[0]
    args = parts[1:]
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            print("Ви нічого не ввелию Будь ласка, введіть команду)")
        else:
            command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
