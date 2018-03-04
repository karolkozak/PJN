YEAR = "2013"
ALL_JUDGMENTS = list()
JUDGMENTS = list()
NORMALIZED_VALUES = list()
MONEY_VALUES = list()

MONEY_REGEX = "|".join([
        r'\d[\d.,]*\s*zł\b',
        r'\d[\d.,]*\s*\D*\s+zł\b',
        r'\d[\d.,]*\s*złotych',
        r'\d[\d.,]*\s*\D*\s+złotych',
        r'\d[\d.,]*\s*złote',
        r'\d[\d.,]*\s*\D*\s+złote',
    ])

DAMAGE_REGEX = "|".join([
    r'\bszkoda\b', r'\bszkody\b', r'\bszkodzie\b', r'\bszkodę\b', r'\bszkodą\b', r'\bszkodzie\b',  # l. p.
    r'\bszkód\b', r'\bszkodom\b', r'\bszkodami\b', r'\bszkodach\b'])  # l. m.


def clear_all_judgments():
    global ALL_JUDGMENTS
    ALL_JUDGMENTS = list()
