from collections import UserList
from datetime import datetime


class Notebook(UserList):
    def add_record(self, record):
        self.data.append(record)

    def delete_record_by_id(self, record_id):
        for order_number, value in enumerate(self.data):
            if order_number == record_id:
                self.data.pop(record_id)
    """Здесь нужно добавить вывод сообщения с информацией об удаленной записи через return 'запись №record_id была удалена' или 'Запись не найдена'"""

    def find_record_by_tag(self, tag):
        result = []  # list of notes with the requested tag
        for record in self.data:
            for tag_ in record.tags:
                if tag == tag_.value:
                    result.append(str(record))

        return result if result else f"Tag '{tag}' not found"

    def find_record_by_text(self, text_part):
        result = []
        if text_part:
            for record in self.data:
                if text_part in record.note.value:
                    result.append(str(record))
            return result if result else f"The text '{text_part}' not found in notes"
        return "You entered an empty string! Please Try again."

    def find_record_by_date(self, date):
        result = []
        for record in self.data:
            if date == record.date:  # date in format 30 April 2023
                result.append(str(record))

        return result if result else "No notes on this day"

    def find_record_by_id(self, id_record):
        pass
    """Реализовать поиск заметки(note) по порядковому номеру - id"""


class Field:
    def __init__(self, value):
        self.value = value


class Tags(Field):
    def __str__(self):
        return self.value


class Note(Field):
    def __str__(self):
        return self.value


class Record:
    def __init__(self, note):
        self.note = Note(value=note)
        self.tags = []
        self.date = datetime.today().strftime("%d %B %Y")  # date in format 30 April 2023

    def add_tag(self, tag):
        self.tags.append(Tags(tag))

    def change_note(self, new_note):
        self.note = Note(value=new_note)

    def __str__(self):
        """Добавить окрашивание тегов в какой-нибуть цвет, чтобы визуально отделить их от основного текста"""
        result = [self.note.value]
        for tag in self.tags:
            result.append(str(tag))
        result.append(self.date)

        return ", ".join(result)


notebook = Notebook()

record1 = Record("Your time is limited, so don’t waste it living someone else’s life. Don’t be trapped by dogma – which is living with the results of other people’s thinking")
record1.add_tag("TAG1")
record1.add_tag("TAG2")


record2 = Record("The big lesson in life, baby, is never be scared of anyone or anything.")
record2.add_tag("TAG1")

notebook.add_record(record1)
notebook.add_record(record2)

record1.change_note("What doesn't kill you makes you stronger")

notebook.delete_record_by_id(0)

print(notebook.find_record_by_tag("TAG1"))
print(len(notebook))
