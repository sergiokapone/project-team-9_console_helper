import shutil
from pathlib import Path
from .file_copies_deleter import copies_deleter

from .normaliser import normalise

from .colors import G, R, N, Y


EXT_FOLDER = {
    ("mp3", "ogg", "waw", "amr"): "audio",
    ("avi", "mp4", "mov", "mkv", "flv"): "video",
    ("jpeg", "png", "jpg", "svg"): "images",
    ("doc", "docx", "txt", "xlsx", "xls", "pptx"): "documents",
    ("djvu", "djv", "pdf", "tiff"): "books",
    ("zip", "gz", "tar", "7z"): "archives",
}

""" ============================= Функці =================================="""


def get_file_cathegory(file: str):
    """Функція повертає назву категорії у відповідності до імені вхідного файлу."""

    the_path = Path(file)
    ext = the_path.suffix.lstrip(".")

    for exts in EXT_FOLDER.keys():
        if ext in exts:
            return EXT_FOLDER[exts]
    return None


def normalise_file_name(file: str):
    """Функція перейменовує файли з використанням функції normalise."""

    the_path = Path(file)
    normalised_name = normalise(the_path.stem)
    new_file_path = the_path.parent.joinpath(
        "".join([normalised_name, the_path.suffix])
    )
    the_path.rename(new_file_path)
    return new_file_path


def create_folders(root):
    """Створює папки каталогів у root"""

    for folder in EXT_FOLDER.values():
        Path(root).joinpath(folder).mkdir(exist_ok=True)


def organize_files(
    path, level=0, known_exts=set(), unknown_exts=set(), categories=set()
):
    """Функція фасує файли по відповідним папкам."""

    the_path = Path(path)
    if level == 0:
        global root_path
        root_path = the_path.resolve()

    for item in the_path.iterdir():
        if item.is_dir() and item.name not in EXT_FOLDER.values():
            organize_files(item.resolve(), level + 1)
        else:
            category = get_file_cathegory(item.name)
            if category:
                # --------------------------
                categories.add(category)
                known_exts.add(item.suffix)
                item = normalise_file_name(item)
                # --------------------------
                root_name = Path(root_path).joinpath(category, item.name)
                shutil.move(item, Path(root_path).joinpath(category))
                if category == "archives":
                    unpack(
                        root_name,
                        Path(root_path).joinpath(category, item.stem),
                    )
            else:
                if item.is_file():
                    unknown_exts.add(item.suffix)
    return tuple(unknown_exts)


def unpack(archive_path, path_to_unpack):
    """Розраковувач файлів."""

    try:
        shutil.unpack_archive(archive_path, path_to_unpack)
    except OSError as er:
        print(er)


def remove_empty(path):
    """Видаляє порожні папки."""

    the_path = Path(path)
    empty = True
    for item in the_path.glob("*"):
        if item.is_file():
            empty = False
        if item.is_dir() and not remove_empty(item):
            empty = False

    if empty:
        path.rmdir()
    return empty


def known_exts(root):
    exts = set()
    for item in Path(root).iterdir():
        if item.is_dir():
            for file in item.iterdir():
                if file.is_file():
                    exts.add(file.suffix)
    return exts


""" ======================== Основна програма =============================="""


def sort_folder(root):
    path = Path(root)
    if not path.is_dir():
        return f"{Y}Warning!{N} The {root} is not a valid path!"

    agreement = input(
        f"{Y}WARNING! {G}Are you sure you want to sort the files in CATALOG {Y + root}{N}? (y/n): "
    )

    if agreement not in ("y", "Y", "yes", "Yes", "YES"):
        return f"{G}Operation approved!{N}"

    copies_deleter(root)
    create_folders(root)
    unknown_exts = organize_files(root)
    remove_empty(root)

    ke = ", ".join([ext for ext in known_exts(root)])
    print(f"{G}Known extensions:{N} {ke}")

    if unknown_exts:
        ue = ", ".join([ext for ext in unknown_exts])
        print(f"{R}Unknown extensions:{N} {ue}")

    for item in path.iterdir():
        if item.is_dir():
            num_of_files = sum(1 for file in item.iterdir() if file.is_file())
            print(
                f"{G}Folder {Y}{item.name}{G} contain {Y}{num_of_files}{G} file(s){N}"
            )

    return f"{G}Folder {Y}{root}{G} sorted!{N}"
