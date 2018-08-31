'''A script to help build the cooccurrence matrix and vocabulary and save them to files

July 2018
'''

import itertools
import re
from glove import Corpus, Glove
import _pickle as cPickle


def read_corpus(filename):
    '''Reads a corpus of text and parses it, lowercasing all characters and removing non standard characters'''
    with open(filename, 'r', encoding='utf8') as datafile:
        for line in datafile:
            yield re.sub(r'\W+', ' ', line.lower()).split(' ')


if __name__ == '__main__':
    # input the space delineated corpus that you want to read
    sentences = read_corpus('data_files/science_corpus')

    corpus = Corpus()
    corpus.fit(sentences, window=10)
    cooccurrence_matrix = corpus.matrix
    vocab = list(sorted(corpus.dictionary, key=corpus.dictionary.get))

    # check that the sizes match
    print('Corpus matrix shape:', corpus.matrix.shape)
    print('Vocab length:', len(vocab))

    # save the vocabulary for visualization
    with open('data_files/vocab.txt', 'w', encoding='utf8') as f:
        for word in vocab:
            f.write(word + '\n')

    # save the cooccurrence matrix  and vocabulary file
    with open('data_files/weighted_matrix.pkl', 'wb') as output:
        cPickle.dump(cooccurrence_matrix, output)

    with open('data_files/vocab.pkl', 'wb') as f:
        cPickle.dump(vocab, f)
