"""Реалізація інтерфейсу командного рядка"""

import re
import os
import os.path
from pathlib import Path
from difflib import get_close_matches

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.shortcuts import clear

from prettytable import PrettyTable, SINGLE_BORDER

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

from .addressbook import AddressBook

from .notebook import Notebook

from .serializer import PickleStorage

from .filesorter import main as sort_main

from .colors import G, B, P, R, N, Y


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
        except IndexError:
            return R + "No such index" + N

    return wrapper


# ================================== handlers ================================#


def hello(*args):
    return "\033[32mHow can I help you?\033[0m"


def good_bye(*args):
    PickleStorage.export_file(contacts, CONTACT_FILE)
    os.system("cls" if os.name == "nt" else "clear")
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
    home_path = Path.home()
    file_path = home_path / args[0]
    PickleStorage.export_file(contacts, file_path)
    return f"File {args[0]} saved"


@input_error
def load(*args):
    home_path = Path.home()
    file_path = home_path / args[0]
    if PickleStorage.is_file_exist(file_path):
        contacts.clear()
        contacts.update(PickleStorage.import_file(file_path))
        return f"File {args[0]} loaded"
    else:
        raise FileNotFoundError


# ========================= Робота з контактами ============================= #


@input_error
def add_contact(*args):
    """Додає контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.add_record(args[0])

    return f"I added a contact {args[0]} to Addressbook"


@input_error
def remove_contact(*args):
    """Функція-handler видаляє запис з книги."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    result = contacts.remove_record(args[0])

    if result:
        return f"Contact {args[0]} was removed"
    return f"{R}Contact {args[0]} not in address book{N}"


@input_error
def set_phone(*args):
    """Додає телефонный номер в контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")
    if not args[1]:
        raise ValueError("Give me a phone, please")

    contacts.add_phone(args[0], args[1])

    return f"I added a phone {args[1]} to contact {args[0]}"


@input_error
def remove_phone(*args):
    """Видаляє телефонный номер в контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.delete_phone_by_index(args[0], int(args[1]) - 1)

    return f"I removed a phone of contact {args[0]}"


@input_error
def set_email(*args):
    """Додає email номер в контакті по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    if not args[1]:
        raise ValueError("Give me a email, please")

    contacts.add_email(args[0], args[1])

    return f"I added a email {args[1]} to contact {args[0]}"


@input_error
def remove_email(*args):
    """Видаляє email номер в контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.delete_email_by_index(args[0], int(args[1]) - 1)

    return f"I removed a email of contact {args[0]}"


@input_error
def set_address(*args):
    """Додає адресу в контакт по імені."""
    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.add_address(args[0], args[1])

    return f"I added a address {args[1]} to contact {args[0]}"


