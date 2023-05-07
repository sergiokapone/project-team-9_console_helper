"""Реалізація інтерфейсу командного рядка"""
import re
import os
import os.path
from pathlib import Path
from difflib import get_close_matches

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from prettytable.colortable import ColorTable, Themes

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

from bs4 import BeautifulSoup
import requests

from .addressbook import AddressBook

from .notebook import Notebook

from .currenсy import CurrencyList

from .serializer import PickleStorage

from .filesorter import sort_folder


from .colors import *


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
    return f"{G}How can I help you?{N}"


def good_bye(*args):
    os.system("cls" if os.name == "nt" else "clear")
    save(CONTACT_FILE)
    save_notes(NOTES_FILE)
    print("See you later.\nDotn't warry, your data was saved.")
    return "Good bye!"


@input_error
def undefined(*args):
    """Реакція на невідому команду"""

    if args[0] not in list(COMMANDS.keys()):
        matches = get_close_matches(args[0], list(COMMANDS.keys()))
        if matches:
            suggestion = matches[0]
            return f"{W}Command {R + args[0] + N} {W}not found. Possibly you mean {Y + suggestion + N}?"
        else:
            return R + "What do you mean?" + N


@input_error
def save(*args):
    if not args[0]:
        raise ValueError("Give me a filename.")

    home_path = Path.home()
    file_path = home_path / args[0]
    PickleStorage.export_file(contacts, file_path)
    return f"File {args[0]} saved."


@input_error
def load(*args):
    if not args[0]:
        raise ValueError("Give me a filename.")

    home_path = Path.home()
    file_path = home_path / args[0]
    if PickleStorage.is_file_exist(file_path):
        contacts.clear()
        contacts.update(PickleStorage.import_file(file_path))
        return f"File {args[0]} loaded."
    else:
        raise FileNotFoundError


# ========================= Робота з контактами ============================= #


def parse_contact_params(string):
    phone_regex = re.compile(r"\d{10}")
    date_regex = re.compile(r"\d{2}\.\d{2}\.\d{4}")
    email_regex = re.compile(r"[\w.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}")

    phone = phone_regex.search(string)
    date = date_regex.search(string)
    email = email_regex.search(string)

    phone = phone.group(0) if phone else None
    date = date.group(0) if date else None
    email = email.group(0) if email else None

    return phone, date, email


@input_error
def add_contact(*args):
    """Добавляет контакт с указанными параметрами"""
    usage_message = (
        f"Example of usage: {G}add contact {Y}Username{N} [phone1] [birthday] [email]."
    )
    error_message = None
    name = args[0]
    if not name:
        error_message = "Please provide a name for the contact."

    if error_message:
        print(usage_message)
        raise ValueError(error_message)

    contacts.add_record(name)
    rest_args = " ".join(args[1:]) if args[1:] != (None,) else False

    if rest_args:
        parsed_params = parse_contact_params(" ".join(args[1:]))
        phone = parsed_params[0]
        birthday = parsed_params[1]
        email = parsed_params[2]

        if phone:
            contacts.add_phone(name, phone)

        if birthday:
            contacts.add_birthday(name, birthday)

        if email:
            contacts.add_email(name, email)

    return f"I added a contact {name} to the address book."


@input_error
def remove_contact(*args):
    """Функція-handler видаляє запис з книги."""

    usage_message = f"Example of usage: {G}remove contact {Y}Username{N}."
    error_message = None

    if not args[0]:
        error_message = "Give me a name, please."

    if error_message:
        print(usage_message)
        raise KeyError(error_message)

    result = contacts.remove_record(args[0])

    if result:
        return f"Contact {args[0]} was removed."
    return f"{R}Contact {args[0]} not in address book{N}."


@input_error
def set_phone(*args):
    """Додає телефонный номер в контакт по імені."""

    usage_message = f"Example of usage: {G}set phone {Y}Username 0985467856{N}"
    error_messageK, error_messageV = None, None

    if not args[0]:
        error_messageK = "Give me a name, please."
    if not args[1]:
        error_messageV = "Give me a phone, please."

    if error_messageK:
        print(usage_message)
        raise KeyError(error_messageK)
    if error_messageV:
        print(usage_message)
        raise ValueError(error_messageV)

    contacts.add_phone(args[0], args[1])

    return f"I added a phone {args[1]} to contact {args[0]}"


