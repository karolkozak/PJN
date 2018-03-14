import data as d
import json
import matplotlib.pyplot as plt
import re
import operator
import pickle
from collections import Counter


def read_file(fileName):
    with open(fileName, 'r', encoding="utf8") as file:
        d.ALL_JUDGMENTS = json.load(file)["items"]


def filter_judgements():
    for judgment in d.ALL_JUDGMENTS:
        if d.YEAR in judgment["judgmentDate"]:
            d.JUDGMENTS.append(judgment)
    d.clear_all_judgments()


def create_judgments_word_dictionary():
    length = len(d.JUDGMENTS)
    for index in range(length):
        judgment = d.JUDGMENTS.pop()
        temp = re.sub(d.HTML_REGEX, '', judgment['textContent'])
        temp = re.sub(d.NEW_LINE_SIGN, '', temp)
        judgment_words = re.findall(d.STRINGS_TO_CATCH_REGEX, temp)
        temp = list()
        for word in judgment_words:
            if len(word) > 1:
                temp.append(word)
        temp = [x.lower() for x in temp]
        d.WORD_FREQUENCY_LIST.extend(temp)


def sort_dictionary():
    d.WORD_FREQUENCY_LIST = Counter(d.WORD_FREQUENCY_LIST)
    d.WORD_FREQUENCY_LIST = sorted(d.WORD_FREQUENCY_LIST.items(), key=operator.itemgetter(1), reverse=False)
    length = len(d.WORD_FREQUENCY_LIST)
    temp_dict = {}
    for index in range(length):
        word_tuple = d.WORD_FREQUENCY_LIST.pop()
        temp_dict[word_tuple[0]] = word_tuple[1]
    d.WORD_FREQUENCY_LIST = temp_dict
    print('Dictionary length: %s' % len(d.WORD_FREQUENCY_LIST))


def write_to_file(file, data):
    with open(file, 'wb') as fp:
        pickle.dump(data, fp)


def read_from_file(file):
    with open(file, 'rb') as fp:
        data = pickle.load(fp)
    return data


def read_and_store_polimorfologik():
    file_name = '../resources/polimorfologik/polimorfologik-2.1.txt'
    with open(file_name, 'r', encoding="utf8") as f:
        content = f.readlines()
    for line in content:
        split_line = line.split(';')
        d.POLIMORFOLOGIK_LIST.append(split_line[0].lower())
        d.POLIMORFOLOGIK_LIST.append(split_line[1].lower())
    temp_set = set(d.POLIMORFOLOGIK_LIST)
    d.POLIMORFOLOGIK_LIST = list(temp_set)
    print("lenght %s" % len(d.POLIMORFOLOGIK_LIST))
    write_to_file('temp/polimorfologik_list', d.POLIMORFOLOGIK_LIST)


def find_word_not_contained_in_polimorfologik():
    d.NOT_EXIST_IN_POLIMORFOLOGIK = list(set(d.WORD_FREQUENCY_LIST) - set(d.POLIMORFOLOGIK_LIST))
    print('30 przykładowych słów, które nie należą do słownika:')
    for index in range(30):
        print(d.NOT_EXIST_IN_POLIMORFOLOGIK[index])
        d.CHOOSEN_30_WORDS.append(d.NOT_EXIST_IN_POLIMORFOLOGIK[index])


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def levenshtein_correct_words():
    suggestions = list()
    print('30 przykładowych poprawionych słów, które nie należą do słownika:')
    for word in d.NOT_EXIST_IN_POLIMORFOLOGIK:
        best_match = None
        dist = 9999
        for suggestion in d.WORD_FREQUENCY_LIST:
            if suggestion == word:
                continue
            new_dist = levenshtein_distance(suggestion, word)
            if new_dist < dist:
                best_match = suggestion
                dist = new_dist
        suggestions.append(best_match)
        print('%s => %s' % (word, best_match))


def draw_histogram(data):
    to_diagram = list()
    for value in data.values():
        to_diagram.append(value)
    plt.loglog(range(len(to_diagram)), to_diagram)
    plt.title('Histogram liczby wystąpień słów na pozycji w skali logarytmicznej')
    plt.xlabel('Pozycja na liście frekwencyjnej')
    plt.ylabel('Liczba wystąpień słowa na pozycji')
    plt.show()


for i in range(549, 1011):
    fileName = '../resources/json/judgments-' + str(i) + '.json'
    read_file(fileName)
    filter_judgements()

create_judgments_word_dictionary()
sort_dictionary()
write_to_file('temp/sorted_frequency_list', d.WORD_FREQUENCY_LIST)
d.WORD_FREQUENCY_LIST = read_from_file('temp/sorted_frequency_list')

index = 0
for k in d.WORD_FREQUENCY_LIST:
    if index == 10:
        break
    print(k, d.WORD_FREQUENCY_LIST[k])
    index += 1
draw_histogram(d.WORD_FREQUENCY_LIST)

d.POLIMORFOLOGIK_LIST = read_from_file('temp/polimorfologik_list')
find_word_not_contained_in_polimorfologik()
levenshtein_correct_words()

# for read and store as list polimorfologik library
# read_and_store_polimorfologik()
