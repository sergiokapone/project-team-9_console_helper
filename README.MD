# Console Assistant

Console Assistant is a `python 3.x`-based command-line program that allows
you to manage your contacts and notes, sort files in a folder by category and delete file copies..

The assistant saves contacts and notes to the folder of the current user.
For example, in `Windows` it's a folder `C:\Users\<User>\`
with names

- `contacts.bin`
- `notes.bin`

  respectively.

## Install and Run Assistant

- Clone repository

```
https://github.com/sergiokapone/project-team-9_console_helper.git
```

- Create virtual environment in folder contains `setup.py`, in command line type

```
python -m venv .venv
```

or

```
py -m venv .venv
```

- Type `activate.cmd` in command line.

- To install a module in a virtual environment, type the `install.cmd` in console.

- To start the assistant, in console type:

```
assistant
```

The following packages are required to install the package:

```txt
prettytable==3.7.0
prompt-toolkit==3.0.0
Pygments==2.15.1
transliterate==1.10.2
```

Install requirements

```
pip install -r requirements.txt
```

## Commands

### Hello and welcome commands

- `help`: Displays a list of available commands and their descriptions.
- `hello`: Greets the user.
- `good bye`, `close`, `exit`: Exits the program with saving data.
- `.`: exits the program without messages with saving data.
- `*`: exits the program without messages without saving data.

### Manage contacts commands

- `add contact`: Add a contact to the address book.
- `set phone:` Allows the user to set their phone number.
- `remove phone:` Removes the user phone number.
- `set email`: Allows the user to set their email address.
- `remove email:` Removes the user email.
- `set address`: Allows the user to set their address.
- `remove address:` Removes the user address.
- `set birthday`: Allows the user to set their birthday.
- `upcoming birthdays`: Shows the list of upcoming birthdays.
- `show contacts`: Shows the list of saved contacts.
- `show contact`: Shows the details of a specific contact.
- `search contact`: Searches for a specific contact by name.
- `remove contact`: Removes a contact from the list.
- `change name`: Change name of contact.
- `save`: save contacts to file.
- `load`: load contacts from file.

### Currency exchange"

- `currency`: Get Currency exchange.

### Sorting Folder

- `sort folder`: Sort folder.

### Manage notes commands

- `add note`: Adds a note.
- `show notes`: Shows the list of saved notes.
- `search notes`: Searches for a specific note by title or date.
- `remove note`: Removes a note from the list.
- `save notes`: Saves the notes to a file.
- `load notes`: Loads the notes from a file.
- `change note`: Edit note by index.
- `remove tag`: Removes Tag for specified note index.

## Usage Examples

### Sort folder

- `>>> sort folder D:\MyGarbage\` --- sort files in folder `D:\MyGarbage\`

### Manage contacts

To manage contacts in your address book, You can type commands by following examples:

- `>>> show contacts` --- shows table of contacts in address book.
- `>>> show contacts 3` displaying contacts in chunks of `3` items, `20` is by default
- `>>> add contact Username` --- add empty contact `Username` to the address book.
- `>>> add contact Someone 03.05.1995 his_mail@i.ua` --- add contact `Someone` to the address book with date of birthday `03.05.1995` and email `his_mail@i.ua`[^2].
- `>>> set phone Username 0935841245` --- add phone[^1] to contact `Username` in address book.
- `>>> set birthday Username 12.12.1978` --- add birthday[^1] to contact `Username` in address book.
- `>>> set email my_name@gmail.com` --- add email[^1] `my_name@gmail.com` to contact `Username` in address book.
- `>>> upcoming birthdays 5` --- shows contacts with upcoming birthdays within `5` days.
- `>>> show contact Username` --- show contact `Username` information.
- `>>> search contact SearchQuery` --- where `SearchQuery` some word or number for searching.
- `>>> remove contact Username` --- remove contact `Uresname`
- `>>> remove phone Username 1` --- remove user phone by index `1`.
- `>>> remove email Username 2` --- remove user email by index `2`.
- `>>> change contact Username Bobo` --- change contact name `Uresname` to new name `Bobo`.

[^1]: If the contact is missing, it will be added automatically.

[^2]: Order doesn't matter.

### Manage notes

To manage contacts in your address book, You can type commands by following examples:

- `>>> show notes` --- just show all notes.
- `>>> show notes Rec` --- show all notes with tag `Rec`.
- `>>> show notes 3` --- displaying notes in chunks of `3` items.
- `>>> add note Tag Text of your note` --- add note with `Tag`[^3] and text `Text of your note`.
- `>>> add tag 1 Mytag` --- add tag `Mytag`[^4] to note with index `1`.
- `>>> remove tag 4 Tag` --- removes `Tag` for note with index `4`.
- `>>> change note 1 New text` --- change note `1` with `New text`.
- `>>> remove note 2` --- remove note with index `2`.

[^3]: When creating a note, you can assign only one single-word tag. You can add subsequent tags with `add tag` command.

[^4]: Tag cannot be a number.

### Exit program

To exit the program just type following commands[^5]:

- `>>> good bye`
- `>>> close`
- `>>> exit`

Another possibility to exit without any messages is typing dot:

- `>>> .`

[^5]: After executing the specified commands, the application will save your data automatically.

Upon subsequent program entry, the data will be loaded automatically.

But if you type `*` the application exit without saving your data:

- `>>> *`
