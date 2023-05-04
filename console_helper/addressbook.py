import re
from datetime import datetime, timedelta
from collections import namedtuple, UserList


class Field:
    """Клас є батьківським для всіх полів, у ньому реалізується логіка,
    загальна для всіх полів."""

    def __init__(self, value: str):
        self.__value = value
        self.value = value

    @property
    def value(self):
        return self.__value

    def __eq__(self, other):
        return self.value == other.value

    # def __str__(self):
    #     return self.value


class Phone(Field):
    """Клас --- необов'язкове поле з телефоном та таких один записів (Record)
    може містити кілька."""

    @Field.value.setter
    def value(self, value):
        if not bool(re.match(r"\d{10}", value)) or len(value) > 10:
            raise ValueError("Phone number must be 10 digits")
        self.__value = value


class Birthday(Field):
    """Клас --- необов'язкове поле з датою народження."""

    @Field.value.setter
    def value(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
        except (TypeError, ValueError):
            raise ValueError("Invalid date format. Please use DD.MM.YYYY")
        if date > datetime.today():
            raise ValueError("Date cannot be in the future")
        self.__value = value


class Email(Field):
    """Клас --- необов'язкове поле з email"""

    @Field.value.setter
    def value(self, value):
        if not bool(re.match(r"[\w.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}", value)):
            raise ValueError("Email is not valid")
        self.__value = value


Record = namedtuple("Record", ["name", "birthday", "phones", "emails", "address"])


class AddressBook(UserList):
    def update(self, records):
        self.data.clear()
        self.data.extend(records)

    def add_record(self, name, birthday=None, phones=None, emails=None, address=None):
        # Проверяем, есть ли уже контакт с таким именем
        for record in self.data:
            if record.name == name:
                # print(f"Contact with {name} already exist!")
                raise ValueError("Contact already exist in AddressBook.")

        # Если контакта с таким именем еще нет, то создаем новый
        birthday = [Birthday(birthday) for birthday in birthday] if birthday else []
        phones = [Phone(phone) for phone in phones] if phones else []
        emails = [Email(email) for email in emails] if emails else []
        address = [address] if address else []
        record = Record(
            name=name,
            birthday=birthday,
            phones=phones,
            emails=emails,
            address=address,
        )
        self.data.append(record)

    def add_phone(self, name, phone):
        for record in self.data:
            if record.name == name:
                record.phones.append(Phone(phone))
                return
        self.add_record(name=name, phones=[phone])

    def add_email(self, name, email):
        for record in self.data:
            if record.name == name:
                record.emails.append(Email(email))
                return
        self.add_record(name=name, emails=[email])

    def add_address(self, name, address):
        for record in self.data:
            if record.name == name:
                record.address.clear()
                record.address.append(address)
                return
        self.add_record(name=name, address=address)

    def remove_record(self, name):
        for record in self.data:
            if record.name == name:
                self.data.remove(record)
                return True
        return False

    def update_name(self, name, new_name):
        for i, record in enumerate(self.data):
            if record.name == name:
                self.data[i] = record._replace(name=new_name)
                return True
        return False

    def remove_address(self, name):
        for record in self.data:
            if record.name == name:
                record.address.clear()
                return True
        return False

    def add_birthday(self, name, birthday):
        for record in self.data:
            if record.name == name:
                record.birthday.clear()
                record.birthday.append(Birthday(birthday))
                return
        self.add_record(name=name, birthday=[birthday])

    def delete_phone_by_index(self, name, phone_index):
        for record in self.data:
            if record.name == name:
                del record.phones[phone_index]
                return True
        return False

    def delete_email_by_index(self, name, email_index):
        for record in self.data:
            if record.name == name:
                del record.emails[email_index]
                return True
        return False

    def upcoming_birthdays(self, days):
        """Метод виводить список контактів у яких день народження протягоь days днів"""
        today = datetime.today().date()
        upcoming = today + timedelta(days=days)
        upcoming_bdays = AddressBook()
        for record in self.data:
            if record.birthday:
                birthday = (
                    datetime.strptime(record.birthday[0].value, "%d.%m.%Y")
                    .replace(year=today.year)
                    .date()
                )
                if birthday.month == 2 and birthday.day == 29:
                    # для високосных годов
                    birthday = datetime(birthday.year + 1, 3, 1).date()
                else:
                    birthday = birthday.replace(year=today.year)
                if today <= birthday <= upcoming:
                    upcoming_bdays.data.append(record)
        return upcoming_bdays

    def find_records(self, search_term):
        found_contacts = AddressBook()

        for record in self.data:
            if (
                search_term in record.name
                or search_term in str(record.address)
                or any(search_term in birthday.value for birthday in record.birthday)
                or any(search_term in phone.value for phone in record.phones)
                or any(search_term in email.value for email in record.emails)
            ):
                found_contacts.append(record)

        return found_contacts

    def find_contact_by_name(self, name):
        for record in self.data:
            if record.name == name:
                return [record]
        return None

    def iterator(self, n: int = 10):
        """Метод ітерується по записам і виводить їх частинами по n-штук."""

        items = sorted(self.data)
        for i in range(0, len(items), n):
            data_slice = items[i : i + n]
            yield data_slice
            if i + n < len(items):
                yield "continue"


# отладка
if __name__ == "__main__":
    contacts = AddressBook()
    # contacts.add_record("Sergiy")
    # contacts.add_phone("Sergiy", "0987654321")
    # contacts.add_phone("Sergiy", "0987654321")
    # contacts.add_phone("Sergiy", "2323456545")
    # contacts.add_email("Sergiy", "qw@df.df")
    # contacts.add_email("Sergiy", "qww@dsdf.dsdf")
    # contacts.add_email("Sergiy", "qww@dsdf.dsdf")
    # contacts.add_address("Sergiy", "Київ де не де")
    # contacts.add_record("Angela")
    # contacts.add_address("Sergiy", "Ytw")
    # contacts.add_birthday("Sergiy", "1.05.1987")
    # contacts.delete_phone_by_index("Sergiy", 2)
    # contacts.delete_email_by_index("Sergiy", 0)
    # contacts.add_record("Lego")
    # print(type(contacts) == AddressBook)
    # # print(contacts.upcoming_birthdays(3))
