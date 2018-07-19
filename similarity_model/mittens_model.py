import pickle
from mittens import Mittens

# store the original model to append to and fit to 
glove_file = 'C:/Users/Justin Xu/Desktop/glove.6B.100d.pkl'
# file = 'C:/Users/Justin Xu/Desktop/SciQ dataset-2 3/vectors.pkl'
# file = 'C:/Users/Justin Xu/Desktop/paragram_vectors.pkl'

# files containing the cooccurrence matrix and matching vocabulary
cooccurrence_file = 'C:/Users/Justin Xu/Desktop/SciQ dataset-2 3/weighted_matrix.pkl'
vocab_file = 'C:/Users/Justin Xu/Desktop/SciQ dataset-2 3/vocab.pkl'

with open(glove_file, 'rb') as pkl:
	glove = pickle.load(pkl)
	print('loaded glove')

with open(cooccurrence_file, 'rb') as pkl:
	cooccurrence = pickle.load(pkl)
	print('loaded cooccurrence')

with open(vocab_file, 'rb') as pkl:
	vocab = pickle.load(pkl)
	print('loaded vocab')

mittens_model = Mittens(n=300, max_iter=1000)
# Note: n must match the original embedding dimension
new_embeddings = mittens_model.fit(
    cooccurrence,
    vocab=vocab,
    initial_embedding_dict= glove)

# transform the vectors into a dictionary mapping and then append the vocabulary to glove
embeddings_dict = {key:np.array(vector) for key,vector in zip(cooccurrence.index, new_embeddings)}
glove.update(embeddings_dict)

import _pickle as cPickle

save_file = 'C:/Users/Justin Xu/Desktop/SciQ dataset-2 3/mittens_model.pkl'

# save to mitten_model
with open(save_file, 'wb') as output:
    cPickle.dump(glove, output)
