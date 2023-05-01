# Console Assistant (command project)

Console Assistant is a `python 3.x`-based command-line assistant that allows
you to manage your contacts and notes.

The assistant saves contacts and notes to the folder of the current user.
For example, in `Windows` is a folder `C:Users\<Usaer>\`

## Install and Run Assistant

- Clone repository `https://github.com/sergiokapone/project-team-9_console_helper.git`
- Create virtual environment in folder contains `setup.py`
- To install a module in a virtual environment, type the `install.cmd` in console.
- To start the assistant, type `assistant` in console.

## Hello and welcome commands

- `help`: Displays a list of available commands and their descriptions.
- `hello`: Greets the user.
- `good bye`, `close`, `exit`: Exits the program.
- `.` exits the program without messages.

## Manage contacts commands

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
- `save`: save contacts to file.
- `load`: load contacts from file.

## Sorting Folder

- `sort folder`: Sort folder.

## Manage notes commands

- `add note`: Adds a note.
- `show notes`: Shows the list of saved notes.
- `search notes`: Searches for a specific note by title or date.
- `remove note`: Removes a note from the list.
- `save`: Saves the data to a file.
- `load`: Loads the data from a file.
- `sort folder`: Sorts the notes in ascending or descending order by date or title.
- `edit note`: Edit note by index.

## Usage Examples

### Sort folder

- `>>> sort folder D:\MyGarbage\` --- sort files in folder `D:\MyGarbage\`

### Manage contacts

To manage contacts in your address book, You can type commands by following examples:

- `>>> show contacts` --- shows table of contacts in address book.
- `>>> show contacts 3` where `3` is a number of output records, `20` is by default
- `>>> add contact Username` --- add empty contact `Username` to the address book.
- `>>> set phone Username 0935841245` --- add phone[^1] to contact `Username` in address book.
- `>>> set birthday Username 12.12.1978` --- add birthday[^1] to contact `Username` in address book.
- `>>> set email my_name@gmail.com` --- add email[^1] `my_name@gmail.com` to contact `Username` in address book.
- `>>> upcoming birthdays 5` --- shows contacts with upcoming birthdays within `5` days.
- `>>> show contact Username` --- show contact `Username` information.
- `>>> search contact SearchQuery` --- where `SearchQuery` some word or number for searching.
- `>>> remove contact Username` --- remove contact `Uresname`
- `>>> remove phone Username 1` --- remove user phone by index `1`.
- `>>> remove email Username 2` --- remove user email by index `2`.

[^1]: If the contact is missing, it will be added automatically

### Manage notes

To manage contacts in your address book, You can type commands by following examples:

- `>>> add note Tag Text of your note` --- where `Tag`[^2] is a tag of your note.
- `>>> add tag 1 Mytag` --- add tag `Mytag` to note with index `1`.
- `>>> remove note 2` --- remove note with index `2`.
- `>>> show notes` --- just show all notes.
- `>>> show notes Rec` --- show all notes with tag `Rec`.
- `>>> chamge note 1 New text` --- change note `1` with `New text`.

[^2]: When creating a note, you can assign only one tag. You can add subsequent tags with `add tag` command.

### Exit programm

To exit the program just type following commands `good bye`, `close` or `exit`.
Another possibility to exit without any messages is typing `.`.

After executing the specified commands, the application will save your data automatically.
Upon subsequent program entry, the data will be loaded automatically.