@input_error
def remove_address(*args):
    """Видаляє email в контакті по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.remove_address(args[0])

    return f"I removed a address of contact {args[0]}"


@input_error
def set_birthday(*args):
    """Функція-handler додає день народження до контакту."""

    if not args[0] or args[0].isdigit():
        raise KeyError("Give me a name, please")
    if not args[1]:
        raise ValueError("Give me a date, please")

    contacts.add_birthday(args[0], args[1])

    return f"I added a birthday {args[1]} to contact {args[0]}"


@input_error
def upcoming_birthdays(*args):
    if not args[0]:
        raise TypeError("Set days you interested")
    days = int(args[0])
    result = contacts.upcoming_birthdays(days)
    return f"{N}{pretty_print(result)}{N}"


@input_error
def search_contact(*args):
    if not args[0]:
        raise KeyError("Give me a some string, please")

    results = contacts.find_records(args[0])

    if results:
        return f"{N}{pretty_print(results)}{N}"
    return "By your request found nothing"


def pretty_print(contacts):
    table = PrettyTable()
    table.field_names = ["#", "Name", "Birthday", "Phones", "Emails", "Address"]
    table.align["Emails"] = "l"
    table.set_style(SINGLE_BORDER)
    for i, record in enumerate(contacts):
        birthday = record.birthday[0].value if record.birthday else "-"
        address = record.address[0] if record.address else "-"
        phones_str = _get_phones_str(record.phones)
        emails_str = _get_emails_str(record.emails)
        table.add_row(
            [
                i + 1,
                f"{G}{record.name}{N}",
                f"{B}{birthday}{N}",
                phones_str,
                emails_str,
                f"{Y}{address}{N}",
            ],
            divider=True,
        )
    return table


def _get_phones_str(phones):
    if not phones:
        return "-"
    phones_str = ""
    for i, phone in enumerate(phones):
        phones_str += f"{i+1}. {phone.value}\n"
    return phones_str[:-1]


def _get_emails_str(emails):
    if not emails:
        return "-"
    emails_str = ""
    for i, email in enumerate(emails):
        emails_str += f"{i+1}. {P}{email.value}{N}\n"
    return emails_str[:-1]


@input_error
def show_contacts(*args):
    number_of_entries = (
        int(args[0])
        if args[0] is not None and isinstance(args[0], str) and args[0].isdigit()
        else 20
    )

    current_contact_num = 1  # Начальный номер контакта
    for tab in contacts.iterator(number_of_entries):
        if tab == "continue":
            input(G + "Press <Enter> to continue..." + N)
        else:
            table = pretty_print(tab)
            # table.align["Emails"] = "l"
            # Обновляем номера контактов в колонке #
            for i, row in enumerate(table._rows):
                row[0] = current_contact_num + i
            print(table)
            # Обновляем текущий номер контакта
            current_contact_num += len(tab)
    return f"Address book contain {len(contacts)} contact(s)"


# ============================= Команди для нотаток ========================= #


@input_error
def add_note(*args):
    notebook.add_note([args[0]], args[1])
    return "I added note"


@input_error
def remove_note(*args):
    notebook.remove_note(int(args[0]))
    return "I removed note"


@input_error
def add_tag(*args):
    if not args[0].isdigit():
        raise TypeError("Index must be a number")
    notebook.add_tag(int(args[0]), args[1])
    return f"I addes tag {args[1]} to note {args[0]}"


def build_notes_table(notes, original_indices=False):
    table = PrettyTable()
    table.field_names = ["Index", "Tags", "Creation Date", "Text"]
    table.max_width["Text"] = 79
    table.set_style(SINGLE_BORDER)
    for note, index in notes:
        if original_indices:
            index = notebook.data.index(note)
        date_str = note.date.strftime("%Y-%m-%d %H:%M:%S")
        table.add_row(
            [
                f"{G}{index}{N}",
                ", ".join(note.tags),
                f"{Y}{date_str}{N}",
                f"{B}{note.text}{N}",
            ],
            divider=True,
        )
    return f"{N + str(table)}"


@input_error
def show_notes(*args):
    notes = notebook.display_notes(tag=args[0] or None, original_indices=True)
    return build_notes_table(notes, original_indices=True)


@input_error
def search_notes(*args):
    if not args[0]:
        raise KeyError("Please, add searh query")
    results = notebook.find_notes(args[0])
    if not results:
        return f"{R}Nothing found for {args[0]}{N}"
    return build_notes_table(results)


@input_error
def save_notes(*args):
    home_path = Path.home()
    file_path = home_path / args[0]
    PickleStorage.export_file(notebook, file_path)
    return f"File {args[0]} saved"


@input_error
def change_note(*args):
    if not args[0]:
        raise KeyError("Please, set integer index")

    notebook.change_note(int(args[0]), args[1])

    return f"I changed note {args[0]}"


@input_error
def load_notes(*args):
    home_path = Path.home()
    file_path = home_path / args[0]
    if PickleStorage.is_file_exist(file_path):
        notebook.clear()
        notebook.update(PickleStorage.import_file(file_path))
        return f"File {args[0]} loaded"
    else:
        raise FileNotFoundError


# =========================================================================== #
def help_commands(*args):
    """Функція показує перелік всіх команд."""

    PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
    README_PATH = os.path.join(PACKAGE_ROOT, "../README.md")

    if not os.path.exists(README_PATH):
        return R + f"File {README_PATH} not found." + N

    with open(README_PATH, "r") as file:
        code = file.read()
        lexer = get_lexer_by_name("markdown")
        formatted_code = highlight(code, lexer, TerminalFormatter())
        return formatted_code


@input_error
def sort_folder(*args):
    sort_main(args[0])
    return f"Folder {args[0]} sorted"


def cls(*args):
    clear()
    return HELLO_MESSAGE


# =============================== handler loader =============================#

COMMANDS = {
    # --- Hello commands ---
    "help": help_commands,
    "hello": hello,
    # --- Manage contacts ---
    "add contact": add_contact,
    "set phone": set_phone,
    "remove phone": remove_phone,
    "set email": set_email,
    "remove email": remove_email,
    "set address": set_address,
    "remove address": remove_address,
    "set birthday": set_birthday,
    "upcoming birthdays": upcoming_birthdays,
    "show contacts": show_contacts,
    "search contact": search_contact,
    "show contact": search_contact,
    "remove contact": remove_contact,
    "save": save,
    "load": load,
    # --- Manage notes ---
    "add note": add_note,
    "add tag": add_tag,
    "remove note": remove_note,
    "show notes": show_notes,
    "save notes": save_notes,
    "load notes": load_notes,
    "search notes": search_notes,
    "change note": change_note,
    # --- Sorting folder commnad ---
    "sort folder": sort_folder,
    # --- Googd bye commnad ---
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    "cls": cls,
}


class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()
        matches = [c for c in COMMANDS if c.startswith(word_before_cursor)]
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


session = PromptSession(completer=CommandCompleter())

command_pattern = "|".join(COMMANDS.keys())
pattern = re.compile(
    r"\b(\.|"
    + command_pattern
    + r")\b(?:\s+([а-яА-Яa-zA-Z0-9\.\:\\_\-]+))?(?:\s+(.+))?",
    re.IGNORECASE,
)


def get_handler(*args):
    """Функція викликає відповідний handler."""

    return COMMANDS.get(args[0], undefined)


def wait_for_input():
    while True:
        inp = session.prompt(">>> ")
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
notebook = Notebook()  # Global variable for storing notes


NOTES_FILE = "notes.bin"
CONTACT_FILE = "contacts.bin"
HELLO_MESSAGE = f"{G}Hello, I'm an assistant v1.0.0 (c) Team-9, GoIT 2023.\nType {Y}help{G} for more information.{N}"


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(HELLO_MESSAGE)
    load(CONTACT_FILE)
    load_notes(NOTES_FILE)
    while True:
        command = wait_for_input()
        if command.strip() == ".":
            save(CONTACT_FILE)
            save_notes(NOTES_FILE)
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
