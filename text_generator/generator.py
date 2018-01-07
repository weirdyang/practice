import random

import nltk
from nltk import word_tokenize
#from nltk.collocations import TrigramAssocMeasures
from nltk.util import ngrams


def generate_model(list_ngrams, word, CFD, num=90):
    """
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
    """
    generate model based on CFD for single words
    """
    message = word.capitalize()
    while len(message.split(' ')) < num:
        print(word, end=' ')
        word = cfdist[word].max()


def read_file(filename):
    with open(filename, "r") as file:
        contents = file.read().replace('\n\n', ' ')
        contents = contents.replace("wrote:", ' ')
        contents = contents.replace('  ', ' ')
    return contents


def generate_using_nltk(input_text):
    words = word_tokenize(input_text.lower())
    generated_ngrams = list(ngrams(words, 3))
    bigrams = nltk.bigrams(words)
    CFD = nltk.ConditionalFreqDist(bigrams)
    #FD = nltk.FreqDist(generated_ngrams)
    print(generate_model(generated_ngrams, 'run', CFD))


def generate_using_markov(filename):
    raw = read_file(filename)
    raw = word_tokenize(raw.lower())
    markov = build_chain(raw)
    generated_text = generate_message(markov)
    print(generated_text)


def build_chain(input_text):
    index = 1
    words = input_text
    chain = {}
    for word in words[index:]:
        key = words[index - 1]
        if key in chain:
            chain[key].append(word)
        else:
            chain[key] = [word]
        index += 1
    return chain


def generate_message(chain, count=100):
    word1 = random.choice(list(chain.keys()))
    message = word1.capitalize()
    while len(message.split(' ')) < count:
        word2 = random.choice(chain[word1])
        word1 = word2
        message += ' ' + word2
    return message


generate_using_markov('letsrun_1.txt')
