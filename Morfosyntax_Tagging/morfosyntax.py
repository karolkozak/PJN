import json
import operator
import re
from collections import Counter

import data as d
import requests


def read_file(fileName):
    with open(fileName, 'r', encoding="latin-1") as file:
        d.ALL_JUDGMENTS = json.load(file)["items"]


def filter_judgements():
    for judgment in d.ALL_JUDGMENTS:
        if d.YEAR in judgment["judgmentDate"]:
            d.JUDGMENTS.append(judgment)
    d.clear_all_judgments()


def join_judgments_contents():
    length = len(d.JUDGMENTS)
    for index in range(length):
        judgment = d.JUDGMENTS.pop()
        temp = re.sub(d.HTML_REGEX, '', judgment['textContent'])
        temp = re.sub(d.NEW_LINE_SIGN, '', temp)
        d.JUDGMENTS_CONTENTS.append(temp)
    d.JUDGMENTS_CONTENTS_STRING = ' '.join(d.JUDGMENTS_CONTENTS)
    d.clear_judgments()


def tag_judgments_contents():
    response = requests.post(d.DOCKER_URL, data=d.JUDGMENTS_CONTENTS_STRING)
    # dat = d.ALL_JUDGMENTS.pop()
    # response = requests.post(d.DOCKER_URL, data=dat['textContent'])
    return response.json


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
    with open(file, 'w', encoding='utf-8') as fp:
        json.dump(data, fp)


def read_from_file(file):
    with open(file, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    return data


for i in range(601, 651):
    fileName = '../resources/json/judgments-' + str(i) + '.json'
    read_file(fileName)
    filter_judgements()
    join_judgments_contents()
    tagged_data = tag_judgments_contents()
    with open('temp/tagged/tagged_data_' + str(i), 'w') as kle:
        kle.write(tagged_data)


# fileName = '../resources/example_judgment.json'
# read_file(fileName)
# filter_judgements()
# join_judgments_contents()
# write_to_file('temp/judgments_content_1', d.JUDGMENTS_CONTENTS_STRING)

# d.JUDGMENTS_CONTENTS_STRING = read_from_file('temp/judgments_content_2')
# tagged_data = tag_judgments_contents()
# print(tagged_data)
# with open('temp/tagged/tagged_data_2', 'w') as kle:
# 	kle.write(tagged_data)


# for i in range(600, 651):
#     d.JUDGMENTS_CONTENTS_STRING = read_from_file('temp/judgments_content_' + str(i))
#     tagged_data = tag_judgments_contents()
#     write_to_file('temp/tagged/tagged_data_' + str(i), tagged_data)
