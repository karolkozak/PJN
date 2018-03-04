import json
import re
import data as d
import matplotlib.pyplot as plt
import time


def read_file(fileName):
    with open(fileName, 'r', encoding="utf8") as file:
        d.ALL_JUDGMENTS = json.load(file)["items"]


def filter_judgements():
    for judgment in d.ALL_JUDGMENTS:
        if d.YEAR in judgment["judgmentDate"]:
            d.JUDGMENTS.append(judgment)
    d.clear_all_judgments()


def count_judgments_containing_damage():
    containing_damage = list()
    for judgment in d.JUDGMENTS:
        matches = re.findall(d.DAMAGE_REGEX, judgment["textContent"])
        if matches:
            containing_damage.append(matches)
    print('Liczba orzeczeń zawierających słowo "szkoda" w dowolnej formie fleksyjnej %s' % len(containing_damage))


def count_judgments_by_referenced_regulations():
    referenced_regulations = list()
    for judgment in d.JUDGMENTS:
        for regulation in judgment["referencedRegulations"]:
            journal_title = "Ustawa z dnia 23 kwietnia 1964 r. - Kodeks cywilny"
            if journal_title in regulation["journalTitle"]:
                art_445_regex = r'art\.\s*445'
                art_445 = re.search(art_445_regex, regulation["text"])
                if art_445:
                    referenced_regulations.append(regulation)
                    break
    print('Liczba orzeczeń odwołujących się do artykułu 445 Ustawy z dnia 23 kwietnia 1964 r. - Kodeks cywilny: %s' % len(referenced_regulations))


def search_money_values():
    length = len(d.JUDGMENTS)
    for index in range(length):
        judgment = d.JUDGMENTS.pop()
        matches = re.findall(d.MONEY_REGEX, judgment["textContent"])
        for match in matches:
            if match:
                d.MONEY_VALUES.append(match)


def adjust_big_value(value, multiplier):
    value = re.sub(r'[^\d,]', '', value)
    value = re.sub(r',\d*', '', value)  # remove grosze
    try:
        value = float(value) * multiplier
    except ValueError:
        print(value)
        return 0
    return value


def normalize_values():
    length = len(d.MONEY_VALUES)
    print(length)
    for index in range(length):
        value = d.MONEY_VALUES.pop()
        if "mln" in value:
            value = adjust_big_value(value, 1000000)
        elif "mld" in value:
            value = adjust_big_value(value, 1000000000)
        elif r'tys\b' in value:
            value = adjust_big_value(value, 1000)
        elif "tyś" in value:
            value = adjust_big_value(value, 1000)
        else:
            value = adjust_big_value(value, 1)
        d.NORMALIZED_VALUES.append(value)


def draw_histogram(data, title_part=''):
    print(data)
    print(len(data))
    plt.hist(data, bins=150)
    plt.title('Wartości występujące w orzeczeniach w roku 2013' + title_part)
    plt.xlabel('Wartość pieniężna')
    plt.ylabel('Częstotliwość')
    plt.show()


def divide_values_and_draw_histogram(pivot):
    less_or_equal = [n for n in d.NORMALIZED_VALUES if n <= pivot]
    draw_histogram(less_or_equal, ' do 1 mln')
    greater_than = [n for n in d.NORMALIZED_VALUES if n > pivot]
    draw_histogram(greater_than, ' powyżej 1 mln')


start_time = time.time()

for i in range(1, 3174):
    fileName = '../resources/json/judgments-' + str(i) + '.json'
    read_file(fileName)
    filter_judgements()

count_judgments_by_referenced_regulations()
count_judgments_containing_damage()
search_money_values()
normalize_values()

print('Before drawing: %s' % (time.time() - start_time))

draw_histogram(d.NORMALIZED_VALUES)
divide_values_and_draw_histogram(1000000)
