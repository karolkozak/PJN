from WNQuery import *

WNQUERY = WNQuery("plwordnet-3.1-visdisc.xml")

TOKENS_GROUP_1 = {'szkoda': 1, 'strata': 1, 'uszczerbek': 1, 'szkoda majątkowa': 1, 'uszczerbek na zdrowiu': 1, 'krzywda': 1,
         'niesprawiedliwość': 1, 'nieszczęście': 2}
TOKENS_GROUP_2 = {'wypadek': 1, 'wypadek komunikacyjny': 1, 'kolizja': 2, 'zderzenie': 2, 'kolizja drogowa': 1,
                      'katastrofa budowlana': 1, 'wypadek drogowy': 1}

L_C_SYNSETS = [(WNQUERY.lookUpSense('szkoda', 2, 'n'), WNQUERY.lookUpSense('wypadek', 1, 'n')),
               (WNQUERY.lookUpSense('kolizja', 2, 'n'), WNQUERY.lookUpSense('szkoda majątkowa', 1, 'n')),
               (WNQUERY.lookUpSense('nieszczęście', 2, 'n'), WNQUERY.lookUpSense('katastrofa budowlana', 1, 'n'))]
L_C_NAMES = ['szkoda - wypadek', 'kolizja - szkoda majątkowa', 'nieszczęście - katastrofa budowlana']
