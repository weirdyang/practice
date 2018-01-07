import random

import nltk
from nltk import word_tokenize
from nltk.collocations import TrigramAssocMeasures
from nltk.util import ngrams

def generate_model(list_ngrams, word, num=90):
    """http://www.cyber-omelette.com/2017/01/markov.html
    generate model based on ngrams
    """
    list_random = list_ngrams
    message = word.capitalize() + ' '
    print(message)
    while len(message.split(' ')) < num:
        random.shuffle(list_ngrams)
        for item in list_ngrams:
            if item[0] == word.lower():
                message += "{0} {1} ".format(item[1], item[2])
                word = CFD[item[2]].max().lower()
                list_random.remove(item)
    return message

def generate_model_2(cfdist, word, num=15):
    """http://www.cyber-omelette.com/2017/01/markov.html
    generate model based on markov chain for single words
    """
    message = word.capitalize()
    while len(message.split(' ')) < num:
        print(word, end=' ')
        word = cfdist[word].max()


trigram_measures = TrigramAssocMeasures()
with open('letsrun_1.txt', mode='r', encoding='utf-8') as f:
    raw = f.read()

words = word_tokenize(raw.lower())
print(words)
generated_ngrams = list(ngrams(words, 3))
bigrams = nltk.bigrams(words)
CFD = nltk.ConditionalFreqDist(bigrams)
FD = nltk.FreqDist(generated_ngrams)
print(FD)
print(generate_model(generated_ngrams, 'run'))
