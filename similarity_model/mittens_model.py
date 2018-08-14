''' this is a mittens model to construct new vectors

2018 July 19
'''

import pickle
import _pickle as cPickle
import numpy as np
from mittens import Mittens


# the file that contains the vocab vectors from glove trained model
glove_file = 'data_files/glove.6B.100d.pkl'

# files containing the cooccurrence matrix and matching vocabulary
cooccurrence_file = 'data_files/weighted_matrix.pkl'
vocab_file = 'data_files/vocab.pkl'


if __name__ == '__main__':
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
    print('Initial cooccurrence shape:', cooccurrence.shape)

    glove_vocab = glove.keys()
    # indices for vocab thats not in glove
    missing_words = np.array(
        [i for i in range(len(vocab)) if vocab[i] not in glove_vocab])

    print('missing_words shape:', missing_words.shape)

    cooccurrence = cooccurrence[missing_words][:, missing_words]
    vocab = list(np.array(vocab)[missing_words])

    # check if sizes match up
    print('Vocab length:', len(vocab))
    print('New cooccurrence shape:', cooccurrence.shape)

    print('size of glove vocab {}'.format(len(glove)))

    mittens_model = Mittens(n=100, max_iter=1000)
    # Note: n must match the original embedding dimension
    new_embeddings = mittens_model.fit(cooccurrence,
                                       vocab=vocab,
                                       initial_embedding_dict=glove)

    print('\nsize of new embeddings vocab {}'.format(len(new_embeddings)))

    # transform the vectors into a dictionary mapping and then append the vocabulary to glove
    embeddings_dict = {key: np.array(vector)
                       for key, vector in zip(vocab, new_embeddings)}
    glove.update(embeddings_dict)

    print('size of updated glove vocab {}'.format(len(glove)))

    # save to mitten_model
    with open('data_files/mittens_model.pkl', 'wb') as output:
        cPickle.dump(glove, output)
