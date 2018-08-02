'''A script to help build the cooccurrence matrix and vocabulary and save them to files

July 2018
'''

import itertools
import re
from glove import Corpus, Glove


def read_corpus(filename):
    '''Reads a corpus of text and parses it, lowercasing all characters and removign non standard characters'''
    delchars = [chr(c) for c in range(256)]
    delchars = [x for x in delchars if not x.isalnum()]
    delchars.remove(' ')
    delchars = ''.join(delchars)

    with open(filename, 'r', encoding='utf8') as datafile:
        for line in datafile:
            yield re.sub(r'\W+', ' ', line.lower()).split(' ')


# input the space delineated corpus that you want to read
sentences = read_corpus('data_files/science_corpus')

corpus = Corpus()
corpus.fit(sentences, window=10)
cooccurrence_matrix = corpus.matrix
vocab = list(sorted(corpus.dictionary, key=corpus.dictionary.get))

# check that the sizes match
print(corpus.matrix.shape)
print(len(vocab))

# save the vocabulary for visualization
with open('data_files/vocab.txt', 'w', encoding='utf8') as f:
    for word in vocab:
        f.write(word + '\n')

import _pickle as cPickle

# save the cooccurrence matrix  and vocabulary file
with open('data_files/weighted_matrix.pkl', 'wb') as output:
    cPickle.dump(cooccurrence_matrix, output)

with open('data_files/vocab.pkl', 'wb') as f:
    cPickle.dump(vocab, f)
