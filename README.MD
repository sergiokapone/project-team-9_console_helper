# Домашнє завдання №12


- Записи `Record` у `AddressBook` зберігаються як значення у словнику.
  В якості ключів використовується значення `Record.name.value`.
- `Record` зберігає об'єкт <Name> в окремому атрибуті.
- `Record` зберігає список об'єктів `Phone` в окремому атрибуті.
- `Record` реалізує методи додавання/видалення/редагування об'єктів `Phone`.
- `AddressBook` реалізує метод `add_record`, який додає <Record> у `self.data`.


## Команди
- `hello` --- чат вітається.
- `set birthday` -- встановлює дату народження контакуту у форматі  `DD.MM.YYY`, наприклад `set birthday Sergiy 12.12.1978`.
- `birthday of` -- Виводить на екран дату вказаного контакту, наприклад `birthday of Sergiy`.
- `add` --- чат додає ім'я і телефон, приклад `add Sergiy 0936564532`.
- `chage` --- чат змінює номер для відповідного контакту, приклад `change Sergiy 0936564532 0634564545`.
- `phones` --- чат виводить номери телефонів контакту, приклад `phone Sergiy`.
- `show all N`--- чат показує усі контакти та їх номери, приклад `show all 10`. Необов'язковий параметр `N` - число записів, що виводяться за одну ітерацію.
- `remove` --- чат видаляє запис з вказаним іменем, приклад `remove Sergiy`.
- `good bye`, `good`, `exit` --- чат прощається і завершує роботу і зберігає контакти у файл `contacts.json`.
- `.` --- чат перериває свою роботу без попереджень і зберігає контакти у файл `contacts`.
- `save` --- зберігає контакти у файл `.json`, наприклад `save contacts`.
- `load` --- завантажує книгу з контактами з файлу в чат, наприклад `load contacts`.
- `search` -- здійснює пошук за ключовою фразою, частиною номеру телефона чи дні народження, наприклад `search 123`, або `search Beth`.
- `export` -- Експортує дані в формат `csv`, приклад `export somefile`.
- `import` -- Імпортує дані з формату `csv`, приклад `impott somefile`.


```
COMMANDS = {
    "hello": hello,
    "set birthday": set_birthday,
    "birthday of": birthday,
    "add": add,
    "change": change,
    "phones of": phones,
    "show all": show_all,
    "remove": remove,
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    "save": save,
    "load": load,
    "search": search,
    "export": export_to_csv,
    "import": import_from_csv,
}
```
