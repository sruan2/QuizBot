'''This is the test function for SIF similarity model 

2018 July 6
'''

import sys
sys.path.append("..")
import numpy as np
from nltk import RegexpTokenizer
import pickle

from messages import MESSAGES
from QAKnowledgebase import QAKnowlegeBase
from sif_implementation.wordembeddings import EmbeddingVectorizer
from sif_implementation.utils import *


def build_heatmap(messages, emb, filename):
    '''subfunction that builds the heatmap

    Args:
        messages: the file which contains a list of words to compare
        emb: the word embeddings from file (glove, mittens, ...)
        filename: file to save the image to
    '''
    tokenized_messages = preprocess(MESSAGES, tokenizer)
    message_embeddings = emb.transform(tokenized_messages)

    # normalize our message embeddings so that cosine similarity is simply their dot product
    message_embeddings /= np.linalg.norm(message_embeddings,
                                         axis=1).reshape(-1, 1)
    corr = np.inner(message_embeddings, message_embeddings)

    # plot the heat map
    plot_similarity(MESSAGES, corr, 90, 'heatmaps/mittens_heatmap.png')


if __name__ == '__main__':
    # Read QA json data and construct the QA knowledge base
    json_file = '../QAdataset/questions_filtered_150_quizbot.json'
    qa_kb = QAKnowlegeBase(json_file)

    sentences = qa_kb.AKB
    sentences = list(map(str, sentences))

    tokenizer = RegexpTokenizer(r'[\w]+')

    tokenized_sentences = preprocess(sentences, tokenizer)

    # file that contains the word embedding pickle file
    file = 'data_files/mittens_model.pkl'
    # file = 'glove.6B.100d.pkl'
    # file = 'glove.6B.300d.pkl'
    # file = 'mittens_model.pkl'
    # file = 'vectors.pkl'
    # file = 'paragram_vectors.pkl'

    with open(file, 'rb') as pkl:
        glove = pickle.load(pkl)
        print("="*80+"\nloaded vectors")

    emb = EmbeddingVectorizer(word_vectors=glove, weighted=True, R=True)
    V = emb.fit_transform(tokenized_sentences)

    build_heatmap(MESSAGES, emb, 'heatmaps/mittens_heatmap.png')
