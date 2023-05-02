from collections import namedtuple, UserList
from datetime import datetime
from prettytable import PrettyTable

Note = namedtuple("Note", ["tags", "date", "text"])


class Notebook(UserList):
    def update(self, notes):
        """Оновлює нотатки. Треба для читання з файлу"""
        self.data.clear()
        self.data.extend(notes)

    def add_note(self, tags, note_text):
        """Додає нотатку з одним тегом"""
        note = Note(tags=tags, date=datetime.now(), text=note_text)
        self.data.append(note)

    def remove_note(self, index):
        """Видапляє нотатку"""
        self.data.pop(index)

    def display_notes(self, tag=None, original_indices=False):
        """Показывает заметки, может фильтровать по тегу, возвращает исходные индексы если original_indices=True"""
        notes = self.data
        if tag is not None:
            notes = [note for note in notes if tag in note.tags]
        if original_indices:
            notes = [
                (note, index) for index, note in enumerate(self.data) if note in notes
            ]
        return notes

    def find_notes(self, search_term):
        """Шукає нотатки за текстом"""
        search_term = search_term.lower()
        results = []
        for i, note in enumerate(self.data):
            if search_term in note.text.lower():
                results.append((note, i))
        return results

    def sort_notes_by_tag(self):
        """Шукає нотатку за тегом"""
        return sorted(self.data, key=lambda note: tuple(note.tags))

    def add_tag(self, index, tag):
        """Добавляет тег к заметке по индексу."""
        note = self.data[index]
        note_tags = list(note.tags)
        if tag not in note_tags:
            note_tags.append(tag)
            self.data[index] = note._replace(tags=tuple(note_tags))

    def change_note(self, index, new_text):
        """Замінює текст нотатки"""
        note = self.data[index]
        self.data[index] = note._replace(text=new_text)

    def __len__(self):
        return len(self.data)

    def remove_tag(self, index, tag):
        """Видаляє тег із нотатки"""
        note = self.data[index]
        note_tags = list(note.tags)
        if tag in note_tags:
            note_tags.remove(tag)
            self.data[index] = note._replace(tags=tuple(note_tags))
            return True
        return False


# отладка
if __name__ == "__main__":
    notebook = Notebook()
    notebook.add_note(["Rec"], "Mu fully featured class")
    notebook.add_note(["Rec"], "My new note")
    notebook.add_note(["Alarm"], "My new2 note")

    def display_notes_table(notes):
        table = PrettyTable()
        table.field_names = ["Index", "Tags", "Cration Date", "Text"]
        for i, note in enumerate(notes):
            date_str = note.date.strftime("%Y-%m-%d %H:%M:%S")
            table.add_row([i, ", ".join(note.tags), date_str, note.text])
        return table

    notebook.add_tag(0, "Curl")
    notebook.sort_notes_by_tag()
    b = display_notes_table(notebook.display_notes())
    print(b)

    notebook.remove_note(0)
    notebook.edit_note(0, "Wow!")

    a = display_notes_table(notebook.display_notes())
    print(a)
