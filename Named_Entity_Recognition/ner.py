import json
import re
import data as d
import time
import requests
import xml.dom.minidom as minidom
import operator
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
from expression import Expression
import pickle


def read_file(fileName):
    with open(fileName, 'r', encoding="utf8") as file:
        d.ALL_JUDGMENTS = json.load(file)["items"]


def filter_judgements():
    for judgment in d.ALL_JUDGMENTS:
        if d.YEAR in judgment["judgmentDate"]:
            d.JUDGMENTS.append(judgment)
        if len(d.JUDGMENTS) == 2:
            break
    d.clear_all_judgments()


def filter_html_tags():
    length = len(d.JUDGMENTS)
    temp_judgments_list = list()
    for index in range(length):
        judgment = d.JUDGMENTS.pop()
        temp = re.sub(d.HTML_REGEX, '', judgment['textContent'])
        temp = re.sub(d.NEW_LINE_SIGN, '', temp)
        temp_judgments_list.append(temp)
    d.JUDGMENTS = temp_judgments_list


def write_to_file(file, data):
    with open(file, 'wb') as fp:
        pickle.dump(data, fp)


def read_from_file(file):
    with open(file, 'rb') as fp:
        data = pickle.load(fp)
    return data


def recognize_judgments():
    text = ''
    for judgment in d.JUDGMENTS:
        text = text + ' ' + judgment

    data = {'lpmn': d.LPMN, 'user': d.USER, 'text': text}
    data = process(data)
    if data == None:
        return
    data = data[0]["fileID"]
    content = requests.get(d.URL + '/download' + data).text
    parsed = minidom.parseString(content)
    sentences = parsed.getElementsByTagName('sentence')
    for sentence in sentences:
        expressions = get_from_sentence(sentence)
        d.EXPRESSIONS.extend(expressions)
    parsed.unlink()
    write_to_file('temp/EXPRESSIONS', d.EXPRESSIONS)


def get_from_sentence(sentence):
    expressions = list()
    toks = sentence.getElementsByTagName('tok')
    toks_length = len(toks)
    for i in range(toks_length):
        tok = toks.pop()
        orth_word = tok.getElementsByTagName('orth')[0].childNodes[0].nodeValue
        anns = tok.getElementsByTagName('ann')
        anns_length = len(anns)
        for j in range(anns_length):
            ann = anns.pop()
            chan = ann.attributes['chan'].value
            index = int(ann.childNodes[0].nodeValue)
            if not index == 0:
                added = False
                for exp in expressions:
                    if exp.class_index == index and exp.class_name == chan:
                        exp.tokens.append(orth_word)
                        added = True
                        break
                if not added:
                    expressions.append(Expression(orth_word, chan, index))
    # parsed.getElementsByTagName('tok')[23].getElementsByTagName('orth')[0].childNodes[0].data
    # parsed.getElementsByTagName('tok')[23].getElementsByTagName('ann')[0].attributes['chan'].value
    # parsed.getElementsByTagName('tok')[23].getElementsByTagName('ann')[0].childNodes[0].data
    return expressions


def process(data):
    doc = json.dumps(data)
    taskid = requests.post(d.URL + '/startTask/', doc, {'Content-Type': 'application/json'}).text
    time.sleep(0.2)
    resp = requests.get(d.URL + '/getStatus/' + taskid).text
    data = json.loads(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(5)
        resp = requests.get(d.URL + '/getStatus/' + taskid).text
        data = json.loads(resp)
    if data["status"] == "ERROR":
        print("Error " + data["value"])
        return None
    return data["value"]


def display_diagrams():
    fain_class = list()
    rougher_class = list()
    for expr in d.EXPRESSIONS:
        fain_class.append(expr.class_name)
        rougher_class.append(expr.general_class_name)
    fain_class = Counter(fain_class)
    rougher_class = Counter(rougher_class)
    print(fain_class)
    fain_class = OrderedDict(sorted(fain_class.items(), key=operator.itemgetter(0), reverse=False))
    rougher_class = OrderedDict(sorted(rougher_class.items(), key=operator.itemgetter(0), reverse=False))
    plt.bar(fain_class.keys(), fain_class.values())
    plt.title('Liczność rozpoznanych klas - drobnoziarnista klasyfikacja wyrażeń')
    plt.xlabel('Wyrażenie')
    plt.ylabel('Liczba wystąpień')
    plt.xticks(range(0, len(fain_class) + 1), fain_class.keys(), rotation='vertical')
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    print(d.ROUGHER_CLASSIFICATION)
    print(rougher_class)
    plt.bar(rougher_class.keys(), rougher_class.values())
    plt.title('Liczność rozpoznanych klas - zgrubna klasyfikacja wyrażeń')
    plt.xlabel('Wyrażenie')
    plt.ylabel('Liczba wystąpień')
    plt.xticks(range(0, len(rougher_class)), rougher_class.keys(), rotation='vertical')
    plt.subplots_adjust(bottom=0.20)
    plt.show()


for i in range(549, 551):
    fileName = '../resources/json/judgments-' + str(i) + '.json'
    read_file(fileName)
    filter_judgements()


filter_html_tags()
# d.EXPRESSIONS = read_from_file('temp/EXPRESSIONS')
recognize_judgments()
display_diagrams()

top_expressions = {}
for expression in d.EXPRESSIONS:
    key = (expression.class_name, expression.get_tokens())
    if key in top_expressions:
        top_expressions[key] += 1
    else:
        top_expressions[key] = 1
print(top_expressions)
top = sorted(top_expressions.items(), key=operator.itemgetter(1), reverse=True)
for i in range(100):
    if i < len(top):
        print(top[i])

general_top = {}
for expression in d.EXPRESSIONS:
    key = expression.general_class_name
    if key in general_top:
        general_top[key].append(expression.get_tokens())
    else:
        general_top[key] = [expression.get_tokens()]
for key in general_top.keys():
    freq = Counter(general_top[key])
    sorted_general = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    print(key)
    for i in range(10):
        if i < len(sorted_general):
            print(sorted_general[i])
