from __future__ import division
# code adpated from https://github.com/PrincetonML/SIF: examples/sif_embedding

import sys
sys.path.append('../src')
sys.path.append('/home/venv/quizbot/QuizBot/sentence_similarity/sif_implementation')
import data_io, params, SIF_embedding
import numpy as np


# input
#wordfile = '../data/glove.840B.300d.txt' # word vector file, can be downloaded from GloVe website
wordfile = 'sentence_similarity/glove/glove.6B.100d.txt' # sherry: use glove.6B instead # updated path for AWS
weightfile = 'sentence_similarity/princeton_sif/auxiliary_data/enwiki_vocab_min200.txt' # each line is a word and its frequency
weightpara = 1e-3 # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
rmpc = 1 # number of principal components to remove in SIF weighting scheme

# ======= loading necessary word vectors and weights. They should only be loaded once. ========

# load word vectors
(words, We) = data_io.getWordmap(wordfile)
# load word weights
word2weight = data_io.getWordWeight(weightfile, weightpara) # word2weight['str'] is the weight for the word 'str'
weight4ind = data_io.getWeight(words, word2weight) # weight4ind[i] is the weight for the i-th word


def sentences2embeddings(sentences):
	"""
	Input: sentences - a list of sentences
	Output: sentence_embeddings - a list of sentence embeddings (numpy vectors of shape (1,300))

	"""
	# load sentences
	x, m = data_io.sentences2idx(sentences, words) # x is the array of word indices, m is the binary mask indicating whether there is a word in that location
	w = data_io.seq2weight(x, m, weight4ind) # get word weights

	# set parameters
	parameters = params.params()
	parameters.rmpc = rmpc
	# get SIF embedding
	embedding = SIF_embedding.SIF_embedding(We, x, w, parameters) # embedding[i,:] is the embedding for sentence i

	sentence_embeddings = []
	for i in range(len(sentences)):
		e = np.array(embedding[i,:]).reshape((1,100)) # reshape to fit into the function semantic_similarity
		sentence_embeddings.append(e)

	return sentence_embeddings

# Compute Coisine Similarity of first two sentences
def semantic_similarity(vec_1, vec_2):
    return int(((np.dot(vec_1, vec_2.T) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2)))[0,0]+1)*5) # shape is (0,0)

# answer similarity API for Quizbot
def answer_similarity(s1, s2):
	""" Input: s1 - string, sentence 1
			   s2 - string, sentence 2
		Return: similarity - float, coisine similarity score [-1,1] between s1 and s2
	"""
	embs = sentences2embeddings([s1,s2])
	return semantic_similarity(embs[0], embs[1])


if __name__ == '__main__': # for testing

	sentences = ['this is an example sentence', 
			 'this is another sentence that is slightly longer',
			 'this is the same sentence',
			 'this is not the same sentence',
			 'this is me',
			 'this is a different sentece',
			 'a flying bird',
			 'a bird flies',
			 'The bird is in the sky']

	sentence_embeddings = sentences2embeddings(sentences)

	for i,s in enumerate(sentences):
		for j,t in enumerate(sentences[i:]):
			print(s)
			print(t)
			print("similarity: " + str(semantic_similarity(sentence_embeddings[i], sentence_embeddings[i+j]))+ "\n")



