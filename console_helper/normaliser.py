from transliterate import translit
from string import ascii_letters, digits


def normalise(name):
    transliterated = translit(
        name, language_code="ru", reversed=True
    )  # from latin to cyrillic
    normalized_name = "".join(
        [
            char if char in ascii_letters or char in digits else "_"
            for char in transliterated
        ]
    )
    return normalized_name

