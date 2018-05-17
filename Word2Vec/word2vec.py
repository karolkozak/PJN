import json
import re
import data as d
from gensim.models import Word2Vec
from gensim.models.phrases import Phraser, Phrases
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def read_file(fileName):
    with open(fileName, 'r', encoding="utf8") as file:
        d.JUDGMENTS.append(json.load(file)["items"])


def filter_html_tags():
    length = len(d.JUDGMENTS)
    temp_judgments_list = list()
    for index in range(length):
        judgment = d.JUDGMENTS.pop()
        temp = re.sub(d.HTML_REGEX, '', judgment['textContent'])
        temp = re.sub(d.NEW_LINE_SIGN, '', temp)
        temp_judgments_list.append(temp)
        d.JUDGMENTS_TEXT = ''.join(temp_judgments_list)
    d.JUDGMENTS = temp_judgments_list


def convert_text_to_list_of_sentences():
    text = ''
    for judgment in d.JUDGMENTS:
        text = text + ' ' + judgment
    sentences = text.split('.')
    for sentence in sentences:
        d.SENTENCES.append(sentence.strip().split(' '))


def detect_phrases():
    phrases = Phrases(d.SENTENCES)
    bigram = Phraser(phrases)
    trigram_list = list()
    trigram = Phrases(bigram[d.SENTENCES])
    for sentence in d.SENTENCES:
        trigram_list.append(trigram[bigram[sentence]])
    d.TRIGRAM_LIST_SENTENCES = trigram_list
    del trigram_list[:]


def train():
    d.MODEL = Word2Vec(d.TRIGRAM_LIST_SENTENCES, sg=0, window=5, size=300, min_count=3)
    d.MODEL.save('./temp/word2vec_model')


def load_model():
    d.MODEL = Word2Vec.load('./temp/word2vec_model')


for i in range(100, 560):
    fileName = '../resources/json/judgments-' + str(i) + '.json'
    read_file(fileName)

filter_html_tags()
convert_text_to_list_of_sentences()
detect_phrases()
train()

load_model()
for phrase in d.PHRASES:
    print(phrase)
    print(d.MODEL.most_similar(phrase, topn=3))

print(d.MODEL.most_similar(positive=['Sąd_Najwyższy', 'konstytucja'], negative=['kpc'], topn=5))
print(d.MODEL.most_similar(positive=['pasażer', 'kobieta'], negative=['mężczyzna'], topn=5))
print(d.MODEL.most_similar(positive=['samochód', 'rzeka'], negative=['droga'], topn=5))

vectors = [d.MODEL.wv[x] for x in d.WORDS_T_SNE]
transformed = TSNE().fit_transform(vectors)
x, y = zip(*transformed)
plt.scatter(x, y)
for i, txt in enumerate(d.WORDS_T_SNE):
    plt.annotate(txt, (x[i], y[i]))
plt.show()
