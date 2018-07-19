import sys
sys.path.append("..")
import numpy as np
from sif_implementation.wordembeddings import EmbeddingVectorizer
from nltk import RegexpTokenizer
from QAKnowledgebase import QAKnowlegeBase

import pickle
from sif_implementation.utils import *

'''This is the test function for different question sequencing algorithms

2018 July 6
'''

if __name__ == '__main__': # for testing
    # Read QA json data and construct the QA knowledge base

    json_file = '../QAdataset/questions_filtered_150_quizbot.json'
    qa_kb = QAKnowlegeBase(json_file)

    sentences = qa_kb.AKB
    sentences = list(map(str, sentences))

    tokenizer = RegexpTokenizer(r'[\w]+')

    tokenized_sentences = preprocess(sentences, tokenizer)

    # file = 'C:/Users/Justin Xu/Desktop/glove.6B.300d.pkl'
    # file = 'C:/Users/Justin Xu/Desktop/SciQ dataset-2 3/mittens_model.pkl'
    file = 'C:/Users/Justin Xu/Desktop/SciQ dataset-2 3/vectors.pkl'
    # file = 'C:/Users/Justin Xu/Desktop/paragram_vectors.pkl'
    # oldFile = '/Users/sherryruan/data/glove/glove.6B/glove.6B.100d.pkl'
    pkl = open(file, 'rb')

    glove = pickle.load(pkl)
    print("="*80+"\nloaded vectors")

    emb = EmbeddingVectorizer(word_vectors=glove, weighted=True, R=True)


    # V = emb.fit_transform(tokenized_sentences) # for QuizBot replace tokenized_sentences with the entire KB answers
    V = emb.fit_transform(tokenized_sentences) # for QuizBot replace tokenized_sentences with the entire KB answers

    # for new query, cal emb.transform instead of emb.fit_transform
    queryAnswers = [('hypothesis','hypotheses'),
            ('carbon and hydrogen','carbon'),
            ('bond','covalent bonds'),
             ('human activity', 'careless human activity'),
             ('heat', 'thermal energy'),
             ('the nucleus', 'atomic nucleus'),
             ('medulla', 'nuclear'),
             ('altitude', 'height'),
             ('oxygen', 'O2')]
             
    for q,a in queryAnswers:
        tokenized_query = preprocess(q, tokenizer)
        tokenized_answer = preprocess(a, tokenizer)
        answer_query = emb.transform(tokenized_answer)
        V_query = emb.transform(tokenized_query)

        print(q, ',', a)
        print("similarity: " + str(cosine_similarity(V_query[0], answer_query[0]))+ "\n")


