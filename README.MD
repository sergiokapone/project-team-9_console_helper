# Console Assistant (command project)

Console Assistant is a `python 3.x`-based command-line assistant that allows
you to manage your contacts and notes.

The assistant saves contacts and notes to the folder of the current user.
For example, in `Windows` is a folder `C:Users\<Usaer>\`

## Run Assistant

- Clone repository `https://github.com/sergiokapone/project-team-9_console_helper.git`
- Crate virtual environment in folder contains `setup.py`
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

## Manage notes commands

- `add note`: Adds a note.
- `show notes`: Shows the list of saved notes.
- `search notes`: Searches for a specific note by title or date.
- `remove note`: Removes a note from the list.
- `save`: Saves the data to a file.
- `load`: Loads the data from a file.
- `sort folder`: Sorts the notes in ascending or descending order by date or title.

## Using - Manage contacts

To manage contacts in your address book, You can type commands by following examples:

- `>>> show contacts 3` where `3` is a number of output records, `10` is by default
- `>>> set phone Username 0935841245`
- `>>> set birthday Username 12.12.1978`
- `>>> set email my_name@gmail.com`
- `>>> upcoming birthdays 5`
- `>>> show contact Username`
- `>>> search contact SearchQuery` --- where `SearchQuery` some word
  or part of number for searching
- `>>> remove contact Username`

## Using - Manage notes

To manage contacts in your address book, You can type commands by following examples:

- `>>> add note Tag Text of your note` --- where `Tag` is a tag of your note.
- `>>> add tag 1 Mytag` --- add tag `Mytag` to note with index `1`.
- `>>> remove note 2` --- remove note with index `2`.
- `>>> show notes` --- just show all notes.
- `>>> show notes Rec` --- show all notes with tag `Rec`.
