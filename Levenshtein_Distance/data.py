YEAR = "2013"
ALL_JUDGMENTS = list()
JUDGMENTS = list()
WORD_FREQUENCY_LIST = list()
POLIMORFOLOGIK_LIST = list()
NOT_EXIST_IN_POLIMORFOLOGIK = list()
CHOOSEN_30_WORDS = list()

HTML_REGEX = r'<[^>]*>'

NEW_LINE_SIGN = r'-\n'

STRINGS_TO_CATCH_REGEX = r'\b[a-zA-ZąęłćżźóńśŚĄĘŁĆŻŹÓŃ]+\b'


def clear_all_judgments():
    global ALL_JUDGMENTS
    ALL_JUDGMENTS = list()
