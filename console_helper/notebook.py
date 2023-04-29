from collections import namedtuple, UserList
from datetime import datetime


class Tag:
    ...


class Note(namedtuple):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def set_counter(self):
        max_id = 0
        for tag, notes in self.data.items():
            for note in notes:
                if note["id"] > max_id:
                    max_id = note["id"]
        self.counter = max_id

    def add(self, tag, note_text):
        max_id = max(
            (note.get("id", 0) for notes in self.data.values() for note in notes),
            default=-1,
        )

        note_id = max_id + 1
        note = {"id": note_id, "text": note_text, "created": datetime.now()}
        self.data.setdefault(tag, []).append(note)
        self.counter = note_id

    def remove_note(self, note_id):
        for tag, notes in self.data.items():
            for i, note in enumerate(notes):
                if note["id"] == int(note_id):
                    del self.data[tag][i]
                    break

    def display(self, tag=None):
        return self

    def find_notes(self, search_term):
        result = {}
        for tag, notes in self.data.items():
            matching_notes = [
                note
                for note in notes
                if search_term.lower() in str(note["text"]).lower()
            ]
            if matching_notes:
                result[tag] = matching_notes
        return result

    def sort_notes_by_tag(self):
        sorted_notes = {}
        for tag in sorted(self.data.keys()):
            sorted_notes[tag] = self.data[tag]
        return sorted_notes


class Notebook(UserList):
    def add_note(self, text: Note, tag: Tag):
        ...

    def remove_note(self, id):
        ...

    def change_note(self, id):
        ...
