"""Реалізація інтерфейсу командного рядка"""

import re
import os
import os.path
from difflib import get_close_matches

from prettytable import PrettyTable

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

from .addressbook import (
    Name,
    Phone,
    Email,
    Address,
    Birthday,
    Record,
    AddressBook,
)

from .serializer import PickleStorage

from .filesorter import main as sort_main

# ============================== ANSI Colors =================================#

G = "\033[0;32;40m"  # GREEN
B = "\033[96m"  # Blue
P = "\033[95m"  # Pink
R = "\033[1;31m"  # Red
N = "\033[0m"  # Reset
Y = "\033[0;33;40m"  # Yellow

# ============================ Tables decoration =============================#


def build_contacts_table(records):
    table = PrettyTable()
    table.field_names = ["Name", "Phone", "Birthday", "Email", "Address"]
    for record in records:
        table.add_row(
            [
                G + record.data["name"].value + N,
                B + record.show_data("phone") + N,
                Y + record.show_data("birthday") + N,
                P + record.show_data("email") + N,
                Y + record.show_data("address") + N,
            ]
        )
    return f"{N}{table}"


# def build_contacts_table(records):
#     table = PrettyTable()
#     table.field_names = ["Name", "Phone", "Birthday", "Email", "Address"]
#     for record in records:
#         table.add_row(
#             [
#                 record.data["name"].value,
#                 record.show_data("phone"),
#                 record.show_data("birthday"),
#                 record.show_data("email"),
#                 record.show_data("address"),
#             ]
#         )
#     return f"\033[0m{table}"


# def build_table_notes(data):
#     table = PrettyTable()
#     table.field_names = ["ID", "Tag", "Created", "Note"]
#     table.align["Note"] = "l"
#     for tag, notes in data.items():
#         for note in notes:
#             idx = note["id"]
#             created = note["created"].strftime("%Y-%m-%d %H:%M:%S")
#             text = note["text"]
#             table.add_row([idx, tag, created, text])
#     return table


# ================================= Decorator ================================#


def input_error(func):
    def wrapper(*func_args, **func_kwargs):
        try:
            return func(*func_args, **func_kwargs)
        except KeyError as error:
            return "{}".format(R + str(error).strip("'") + N)
        except ValueError as error:
            return f"{R+str(error)+N}"
        except TypeError as error:
            return f"{R + str(error) + N}"
        except FileNotFoundError:
            return R + "File not found" + N

    return wrapper


# ================================== handlers ================================#


def hello(*args):
    return "\033[32mHow can I help you?\033[0m"


def good_bye(*args):
    PickleStorage.export_file(contacts, CONTACT_FILE)
    return "Good bye!"


@input_error
def undefined(*args):
    if args[0] not in list(COMMANDS.keys()):
        matches = get_close_matches(args[0], list(COMMANDS.keys()))
        if matches:
            suggestion = matches[0]
            return f"Command {R + args[0] + N} not found. Possibly you mean {Y + suggestion + N}?"
        else:
            return R + "What do you mean?" + N


@input_error
def save(*args):
    PickleStorage.export_file(contacts, args[0])
    return f"File {args[0]} saved"


# @input_error
# def save_notes(*args):
#     PickleStorage.export_file(notes, args[0])
#     return f"File {args[0]} saved"


@input_error
def load(*args):
    if PickleStorage.is_file_exist(args[0]):
        contacts.clear()
        contacts.update(PickleStorage.import_file(args[0]))
        return f"File {args[0]} loaded"
    else:
        raise FileNotFoundError


@input_error
def set_birthday(*args):
    """Функція-handler додає день народження до контакту."""

    if not args[0] or args[0].isdigit():
        raise KeyError("Give me a name, please")
    if not args[1]:
        raise ValueError("Give me a date, please")

    name, birthday = Name(args[0]), Birthday(args[1])

    if name.value in contacts.data:
        record = contacts.data[name.value]
    else:
        record = Record(name)
        contacts.add_record(record)
    record.add_data("birthday", birthday.value)

    return f"I added a birthday {args[1]} to contact {args[0]}"


@input_error
def set_phone(*args):
    """Додає телефонный номер в контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")
    if not args[1]:
        raise ValueError("Give me a phone, please")

    name, phone = Name(args[0]), Phone(args[1])

    if name.value in contacts.data:
        record = contacts.data[name.value]
    else:
        record = Record(name)
        contacts.add_record(record)
    record.add_data("phone", phone.value)

    return f"I added a phone {args[1]} to contact {args[0]}"


@input_error
def remove_phone(*args):
    """Видаляє телефонный номер в контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    name = Name(args[0])

    if name.value in contacts.data:
        record = contacts.data[name.value]
        record.remove_data("phone")

    return f"I removed a phone of contact {args[0]}"


@input_error
def add_contact(*args):
    """Додає контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    name = Name(args[0])

    if name.value in contacts.data:
        record = contacts.data[name.value]
    else:
        record = Record(name)
        contacts.add_record(record)

    return f"I added a contact {args[0]} to Addressbook"


@input_error
def set_email(*args):
    """Добавляет email номер в контакт по имени."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    if not args[1]:
        raise ValueError("Give me a email, please")

    name, email = Name(args[0]), Email(args[1])

    if name.value in contacts.data:
        record = contacts.data[name.value]
    else:
        record = Record(name)
        contacts.add_record(record)
    record.add_data("email", email.value)

    return f"I added a email {args[1]} to contact {args[0]}"