@input_error
def remove_phone(*args):
    """Видаляє телефонный номер в контакт по імені."""

    usage_message = f"Example of usage: {G}remove phone {Y}Username 1{N}"
    error_message = None
    if not args[0]:
        error_message = "Give me a name, please."
    elif not args[1]:
        error_message = "Give me an index of phone, please."
    elif not args[1].isdigit():
        error_message = "Index of phone must be a number."
    if error_message:
        print(usage_message)
        raise ValueError(error_message)

    result = contacts.delete_phone_by_index(args[0], int(args[1]) - 1)
    if result:
        return f"I removed a phone of contact {args[0]}"
    return f"{R}No contact {args[0]} in AddressBook.{N}"


@input_error
def set_email(*args):
    """Додає email адресу в контакті по імені."""

    usage_message = f"Example of usage: {G}set email {Y}Username my_mail@i.ua{N}"
    error_messageK, error_messageV = None, None

    if not args[0]:
        error_messageK = "Give me a name, please"

    if not args[1]:
        error_messageV = "Give me a email, please"

    if error_messageK:
        print(usage_message)
        raise KeyError(error_messageK)
    if error_messageV:
        print(usage_message)
        raise ValueError(error_messageV)

    contacts.add_email(args[0], args[1])

    return f"I added a email {args[1]} to contact {args[0]}"


@input_error
def remove_email(*args):
    """Видаляє email номер в контакт по імені."""

    usage_message = f"Example of usage: {G}remove email {Y}Username 1{N}"
    error_message = None
    if not args[0]:
        error_message = "Give me a name, please"
    elif not args[1]:
        error_message = "Give me an index of email, please."
    elif not args[1].isdigit():
        error_message = "Index of email must be a number."
    if error_message:
        print(usage_message)
        raise ValueError(error_message)

    result = contacts.delete_email_by_index(args[0], int(args[1]) - 1)

    if result:
        return f"I removed a email of contact {args[0]}"
    return f"{R}No contact {args[0]} in AddressBook.{N}"


@input_error
def set_address(*args):
    """Додає адресу в контакт по імені."""

    usage_message = f"Example of usage: {G}set address {Y}Username Address of user{N}"
    error_messageK, error_messageV = None, None

    if not args[0]:
        error_messageK = "Give me a name, please"

    if not args[1]:
        error_messageV = "Give me an address, please"

    if error_messageK:
        print(usage_message)
        raise KeyError(error_messageK)
    if error_messageV:
        print(usage_message)
        raise ValueError(error_messageV)

    contacts.add_address(args[0], args[1])

    return f"I added a address {args[1]} to contact {args[0]}"


@input_error
def remove_address(*args):
    """Видаляє email в контакті по імені."""

    usage_message = f"Example of usage: {G}set address {Y}Username Address of user{N}"
    error_message = None

    if not args[0]:
        error_message = "Give me a name, please."

    if error_message:
        print(usage_message)
        raise ValueError(error_message)

    result = contacts.remove_address(args[0])
    if result:
        return f"I removed a address of contact {args[0]}"
    return f"{R}No contact {args[0]} in AddressBook.{N}"


@input_error
def set_birthday(*args):
    """Функція-handler додає день народження до контакту."""

    usage_message = f"Example of usage: {G}set birthday {Y}Username 13.03.1989{N}"
    error_messageK, error_messageV = None, None

    if not args[0]:
        error_messageK = "Give me a name, please"

    if not args[1]:
        error_messageV = "Give me an birthday in format DD.MM.YYYY, please"

    if error_messageK:
        print(usage_message)
        raise KeyError(error_messageK)
    if error_messageV:
        print(usage_message)
        raise ValueError(error_messageV)

    contacts.add_birthday(args[0], args[1])

    return f"I added a birthday {args[1]} to contact {args[0]}"


@input_error
def upcoming_birthdays(*args):
    if not args[0]:
        raise TypeError("Set days you interested")
    days = int(args[0])
    result = contacts.upcoming_birthdays(days)
    return f"{N}{build_contacts_table(result)}{N}"


@input_error
def change_name(*args):
    usage_message = f"Example of usage: {G}change name {Y}Old_name New_name{N}"
    error_message = None

    if not args[0]:
        error_message = "Give me a some name, please"

    if not args[1]:
        error_message = "Give me a new name, please"

    if error_message:
        print(usage_message)
        raise ValueError(error_message)

    result = contacts.update_name(args[0], args[1])
    if result:
        return f"I updatw name {args[0]} -> {args[1]}"
    return f"{R}No contact {args[0]} in AddressBook.{N}"


@input_error
def search_contact(*args):
    if not args[0]:
        raise KeyError("Give me a some name, please")

    results = contacts.find_records(args[0])

    if results:
        return f"{N}{build_contacts_table(results)}{N}"
    return "By your request found nothing"


