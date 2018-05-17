JUDGMENTS = list()
SENTENCES = list()
TRIGRAM_LIST_SENTENCES = list()
MODEL = []
JUDGMENTS_TEXT = ''

HTML_REGEX = r'<[^>]*>'

NEW_LINE_SIGN = r'-\n'

PHRASES = ["Sąd_Najwyższy", "Trybunał_Konstytucyjny", "kodeks_cywilny", "kpk", "sąd_rejonowy", "szkoda",
           "wypadek", "kolizja", "szkoda_majątkowa", "nieszczęście", "rozwód"]

WORDS_T_SNE = ["szkoda", "strata", "uszczerbek", "uszczerbek_na_zdrowiu", "krzywda",
               "niesprawiedliwość", "nieszczęście"]


def clear_all_judgments():
    global ALL_JUDGMENTS
    ALL_JUDGMENTS = list()
