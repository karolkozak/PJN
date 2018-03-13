import data as d
import json
import requests
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
from pprint import pprint
from dateutil.parser import parse

# @see http://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def read_file(fileName):
    with open(fileName, 'r', encoding="utf8") as file:
        d.ALL_JUDGMENTS = json.load(file)["items"]


def filter_judgements():
    for judgment in d.ALL_JUDGMENTS:
        if d.YEAR in judgment["judgmentDate"]:
            d.JUDGMENTS.append(judgment)
    d.clear_all_judgments()


def set_index():
    global es
    response = es.indices.create(index='my_index', body=d.INDEX_BODY, ignore=400)
    pprint(response)


def load_judgments():
    global es
    index = 0
    for judgment in d.JUDGMENTS:
        judges = []
        for judge in judgment['judges']:
            judges.append(judge['name'])
        judgment_doc = {
            'textContent': judgment['textContent'],
            'judgmentDate': parse(judgment['judgmentDate']),
            'caseNumber': judgment['courtCases'][0]['caseNumber'],
            'judges.name': judges
        }
        response = es.index(index='my_index', doc_type='doc', id=index, body=judgment_doc)
        index += 1


def search_injury_words():
    global es
    response = es.search(index='my_index', doc_type='doc', body=d.INJURY)
    print("Injury words count %s" % response['hits']['total'])


def search_permanent_injury():
    global es
    response = es.search(index='my_index', doc_type='doc', body=d.SENTENCE)
    print("Permanent injury count %s" % response['hits']['total'])


def search_permanent_injury_with_two_additional_words():
    global es
    response = es.search(index='my_index', doc_type='doc', body=d.SENTENCE_SLOP_2)
    print("Permanent injury with 2 slop count %s" % response['hits']['total'])


def search_three_most_active_judges():
    global es
    response = es.search(index='my_index', doc_type='doc', body=d.JUDGES_AGGS)
    print("Top 3 judges: ")
    for j in range(0, 3):
        print(response['aggregations']['group_by_judge']['buckets'][j])


def search_month_judgments():
    response = es.search(index='my_index', doc_type='doc', body=d.MONTH_AGGS)
    data = {}
    month = 0
    for m in response['aggregations']['judgments_per_month']['buckets']:
        print(m)
        data[month] = m['doc_count']
        month += 1
    draw_histogram(data)


def draw_histogram(data):
    print(data)
    print(len(data))
    plt.bar(data.keys(), data.values(), 1, color='b')
    plt.title('Histogram liczby orzeczeń w zależności od miesiąca')
    plt.xlabel('Miesiąc')
    plt.ylabel('Liczba orzeczeń')
    plt.show()


res = requests.get(d.BASE_URL)
pprint(res.content)      # check if ES is up
es.indices.delete(index='my_index', ignore=[400, 404])
for i in range(549, 1011):
    fileName = '../resources/json/judgments-' + str(i) + '.json'
    read_file(fileName)
    filter_judgements()

set_index()
print('loading')
load_judgments()
search_injury_words()
search_permanent_injury()
search_permanent_injury_with_two_additional_words()
search_three_most_active_judges()
search_month_judgments()
