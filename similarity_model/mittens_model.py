''' this is a mittens model to construct new vectors

2018 July 19
'''

import pickle
import numpy as np
from mittens import Mittens

# the file that contains the vocab vectors from glove trained model
glove_file = 'data_files/glove.6B.100d.pkl'

# files containing the cooccurrence matrix and matching vocabulary
cooccurrence_file = 'data_files/weighted_matrix.pkl'
vocab_file = 'data_files/vocab.pkl'

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

glove_vocab = glove.keys()
# indices for vocab thats not in glove
missing_words = np.array(
    [i for i in range(len(vocab)) if vocab[i] not in glove_vocab])

cooccurrence = cooccurrence[missing_words][:, missing_words]
vocab = list(np.array(vocab)[missing_words])

# check if sizes match up
print(len(vocab))
print(cooccurrence.shape)

print('size of glove vocab {}'.format(len(glove)))

mittens_model = Mittens(n=100, max_iter=1000)
# Note: n must match the original embedding dimension
new_embeddings = mittens_model.fit(
    cooccurrence,
    vocab=vocab,
    initial_embedding_dict=glove)

print()
print('size of new embeddings vocab {}'.format(len(new_embeddings)))

# transform the vectors into a dictionary mapping and then append the vocabulary to glove
embeddings_dict = {key: np.array(vector)
                   for key, vector in zip(vocab, new_embeddings)}
glove.update(embeddings_dict)

print('size of updated glove vocab {}'.format(len(glove)))

import _pickle as cPickle

save_file = 'data_files/mittens_model.pkl'

# save to mitten_model
with open(save_file, 'wb') as output:
    cPickle.dump(glove, output)
