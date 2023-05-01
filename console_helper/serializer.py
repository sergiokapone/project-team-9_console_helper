"""Класи реалызують збереження книги контактыв та нотатника"""

import pickle
from pathlib import Path


class Storage:
    def export_file(object, filename: str):
        raise NotImplementedError

    def import_file(object, filename: str):
        raise NotImplementedError


class PickleStorage(Storage):
    @staticmethod
    def export_file(obj, filename):
        filename = Path(filename)
        with filename.open(mode="wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def import_file(filename):
        filename = Path(filename)
        with filename.open(mode="rb") as file:
            return pickle.load(file)

    @staticmethod
    def is_file_exist(filename):
        filename = Path(filename)
        if filename.exists():
            return True
        return False
