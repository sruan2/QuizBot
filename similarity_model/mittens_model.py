import pickle
import numpy as np

from mittens import Mittens

''' this is a mittens model to construct new vectors

2018 July 19
'''

glove_file = 'glove.6B.100d.pkl'
# glove_file = 'vectors.pkl'
# glove_file = 'paragram_vectors.pkl'

# files containing the cooccurrence matrix and matching vocabulary
cooccurrence_file = 'weighted_matrix.pkl'
vocab_file = 'vocab.pkl'

with open(glove_file, 'rb') as pkl:
	glove = pickle.load(pkl)
	print('loaded glove')

with open(cooccurrence_file, 'rb') as pkl:
	cooccurrence = pickle.load(pkl)
	print('loaded cooccurrence')

with open(vocab_file, 'rb') as pkl:
	vocab = pickle.load(pkl)
	print('loaded vocab')

# convert to numpy array
cooccurrence = cooccurrence.toarray()

# check if sizes match up
print(len(vocab))
print(cooccurrence.shape)

mittens_model = Mittens(n=100, max_iter=1000)
# Note: n must match the original embedding dimension
new_embeddings = mittens_model.fit(
    cooccurrence,
    vocab=vocab,
    initial_embedding_dict=glove)

# transform the vectors into a dictionary mapping and then append the vocabulary to glove
embeddings_dict = {key:np.array(vector) for key,vector in zip(cooccurrence.index, new_embeddings)}
glove.update(embeddings_dict)

import _pickle as cPickle

save_file = 'mittens_model.pkl'

# save to mitten_model
with open(save_file, 'wb') as output:
    cPickle.dump(glove, output)
