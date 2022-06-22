"""
1. Добавить функционал сохранения адресной
книги на диск и восстановления с диска.
2. Добавить пользователю возможность
поиска по содержимому книги контакто
"""

from collections import UserDict
from datetime import datetime
import shelve


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if value.isalpha():
            Field.value.fset(self, value)
        else:
            raise ValueError


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if value.replace("+", "").replace("(", "").replace(")", "").isdigit():
            Field.value.fset(self, value)
        else:
            raise ValueError


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            Field.value.fset(self, value)
        except:
            Field.value.fset(self, "")


# Record реализует методы для добавления/удаления/редактирования объектов Phone и виводит др.
class Record:
    def __init__(self, name: Name, phone: list = None, birthday: Birthday = None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            current_date = datetime.now().date()
            bday_year = current_date.year
            days = datetime.strptime(self.birthday.value, "%Y-%m-%d").replace(year=bday_year).date() - current_date
            if days.days < 0:
                days = datetime.strptime(self.birthday.value, "%Y-%m-%d").replace(
                    year=bday_year + 1).date() - current_date
            return f"{self.name.value}'s birthday in {days.days} days."
        else:
            return "No Birthday found"

    def add_phone(self, phone: Phone):
        self.phone.append(phone)

    def del_phone(self, phone: Phone):
        for p in self.phone:
            if phone.value == p.value:
                self.phone.remove(p)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        self.del_phone(old_phone)
        self.add_phone(new_phone)

    def __repr__(self):
        return f"{self.name.value}: {[i.value for i in self.phone]}, birthday: {self.birthday.value}"


class AddressBook(UserDict):
    N = 2

    def iterator(self):
        index, print_block = 1, '-' * 50 + '\n'
        for record in self.data.values():
            print_block += str(record) + '\n'
            if index < self.N:
                index += 1
            else:
                yield print_block
                index, print_block = 1, '-' * 50 + '\n'
        yield print_block

    def show_all_records(contacts, *args):
        if not contacts:
            return 'Address book is empty'
        result = 'List of all users:\n'
        print_list = contacts.iterator()
        for item in print_list:
            result += f'{item}'
        return result

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def show_phone_numbers(self, name: Name):
        return [i.value for i in self.data[name].phone]

    def save(self, *args) -> str:
        fh: str = 'database/contacts_db'
        with shelve.open(fh) as db:
            db['contacts'] = dict(self.data)
        return f"Records were saved to '{fh}' successfully!"

    @staticmethod
    def load_from():
        fh: str = 'database/contacts_db'
        with shelve.open(fh) as db:
            _ = AddressBook()
            _.data = db['contacts']
            return _


phone_book = AddressBook()


def input_error(func):  # обробник помилок
    def inner(*args):
        try:
            result = func(*args)
        except IndexError:
            return "Please, enter the name and number"
        except ValueError:
            return "Enter a valid number"
        except KeyError:
            return "No such name in phonebook"
        return result

    return inner


# распаковывает из
def load(*args):
    global phone_book
    phone_book = AddressBook().load_from()
    return f"Records were loaded successfully!"


@input_error
def add_user(*args):  # новый контакт
    name = Name(args[0])
    phone_list = []
    for i in args[1:]:
        phone_list.append(Phone(i))
    try:
        bday = Birthday(args[-1])
    except ValueError:
        bday = Birthday(None)
    rec = Record(name, phone_list, bday)
    if rec.name.value not in phone_book:
        phone_book.add_record(rec)
    else:
        return f"The name {name.value} already exists."
    return f"Contact {name.value} added successfully!"


@input_error
def add_number(*args):  # новый номер
    phone_book[args[0]].add_phone(Phone(args[1]))
    return f"User {args[0]}: {args[1]} is successfully added."


@input_error
def del_number(*args):  # видалити
    phone_book[args[0]].del_phone(Phone(args[1]))
    return f"Phone number {args[1]} is successfully deleted."


@input_error
# новый номер телефона для существующего контакта
def change_number(*args):
    phone_book[args[0]].change_phone(Phone(args[1]), Phone(args[2]))
    return f"Phone number {args[0]}'s is  changed: {args[2]}"


@input_error
# выводит номер телефона для указанного контакта
def print_phone(*args):
    return phone_book.show_phone_numbers(args[0])


@input_error
def days_to_b_day(*args):
    return phone_book[args[0]].days_to_birthday()


@input_error
# выводит все сохраненные контакты с номерами
def show_all(*args):
    if not phone_book:
        return f'List of contacts is empty'
    lst = ["{:>10}".format(k, str(v)) for k, v in phone_book.items()]
    return "\n".join(lst)


# возможность поиска по содержимому книги контактов
@input_error
def search(*args):
    result = []
    for k, v in phone_book.items():
        if args[0].lower() in k.lower() or args[0] in [p.value for p in v.phone] or args[0] in v.birthday.value:
            result.append("{:^10}: {:>10}".format(k, str(v)))
    if result:
        return "\n".join(result)
    else:
        return "No matches"


def show_records(*args):
    return phone_book.show_all_records(args[0])


def hello(*args):
    return "How can I help you?"


def exit(*args):
    return "Good bye!"


COMMANDS = {hello: ["hello", "hi", "h"],
            change_number: ["change", "change number"],
            print_phone: ["phone"],
            exit: ["exit", "close", "good bye", ".", "bye"],
            add_user: ["add user"],
            add_number: ["add number", "add phone"],
            show_all: ["all users"],
            del_number: ["delete", "del", "del number"],
            days_to_b_day: ["days to birthday", "when birthday", "birthday"],
            show_records: ["show all", "show"],
            search: ["search", "find"],
            phone_book.save: ["save"],
            load: ["load"]
            }


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, tuple(user_input[len(i):].strip().split(" "))


def main():
    while True:
        user_input = input("Enter your command: ")
        try:
            result, data = parse_command(user_input)
            print(result(*data))
            if result is exit:
                break
        except TypeError:
            print(f"Not found. Please , choose the command: {[v for v in COMMANDS.values()]}")


if __name__ == "__main__":
    main()