@input_error
def show_contact(*args):
    if not args[0]:
        raise KeyError("Give me a some name, please")
    result = contacts.find_contact_by_name(args[0])
    if result is not None:
        return f"{N}{build_contacts_table(result)}{N}"
    return f"{R}Contact {args[0]} not found.{N}"


def build_contacts_table(contacts):
    table = ColorTable(theme=Themes.OCEAN)
    table.field_names = ["#", "Name", "Birthday", "Phones", "Emails", "Address"]
    table.align["Emails"] = "l"
    # table.set_style(SINGLE_BORDER)
    for i, record in enumerate(contacts):
        birthday = record.birthday[0].value if record.birthday else "-"
        address = record.address[0] if record.address else "-"
        phones_str = _get_phones_str(record.phones)
        emails_str = _get_emails_str(record.emails)
        table.add_row(
            [
                f"{W}{i + 1}{N}",
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
        phones_str += f"{W}{i+1}. {B}{phone.value}{N}\n"
    return phones_str[:-1]


def _get_emails_str(emails):
    if not emails:
        return "-"
    emails_str = ""
    for i, email in enumerate(emails):
        emails_str += f"{W}{i+1}. {P}{email.value}{N}\n"
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
            table = build_contacts_table(tab)
            # table.align["Emails"] = "l"
            # Обновляем номера контактов в колонке #
            for i, row in enumerate(table._rows):
                row[0] = current_contact_num + i
            print(table)
            # Обновляем текущий номер контакта
            current_contact_num += len(tab)
    return f"Address book contain {len(contacts)} contact(s)."


# ============================= Команди для нотаток ========================= #


@input_error
def add_note(*args):
    usage_message = f"Example of usage: {G}add note {Y}Tag Text{N}"
    error_message = None
    if not args[0]:
        error_message = "Give me a tag and text, please."
    if not args[1]:
        error_message = "Give me a text, please."
    if args[0] is not None and args[0].isdigit():
        error_message = "Tag cannot be a number."
    if error_message:
        print(usage_message)
        raise ValueError(error_message)

    notebook.add_note([args[0]], args[1])
    return "I added note"


@input_error
def remove_note(*args):
    if not args[0]:
        raise ValueError("Give me an index first.")
    if not args[0].isdigit():
        raise ValueError("Index must be a number.")
    notebook.remove_note(int(args[0]))
    return "I removed note"


@input_error
def add_tag(*args):
    usage_message = f"Example of usage: {G}add tag {Y}1 Tag{N}"
    error_message = None
    if args[0] is None:
        error_message = "Give me an index first, please."
    elif not args[0].isdigit():
        error_message = "Index must be a number."
    elif args[1] is None:
        error_message = "Give me a tag, please."
    elif args[1].isdigit():
        error_message = "Tag cannot be a number."

    if error_message:
        print(usage_message)
        raise ValueError(error_message)

    notebook.add_tag(int(args[0]), args[1])
    return f"I added tag {args[1]} to note {args[0]}."


def build_notes_table(notes, original_indices=False):
    table = ColorTable(theme=Themes.OCEAN)
    table.field_names = ["Index", "Tags", "Creation Date", "Text"]
    table.max_width["Text"] = 79
    # table.set_style(SINGLE_BORDER)
    for note, index in notes:
        if original_indices:
            index = notebook.data.index(note)
        date_str = note.date.strftime("%Y-%m-%d %H:%M:%S")
        table.add_row(
            [
                f"{W}{index}{N}",
                G + ", ".join(note.tags) + N,
                f"{Y}{date_str}{N}",
                f"{B}{note.text}{N}",
            ],
            divider=True,
        )
    return table


# @input_error
def show_notes(*args):
    if args[0] is None or not args[0].isdigit():
        notes = notebook.display_notes(tag=args[0] or None, original_indices=True)
        print(build_notes_table(notes, original_indices=True))
    else:
        n = int(args[0])
        for i, tab in enumerate(notebook.iterator_notes(n)):
            if tab == "continue":
                input(G + "Press <Enter> to continue..." + N)
            else:
                table = build_notes_table(tab)
                print(table)
    return f"Notes book contain {len(notebook)} note(s)."


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
    if not args[0]:
        raise ValueError("Give me a filename")
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
def remove_tag(*args):
    if not args[0]:
        raise ValueError("Give me an index first.")
    if not args[0].isdigit():
        raise ValueError("Index must be a number.")
    if not args[1]:
        raise ValueError("Give me a tag, please.")

    result = notebook.remove_tag(int(args[0]), args[1])
    if result:
        return f"I changed tag {args[1]} for note with index {args[0]}"
    else:
        raise ValueError(f"Tag {args[1]} not found for this note")


@input_error
def load_notes(*args):
    if not args[0]:
        raise ValueError("Give me a filename")

    home_path = Path.home()
    file_path = home_path / args[0]
    if PickleStorage.is_file_exist(file_path):
        notebook.clear()
        notebook.update(PickleStorage.import_file(file_path))
        return f"File {args[0]} loaded"
    else:
        raise FileNotFoundError


# ================================ Валюта =================================== #


def get_currency_table(currency_list: CurrencyList):
    table = ColorTable(theme=Themes.OCEAN)
    table.max_width["Currency"] = 30
    table.max_width["Short Name"] = 15
    table.max_width["Rate"] = 10
    table.align["Short Name"] = "c"
    table.align["Rate"] = "c"
    table.field_names = ["Currency", "Short Name", "Rate"]
    for currency in currency_list.get_currency_rates():
        table.add_row([currency.name, currency.cc, currency.rate])
    return table


@input_error
def get_currency(*args):
    return get_currency_table(CurrencyList())


# =============================== Погода ==================================== #

#! Не реалізовано пошук по україномовни словам


def get_weather(*args):
    city = args[0]
    url = f"https://ua.sinoptik.ua/погода-{city}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    temperature = soup.select_one(".today-temp")
    description = soup.select_one(".description")

    if temperature and description:
        temperature = temperature.text
        description = description.text.strip()

        table = ColorTable(theme=Themes.OCEAN)
        table.field_names = ["City", "Temperature", "Description"]
        table.add_row([f"{Y}{city}{N}", f"{G}{temperature}{N}", description])
        table._max_width = {"Description": 79}

        return table
    else:
        return f"Unable to find weather information for {city}."


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
def sort_folder_cli(*args):
    if not args[0]:
        raise ValueError("Give me a folder name, please.")
    return sort_folder(args[0])


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
    "show contact": show_contact,
    "remove contact": remove_contact,
    "change name": change_name,
    "save": save,
    "load": load,
    # --- Валюта ---
    "currency": get_currency,
    # --- Погода ---
    "weather in": get_weather,
    # --- Manage notes ---
    "add note": add_note,
    "add tag": add_tag,
    "remove note": remove_note,
    "show notes": show_notes,
    "save notes": save_notes,
    "load notes": load_notes,
    "search notes": search_notes,
    "change note": change_note,
    "remove tag": remove_tag,
    # --- Sorting folder commnad ---
    "sort folder": sort_folder_cli,
    # --- Googd bye commnad ---
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    "cls": cls,
}


class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        text_before_cursor = document.current_line_before_cursor
        command, _, rest = text_before_cursor.partition(" ")
        if not rest:
            matches = [c for c in COMMANDS if c.startswith(command)]
            for m in matches:
                yield Completion(m, display=m, start_position=-len(command))
        # else:
        #     matches = [c for c in COMMANDS if c.startswith(command)]
        #     for m in matches:
        #         usage = COMMAND_USAGE.get(m, "")
        #         yield Completion(usage, display=usage)


# COMMAND_USAGE = {
#     "add contact": "Someone 03.05.1995",
#     "set phone": "Username 0935841245",
#     "remove phone": "Username 12.12.1978",
#     "set email": "my_name@gmail.com",
#     "remove email": "rUsername 2",
#     "set address": "",
#     "remove address": "",
#     "set birthday": "Username 12.12.1978",
#     "upcoming birthdays": "5",
#     "show contacts": "",
#     "search contact": "SearchQuery",
#     "show contact": "Username",
#     "remove contact": "Username",
#     "change name": "Username Bobo",
# }


session = PromptSession(completer=CommandCompleter(), complete_while_typing=True)

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
        inp = session.prompt(
            ">>> ",
            auto_suggest=AutoSuggestFromHistory(),
        )
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
HELLO_MESSAGE = f"{N}Hello, I'm an assistant v1.0.0 {G}(c) Team-9, GoIT 2023.{N}\nType {Y}help{N} for more information.{N}"


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
        if command.strip() == "*":
            return

        params = parse_command(command)
        handler = get_handler(*params)
        response = handler(*params[1:])
        print(f"{G}{response}{N}")

        if response == "Good bye!":
            return None


# ================================ main program ============================= #

if __name__ == "__main__":
    main()
