YEAR = "2013"
ALL_JUDGMENTS = list()
JUDGMENTS = list()
RECOGNIZED = list()
EXPRESSIONS = list()

HTML_REGEX = r'<[^>]*>'

ROUGHER_REGEX = r'[a-z]+_[a-z]+'

NEW_LINE_SIGN = r'-\n'

URL = "http://ws.clarin-pl.eu/nlprest2/base"

LPMN = 'any2txt|wcrft2|liner2({"model":"n82"})'

USER = "john@doe.com"


def clear_all_judgments():
    global ALL_JUDGMENTS
    ALL_JUDGMENTS = list()
