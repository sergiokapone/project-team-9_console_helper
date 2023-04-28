import re
from datetime import datetime, timedelta
from collections import UserDict


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


class Name(Field):
    """Клас --- обов'язкове поле з ім'ям."""

    @Field.value.setter
    def value(self, value):
        self.__value = value


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
        self.__value = date


class Email(Field):
    """Клас --- необов'язкове поле з email"""

    @Field.value.setter
    def value(self, value):
        if not bool(re.match(r"[\w.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}", value)):
            raise ValueError("Email is not valid")
        self.__value = value


class Address(Field):
    """Клас --- необов'язкове поле з адресою"""

    @Field.value.setter
    def value(self, value):
        self.__value = value


class DataFactory:
    def create_data(self, value):
        pass


class NameFactory:
    def create_name(self, name):
        return Name(name)


class PhoneFactory(DataFactory):
    def create_data(self, value):
        return Phone(value)


class BirthdayFactory(DataFactory):
    def create_data(self, value):
        return Birthday(value)


class EmailFactory(DataFactory):
    def create_data(self, value):
        return Email(value)


class AddressFactory(DataFactory):
    def create_data(self, value):
        return Address(value)


FACTORIES = {
    "phone": PhoneFactory(),
    "birthday": BirthdayFactory(),
    "email": EmailFactory(),
    "address": AddressFactory(),
}


class Record(UserDict):
    def __init__(self, name: Name):
        super().__init__()
        self.data["name"] = name

    def add_data(self, data_type, data_value):
        factory = FACTORIES.get(data_type)
        if factory:
            data = factory.create_data(data_value)
            self.data[data_type] = data
        else:
            raise ValueError(f"Invalid data type: {data_type}")

    def show_data(self, data_type):
        data_value = self.data.get(data_type)
        return data_value.value if data_value else "-"

    def remove_data(self, data_type):
        if data_type in self.data:
            del self.data[data_type]
        else:
            raise ValueError(f"Invalid data type: {data_type}")

    def update_data(self, data_type, data_value):
        factory = FACTORIES.get(data_type)
        if factory:
            data = factory.create_data(data_value)
            self.data[data_type] = data
        else:
            raise ValueError(f"Invalid data type: {data_type}")

    def __str__(self):
        return ", ".join([item.value for item in self.data.values()])


class AddressBook(UserDict):
    def add_record(self, record: Record):
        name = record.data["name"].value
        if name in self.data:
            existing_record = self.data[name]
            for data_type, data_value in record.data.items():
                if data_type != "name":
                    existing_record.add_data(data_type, data_value.value)
        else:
            self.data[name] = record

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]

    def find_records(self, search_term):
        return [
            record
            for record in self.data.values()
            if search_term.lower() in str(record).lower()
        ]

    def show_records(self):
        return [record for record in self.data.values()]

    def __str__(self):
        return "\n\n".join([str(record) for record in self.data.values()])

    def upcoming_birthdays(self, days):
        today = datetime.today().date()
        upcoming = today + timedelta(days=days)
        result = []
        for record in self.data.values():
            if "birthday" in record.data:
                birthday = (
                    datetime.strptime(record.data["birthday"].value, "%d.%m.%Y")
                    .replace(year=today.year)
                    .date()
                )
                if birthday.month == 2 and birthday.day == 29:
                    # для високосных годов
                    birthday = datetime(birthday.year + 1, 3, 1).date()
                else:
                    birthday = birthday.replace(year=today.year)
                if today <= birthday <= upcoming:
                    result.append(record)
        return result

    def iterator(self, n: int = 10):
        """Метод ітерується по записам і виводить їх частинами по n-штук."""

        data_items = list(self.data.items())
        for i in range(0, len(data_items), n):
            data_slice = dict(data_items[i : i + n])
            yield data_slice
            if i + n < len(data_items):
                yield "continue"
