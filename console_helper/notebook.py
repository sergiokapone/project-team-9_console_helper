from collections import namedtuple, UserList
from datetime import datetime

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
        """Показує нотоатки, може фільтрувати за тегом, повертає вихідні індекси якщо original_indices=True"""
        notes = self.data
        if tag is not None:
            notes = [note for note in notes if tag in note.tags]
        if original_indices:
            notes = [
                (note, index) for index, note in enumerate(self.data) if note in notes
            ]
        return notes

    def iterator_notes(self, n: int = 10):
        """Метод ітерується по записам і виводить їх частинами по n-штук."""
        items = self.data
        for i, note in enumerate(items):
            if i % n == 0:
                items[i : i + n]
                yield [(note, j) for j in range(i, i + n) if j < len(items)]
                if i + n < len(items):
                    yield "continue"

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
        """Додає тег до нотатки за індексом."""
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
