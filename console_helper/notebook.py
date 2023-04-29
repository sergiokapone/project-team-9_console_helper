from collections import UserDict
from datetime import datetime


class Notebook(UserDict):
    id_count = 1

    def add_record(self, record):
        self.data[str(Notebook.id_count)] = record
        Notebook.id_count += 1

    def delete_record_by_id(self, record_id):
        if self.data[record_id]:
            del self.data[record_id]

    def find_record_by_tags(self, tag):
        result = []
        for record in self.data.values():
            for tag_ in record.tags:
                if tag == str(tag_):
                    result.append(str(record) + " ")
        if result:
            return result
        return f"Tag '{tag}' not found"

    def find_record_by_text(self, text_part):

        for record in self.data.values():
            if text_part in record.text:
                return record
        return f"The text '{text_part}' not found"

    def find_record_by_date(self, date):
        for record in self.data.values():
            if date == record.date:
                return record
        return f"Not found"

    def find_record_by_id(self, id_record):
        return self.data[str(id_record)] if str(id_record) in self.data else "Not found"


class Field:
    def __init__(self, value):
        self.value = value


class Tags(Field):
    def __str__(self):
        return self.value


class Record:
    def __init__(self, text):
        self.text = text
        self.tags = set()
        self.date = datetime.today().strftime("%d %B %Y")

    def add_tag(self, tag):
        self.tags.add(Tags(tag))

    def change_text(self, new_text):
        self.text = new_text

    def __str__(self):
        result = self.text + " ("
        for tag in self.tags:
            result += str(tag) + ", "
        return result + ") " + self.date


notebook = Notebook()

record1 = Record("Some text")
record2 = Record("Another some text")

record1.add_tag("work")
record1.add_tag("job")
record2.add_tag("work")

notebook.add_record(record1)
notebook.add_record(record2)

record1.change_text("What doesn't kill you makes you stronger")
print(notebook.find_record_by_id(1))