@input_error
def set_address(*args):
    """Добавляет email номер в контакт по имени."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    if not args[1]:
        raise ValueError("Give me a address, please")

    name, address = Name(args[0]), Address(args[1])

    if name.value in contacts.data:
        record = contacts.data[name.value]
    else:
        record = Record(name)
        contacts.add_record(record)
    record.add_data("address", address.value)

    return f"I added a address {args[1]} to contact {args[0]}"


@input_error
def search(*args):

    if not args[0]:
        raise KeyError("Give me a some string, please")

    results = contacts.search(args[0])

    if results:
        return f"{N + build_contacts_table(results)}"
    return "By your request found nothing"


@input_error
def remove(*args):
    """Функція-handler видаляє запис з книги."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    name = Name(args[0])

    if name.value in contacts:
        del contacts[name.value]
    else:
        raise KeyError(f"Name {args[0]} does not exist in addressbook.")

    return f"Contact {name.value} was removed"


@input_error
def export_to_csv(*args):
    if not args[0]:
        raise TypeError("Set file name, please")
    contacts.export_file(args[0])
    return f"File {args[0]} exported to csv"


@input_error
def import_from_csv(*args):
    contacts.import_file(args[0])
    return f"File {args[0]} imported from csv"


@input_error
def show_contact(*args):
    if not args[0]:
        raise TypeError("What contact are you search for?")
    record = contacts.find_records(args[0])
    return build_contacts_table(record)


def show_contacts(*args):
    number_of_entries = (
        int(args[0])
        if args[0] is not None and isinstance(args[0], str) and args[0].isdigit()
        else 100
    )
    for tab in contacts.iterator(number_of_entries):
        if tab == "continue":
            input(G + "Press <Enter> to continue..." + N)
        else:
            print(build_contacts_table(tab.values()))

    return f"Address book contain {len(contacts)} contacts"


# record = contacts.show_records()
# return build_contacts_table(record)


def help_commands(*args):
    """Функція показує перелік всіх команд."""

    file_path = "readme.md"
    if not os.path.exists(file_path):
        return R + "File {file_path} not found." + N

    with open(file_path, "r") as file:
        code = file.read()
        lexer = get_lexer_by_name("markdown")
        formatted_code = highlight(code, lexer, TerminalFormatter())
        return formatted_code

    # table = PrettyTable()
    # table.field_names = ["Command"]
    # table.min_width.update({"Command": 20})

    # for command in COMMANDS:
    #     table.add_row([command])

    # return f"\nPlease type followed commands:\n\033[0m{table}"


# def add_note(*args):
#     notes.add(args[0], args[1])
#     return "I had added note."


# def show_notes(*args):
#     return f"\033[0m{build_table_notes(notes.display())}\033[0m"


# def search_notes(*args):
#     return f"\033[0m{build_table_notes(notes.find_notes(args[0]))}\033[0m"


# def remove_note(*args):
#     notes.remove_note(args[0])
#     return "Note deleted"


def show_contactsupcoming_birthdays(*args):
    results = contacts.upcoming_birthdays(args[0])
    return f"{N + build_contacts_table(results)}"


@input_error
def upcoming_birthdays(*args):
    if not args[0]:
        raise TypeError("Set days you interested")
    days = int(args[0])
    result = contacts.upcoming_birthdays(days)
    return build_contacts_table(result)


@input_error
def sort_folder(*args):
    sort_main(args[0])
    return f"Folder {args[0]} sorted"


# =============================== handler loader =============================#

COMMANDS = {
    "help": help_commands,
    "hello": hello,
    "add contact": add_contact,
    "set phone": set_phone,
    "remove phone": remove_phone,
    "set email": set_email,
    "set address": set_address,
    "set birthday": set_birthday,
    "upcoming birthdays": upcoming_birthdays,
    "show contacts": show_contacts,
    "show contact": show_contact,
    "remove contact": remove,
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    "save": save,
    "load": load,
    "search contact": show_contact,
    "export": export_to_csv,
    "import": import_from_csv,
    # "add note": add_note,
    # "show notes": show_notes,
    # "search notes": search_notes,
    # "remove note": remove_note,
    "sort folder": sort_folder,
}

command_pattern = "|".join(COMMANDS.keys())
pattern = re.compile(
    r"\b(\.|" + command_pattern + r")\b(?:\s+([a-zA-Z0-9\.\:\\_\-]+))?(?:\s+(.+))?",
    re.IGNORECASE,
)


def get_handler(*args):
    """Функція викликає відповідний handler."""

    return COMMANDS.get(args[0], undefined)


def wait_for_input(prompt):
    while True:
        inp = input(prompt).strip()
        if inp == "":
            continue
        break
    return inp


def parse_command(command):
    text = pattern.search(command)

    params = (
        tuple(
            map(
                # Made a commands to be a uppercase
                lambda x: x.lower() if text.groups().index(x) == 0 else x,
                text.groups(),
            )
        )
        if text
        else (None, command, 0)
    )

    return params


# ================================ main function ============================ #

contacts = AddressBook()  # Global variable for storing contacts
# notes = Note()  # Global variable for storing notes

NOTES_FILE = "notes"
CONTACT_FILE = "contacts.bin"


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(
        G
        + "Hello, I'm an assistant v1.0.0 (c) Team-9, GoIT 2023.\nType help, for more information."
        + N
    )
    load(CONTACT_FILE)
    # load_notes(NOTES_FILE)
    while True:
        command = wait_for_input(">>> ")

        if command.strip() == ".":
            save(CONTACT_FILE)
            # save_notes(NOTES_FILE)
            return

        params = parse_command(command)
        handler = get_handler(*params)
        response = handler(*params[1:])
        print(f"{G + response + N}")

        if response == "Good bye!":
            return None


# ================================ main program ============================= #

if __name__ == "__main__":
    main()
