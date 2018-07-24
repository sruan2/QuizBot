import sys
sys.path.append("..")
import numpy as np
from nltk import RegexpTokenizer
from keras.models import Sequential, Model
from keras.layers import Dense, Input, concatenate
from keras.optimizers import Adam
import pickle

from messages import MESSAGES, EXAMPLE_MESSAGES
from sif_implementation.wordembeddings import EmbeddingVectorizer
from QAKnowledgebase import QAKnowlegeBase
from sif_implementation.utils import *

'''This is the test function for semi supervised model 
   code taken from https://github.com/jorisvandenbossche/wordembeddings
2018 July 6
'''

# model to fit semi supervised model data
def init_model():
	lin_dot = Input(shape=(100,), name='lin_dot')
	lin_abs = Input(shape=(100,), name='lin_abs')

	l_sum = concatenate([lin_dot, lin_abs])
	l_sigmoid = Dense(50, activation='sigmoid')(l_sum)
	l_softmax = Dense(5, activation='softmax')(l_sigmoid)

	model = Model(inputs=[lin_dot, lin_abs], outputs=l_softmax)
	return model

# map the scores to a sprase matrix
def to_float_dummies(scores, integer_scores):
	diffs = scores[:, np.newaxis] - integer_scores[np.newaxis, :]

	diffs[np.abs(diffs) > 1] = 0
	mask1 = (diffs < 0).copy()
	mask2 = (diffs > 0).copy()
	diffs[mask1] = 1 - np.abs(diffs[mask1]) 
	diffs[mask2] = 1 - diffs[mask2]

	diffs[scores[:, np.newaxis] == integer_scores[np.newaxis, :]] = 1
	
	return diffs

# fit the unsupervised embedding model to the quizbot answer database
def fit_model(glove_file, json_file):
	# open the file from pretrained vector model. This one is of size 100
	with open(glove_file, 'rb') as pkl:
		glove = pickle.load(pkl)
		print("="*80+"\nloaded vectors")

	emb = EmbeddingVectorizer(word_vectors=glove, weighted=True, R=True)

	qa_kb = QAKnowlegeBase(json_file)

	sentences = qa_kb.AKB
	sentences = list(map(str, sentences))

	tokenizer = RegexpTokenizer(r'[\w]+')

	tokenized_sentences = preprocess(sentences, tokenizer)
	V = emb.fit_transform(tokenized_sentences)
	return emb

# transform data to put into the NN model from word pairs to dot product and abstolute value
def transform_data(emb, pair_one, pair_two):
	pair_one = np.array(pair_one)
	pair_two = np.array(pair_two)
	vectors_one = emb.transform(pair_one)
	vectors_two = emb.transform(pair_two)

	g1_dot_g2 = vectors_one * vectors_two	
	g1_abs_g2 = np.abs(vectors_one - vectors_two)
	return g1_dot_g2, g1_abs_g2

# get scores from words
def evaluate_model(model, emb, pair_one, pair_two):
	g1_dot_g2, g1_abs_g2 = transform_data(emb, pair_one, pair_two)
	predicted = model.predict([g1_dot_g2, g1_abs_g2])
	pred_score = np.dot(predicted, np.array([1,2,3,4,5]))
	return pred_score

# repeat data such that the 
def repeat_data(pair_one, pair_two, pair_scores):
	one_labeled_data = [i for i in range(len(pair_scores)) if pair_scores[i] == 1]
	five_labeled_data = [i for i in range(len(pair_scores)) if pair_scores[i] == 5]
	print('number of one labeled: ', len(one_labeled_data))
	print('number of five labeled: ', len(five_labeled_data))

	# repeat the five_labeled data to match size of one labeled
	five_labeled_data = np.hstack((np.array(five_labeled_data),
		np.random.choice(five_labeled_data, len(one_labeled_data) - len(five_labeled_data))))
	print('five labeled data length: ', len(five_labeled_data))
	print('one labeled data length: ', len(one_labeled_data))
	indices = np.hstack((one_labeled_data, five_labeled_data))
	np.random.shuffle(indices)
	print('total data length: ', len(indices))

	pair_one = [pair_one[i] for i in indices]
	pair_two = [pair_two[i] for i in indices]
	pair_scores = np.array([pair_scores[i] for i in indices])

	return pair_one, pair_two, pair_scores

def fit_supervised_model(model, emb, csv_file):
	relatedness_pairs = np.genfromtxt(csv_file, dtype = str, delimiter = ',')
	pair_one = relatedness_pairs[:,0]
	pair_two = relatedness_pairs[:,1]
	pair_scores = relatedness_pairs[:,2].astype(float)

	pair_one, pair_two, pair_scores = repeat_data(pair_one, pair_two, pair_scores)	
	g1_dot_g2, g1_abs_g2 = transform_data(emb, pair_one, pair_two)
	y = to_float_dummies(pair_scores, np.array([1,2,3,4,5]))

	model.compile(optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08),
			  loss='kullback_leibler_divergence',
			  metrics=['accuracy'])	

	# sample_weight = np.array([1 if pair_scores[i] == 1 else 10 for i in range(len(pair_scores))])
	model.fit([g1_dot_g2, g1_abs_g2], y, epochs=300, verbose=2, validation_split = 0)

	return model

def build_heatmap(messages, heatmap_file):
	# construct the message pairs to pass to the model
	test_pair_one = []
	test_pair_two = []
	for message1 in messages:
		for message2 in messages:
			test_pair_one.append(message1)
			test_pair_two.append(message2)	

	# convert the scores so that they are on 0-1 scale
	test_scores = evaluate_model(model, emb, np.array(test_pair_one), np.array(test_pair_two))
	corr = ((test_scores - 1) / 4).reshape(len(messages), len(messages))
	labels = messages
	plot_similarity(messages, corr, 90, heatmap_file)

if __name__ == '__main__': # for testing
	csv_file = 'relatedness_scores.csv'

	# file in the form of a dictionary {vocab word : numpy array} edit the Input size
	glove_file = 'mittens_model.pkl'
	json_file = '../QAdataset/questions_filtered_150_quizbot.json'

	emb = fit_model(glove_file, json_file)

	model = init_model()
	model = fit_supervised_model(model, emb, csv_file)

	model.save_weights('model_weights.h5')
	# TODO: Save the model
	with open('model_architecture.json', 'w') as f:
		f.write(model.to_json())

	build_heatmap(MESSAGES, 'heatmaps/semi_supervised_heatmap.png')
	build_heatmap(EXAMPLE_MESSAGES, 'heatmaps/semi_supervised_example_heatmap.png')

	# test various other pairs of words
	test_pair_one = ['you are right', 'you are right', 'true', 'yes', 'right', 'a mathemematician found a solution to the problem']
	test_pair_two = ['you are correct', 'you are wrong', 'yes', 'yes', 'correct', 'A problem was solved by a young mathematician']

	test_scores = evaluate_model(model, emb, test_pair_one, test_pair_two)
	# transform test scores so that its on a 0-1 scale
	test_scores = (test_scores - 1) / 4

	for i,j,k in zip(test_pair_one, test_pair_two, test_scores):
		print('{}, {}, score: {}'.format(i,j,k))
