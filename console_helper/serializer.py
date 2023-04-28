"""Класи реалызують збереження книги контактыв та нотатника"""

import pathlib
import pickle


class Storage:
    def export_file(object, filename: str):
        raise NotImplementedError

    def import_file(object, filename: str):
        raise NotImplementedError


class PickleStorage(Storage):
    @staticmethod
    def export_file(obj, filename):
        home_path = pathlib.Path.home()
        file_path = home_path / filename
        with file_path.open(mode="wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def import_file(filename):
        home_path = pathlib.Path.home()
        file_path = home_path / filename
        with file_path.open(mode="rb") as file:
            return pickle.load(file)

    @staticmethod
    def is_file_exist(filename):
        home_path = pathlib.Path.home()
        file_path = home_path / filename
        if file_path.exists():
            return True
        return False
