import data as d
import json
import re
from collections import Counter, OrderedDict
import math
import numpy as np


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
            temp.append(word)
        temp = [x.lower() for x in temp]
        d.WORD_LIST.extend(temp)


def create_bigrams_list():
    length = len(d.WORD_LIST)
    for i in range(0, length - 1):
        d.BIGRAMS_LIST.append(d.WORD_LIST[i] + ' ' + d.WORD_LIST[i + 1])


def pmi(word_1, word_2, words_sum, bigram_sum):
    p_word_1 = d.WORD_FREQUENCY_LIST[word_1] / words_sum
    p_word_2 = d.WORD_FREQUENCY_LIST[word_2] / words_sum
    p_word_1_word_2 = d.BIGRAMS_FREQUENCY_LIST[" ".join([word_1, word_2])] / bigram_sum
    return math.log(p_word_1_word_2/float(p_word_1 * p_word_2), 2)


def calculate_pmi():
    # use d.WORD_FREQUENCY_LIST and d.BIGRAMS_FREQUENCY_LIST
    words_sum = float(sum(d.WORD_FREQUENCY_LIST.values()))
    bigram_sum = float(sum(d.BIGRAMS_FREQUENCY_LIST.values()))
    for bigram in d.BIGRAMS_FREQUENCY_LIST.keys():
        word_1, word_2 = bigram.split(' ')
        bigram_pmi = pmi(word_1, word_2, words_sum, bigram_sum)
        d.BIGRAMS_PMI[bigram] = bigram_pmi


def H(k):
    n = np.sum(k)
    return np.sum((k / n) * np.log(k / n + (k == 0)))


def llr(k):
    return 2 * np.sum(k) * (H(k) - H(k.sum(axis=1) - H(k.sum(axis=0))))


def calculate_llr():
    # use d.WORD_FREQUENCY_LIST and d.BIGRAMS_FREQUENCY_LIST and sum(d.BIGRAMS_FREQUENCY_LIST.values())
    k = np.array([[0, 0], [0, 0]])
    for bigram in d.BIGRAMS_FREQUENCY_LIST:
        word_1, word_2 = bigram.split(' ')
        k[0][0] = d.BIGRAMS_FREQUENCY_LIST[bigram]
        k[0][1] = d.WORD_FREQUENCY_LIST[word_2] - k[0][0]
        k[1][0] = d.WORD_FREQUENCY_LIST[word_1] - k[0][0]
        k[1][1] = sum(d.BIGRAMS_FREQUENCY_LIST.values()) - k[0][0] - k[0][1] - k[1][0]
        d.BIGRAMS_LLR[bigram] = llr(k)


def sort_dictionary(dictionary):
    return OrderedDict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))


for i in range(549, 1011):
    fileName = '../resources/json/judgments-' + str(i) + '.json'
    read_file(fileName)
    filter_judgements()

create_judgments_word_dictionary()
create_bigrams_list()
d.WORD_FREQUENCY_LIST = Counter(d.WORD_LIST)
d.BIGRAMS_FREQUENCY_LIST = Counter(d.BIGRAMS_LIST)

print('Length of bigrams list %s' % len(d.BIGRAMS_LIST))
d.clear_words_bigrams_lists()

calculate_pmi()
d.BIGRAMS_PMI = sort_dictionary(d.BIGRAMS_PMI)

print('PMI:')
index = 0
for value in d.BIGRAMS_PMI:
    print(value + ', ', end='')
    if index == 29:
        print('')
        break
    index += 1

calculate_llr()
d.BIGRAMS_LLR = sort_dictionary(d.BIGRAMS_LLR)

print('LLR:')
index = 0
for value in d.BIGRAMS_LLR:
    if index == 0:
        print(value + ' ' + str(d.BIGRAMS_LLR[value]))
    print(value + ', ', end='')
    if index > 30:
        print('')
        break
    index += 1
