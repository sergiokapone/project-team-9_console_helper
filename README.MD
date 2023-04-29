# Console фіішіефте (command project)

Console Assistant is a `python 3.x`-based command-line assistant that allows you to manage your contacts and notes.

## Run Assistant

- To install a module in a virtual environment, type the `install` in console.
- To start the assistant, type `assistant` in console.

## Commands

Console Helper supports the following commands:

- `help`: Displays a list of available commands and their descriptions.
- `hello`: Greets the user.
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
- `add note`: Adds a note.
- `show notes`: Shows the list of saved notes.
- `search notes`: Searches for a specific note by title or date.
- `remove note`: Removes a note from the list.
- `save`: Saves the data to a file.
- `load`: Loads the data from a file.
- `sort folder`: Sorts the notes in ascending or descending order by date or title.
- `good bye`, `close`, `exit`: Exits the program.

## Manage contacts

To manage contacts in your address book, You can type commands by following examples:

- `>>> show contacts 3` where `3` is a number of output records, `10` is by default
- `>>> set phone Username 0935841245`
- `>>> set birthday Username 12.12.1978`
- `>>> set email my_name@gmail.com`
- `>>> upcoming birthdays 5`
- `>>> show contact Username`
- `>>> search contact 123` or `>>> search contact Se`
- `>>> remove contact Username`

## Manage notes

To manage contacts in your address book, You can type commands by following examples:

- `>>> add note Tag Text of your note` --- where `Tag` is a tag of your note,
  and `Text` is a text of your note
