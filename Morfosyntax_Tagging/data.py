YEAR = "2013"
ALL_JUDGMENTS = list()
JUDGMENTS = list()
JUDGMENTS_CONTENTS = list()
JUDGMENTS_CONTENTS_STRING = ''
TAGGED_JUDMENTS_CONTENTS = []
DOCKER_URL = 'http://localhost:9200'

HTML_REGEX = r'<[^>]*>'

NEW_LINE_SIGN = r'-\n'

STRINGS_TO_CATCH_REGEX = r'\b[a-zA-ZąęłćżźóńśŚĄĘŁĆŻŹÓŃ]+\b'


def clear_all_judgments():
    global ALL_JUDGMENTS
    ALL_JUDGMENTS = list()


def clear_judgments():
    global JUDGMENTS_CONTENTS
    JUDGMENTS_CONTENTS = list()
