import itertools
import re

from glove import Corpus, Glove

def read_corpus(filename):

    delchars = [chr(c) for c in range(256)]
    delchars = [x for x in delchars if not x.isalnum()]
    delchars.remove(' ')
    delchars = ''.join(delchars)

    with open(filename, 'r', encoding = 'utf8') as datafile:
        for line in datafile:
            yield re.sub(r'\W+', ' ', line.lower()).split(' ')

# input the space delineated corpus that you want to read
sentences = read_corpus('science_corpus')

corpus = Corpus()
corpus.fit(sentences, window=10)

cooccurrence_matrix = corpus.matrix
vocab = list(sorted(corpus.dictionary, key = corpus.dictionary.get))
# check that the sizes match
print(corpus.matrix.shape)
print(len(vocab))

with open('vocab.txt', 'w', encoding = 'utf8') as f:
	for word in vocab:
		f.write(word + '\n')

# save the cooccurrence matrix 
import _pickle as cPickle

with open('weighted_matrix.pkl', 'wb') as output:
    cPickle.dump(cooccurrence_matrix, output)

with open('vocab.pkl', 'wb') as f:
	cPickle.dump(vocab, f)
