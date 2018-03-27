YEAR = "2013"
ALL_JUDGMENTS = list()
JUDGMENTS = list()
WORD_LIST = list()
BIGRAMS_LIST = list()
WORD_FREQUENCY_LIST = list()
BIGRAMS_FREQUENCY_LIST = list()
BIGRAMS_PMI = {}
BIGRAMS_LLR = {}

HTML_REGEX = r'<[^>]*>'

NEW_LINE_SIGN = r'-\n'

STRINGS_TO_CATCH_REGEX = r'\b[a-zA-ZąęłćżźóńśŚĄĘŁĆŻŹÓŃ]+\b'


def clear_all_judgments():
    global ALL_JUDGMENTS
    ALL_JUDGMENTS = list()


def clear_words_bigrams_lists():
    global WORD_LIST, BIGRAMS_LIST
    WORD_LIST = list()
    BIGRAMS_LIST = list()
