def input_error(func):  # обробник помилок
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except IndexError:
            return "Give me name and phone please"
        except TypeError:
            return "The wrong command was entered. Please try again."
        except KeyError:
            return "This contact is not in list. Please try again"
        return result

    return inner


@input_error
def command_checker(str_: str):
    list_ = str_.split(' ')
    if list_[0].lower() in COMMANDS:
        command = list_[0].lower()
        del list_[0]
        return command, list_
    elif str_.lower() == 'show all':
        return str_.lower(), []


@input_error
def command_hello(*args, **kwargs):
    return "How can I help you?"


CONTACTS = {}


@input_error
def command_add(*args, **kwargs):  # новый контакт
    information = args[0]
    name = information[0]
    phone = information[1]
    CONTACTS[name] = phone
    return f"Contact {name} : {phone}."


@input_error
# новый номер телефона для существующего контакта
def command_change(*args, **kwargs):
    information = args[0]
    name = information[0]
    phone = information[1]
    if name in CONTACTS:
        CONTACTS[name] = phone
        return f"The contact {name}: {phone} was changed."
    else:
        return "Not Found"


@input_error
# выводит все сохраненные контакты с номерами
def command_show_all(*args, **kwargs):
    str_ = ''
    if CONTACTS == {}:
        return "Список пустой"
    else:
        for k, v in CONTACTS.items():
            str_ += k + " : " + v + '\n'
        return str_[:-1]


@input_error
# выводит номер телефона для указанного контакта
def phone_print(*args, **kwargs):
    information = args[0]
    name = information[0]
    if name in CONTACTS:
        return f"Номер {name} : {CONTACTS[name]}"
    else:
        return "Такого контакта не найдено"


COMMANDS = {
    'hello': command_hello,
    'add': command_add,
    'show all': command_show_all,
    'change': command_change,
    'phone': phone_print
}


def get_handler(operator):
    return COMMANDS[operator]


def main():
    while True:
        exit_words = ["good bye", "close", "exit", '.']
        kort = None  # будующий кортеж где первый эллемент - команда, воторой - данные
        command = input("Please input command: ")
        if command.lower() in exit_words:
            print("Good bye!")
            break
        kort = command_checker(command)
        if kort == None:
            print(f"Команды {command} не найдено")
            continue
        handler = get_handler(kort[0])
        print(handler(kort[1]))


if __name__ == "__main__":
    main()
