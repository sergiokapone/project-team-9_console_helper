""" ========================== Таблиця транслітерації ======================"""


TRANS = {'а': 'a',
 'А': 'A',
 'б': 'b',
 'Б': 'B',
 'в': 'v',
 'В': 'V',
 'г': 'g',
 'Г': 'G',
 'д': 'd',
 'Д': 'D',
 'е': 'e',
 'Е': 'E',
 'ё': 'e',
 'Ё': 'E',
 'ж': 'j',
 'Ж': 'J',
 'з': 'z',
 'З': 'Z',
 'и': 'i',
 'И': 'I',
 'й': 'j',
 'Й': 'J',
 'к': 'k',
 'К': 'K',
 'л': 'l',
 'Л': 'L',
 'м': 'm',
 'М': 'M',
 'н': 'n',
 'Н': 'N',
 'о': 'o',
 'О': 'O',
 'п': 'p',
 'П': 'P',
 'р': 'r',
 'Р': 'R',
 'с': 's',
 'С': 'S',
 'т': 't',
 'Т': 'T',
 'у': 'u',
 'У': 'U',
 'ф': 'f',
 'Ф': 'F',
 'х': 'h',
 'Х': 'H',
 'ц': 'ts',
 'Ц': 'TS',
 'ч': 'ch',
 'Ч': 'CH',
 'ш': 'sh',
 'Ш': 'SH',
 'щ': 'sch',
 'Щ': 'SCH',
 'ъ': '',
 'Ъ': '',
 'ы': 'y',
 'Ы': 'Y',
 'ь': '',
 'Ь': '',
 'э': 'e',
 'Э': 'E',
 'ю': 'yu',
 'Ю': 'YU',
 'я': 'ya',
 'Я': 'YA',
 'є': 'je',
 'Є': 'JE',
 'і': 'i',
 'І': 'I',
 'ї': 'ji',
 'Ї': 'JI',
 'ґ': 'g',
 'Ґ': 'G'}

""" ==================== Таблиця кодувань =================================="""


# https://www.w3schools.com/charsets/ref_utf_cyrillic.asp

LATIN_CODES = tuple(range(65, 91)) + tuple(range(97, 123))

CYR_CODES = tuple(range(1024, 1280))

OTHER_SYMBOLS = tuple(str(x) for x in range(0, 10)) + tuple()

WILDCARD = '_'

""" ======================== Функця нормалізації ==========================="""


def normalise(file_name):
    """Функція normalize - проводить транслітерацію кирилічного алфавіту.

    """

    trans = ""  # ініціалізаці

    for letter in file_name:
        if ord(letter) in LATIN_CODES or letter in OTHER_SYMBOLS:
            trans += letter
        elif ord(letter) in CYR_CODES:
            trans += TRANS.get(letter)
        else:
            trans += WILDCARD

    return trans
