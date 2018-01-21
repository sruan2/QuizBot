import sys
sys.path.append("/home/venv/quizbot/QuizBot/sentence_similarity/sif_implementation")
import numpy as np
from wordembeddings import EmbeddingVectorizer
from nltk import RegexpTokenizer
import pickle
from utils import *

if __name__ == '__main__': # for testing
    sentences = ['this is an example sentence', 
                'this is another sentence that is slightly longer',
                'this is the same sentence',
                'this is not the same sentence',
                'this is me',
                'this is a different sentence',
                'a flying bird',
                'a bird flisflies',
                'chromoplasts',
                #'magnetic field',
                #'boiling point'
                ]

    tokenizer = RegexpTokenizer(r'[\w]+')

    tokenized_sentences = preprocess(sentences, tokenizer)

    for i in tokenized_sentences:
        print(i)

    pkl = open('/Users/sherryruan/data/glove/glove.6B/glove.6B.100d.pkl', 'rb')

    glove = pickle.load(pkl)

    print("="*80+"\nloaded glove")

    emb = EmbeddingVectorizer(word_vectors=glove, weighted=True, R=True)

    V = emb.fit_transform(tokenized_sentences) # for QuizBot replace tokenized_sentences with the entire KB answers

    for i,_ in enumerate(V):
        for j,_ in enumerate(V[i:]):
            print(sentences[i])
            print(sentences[i+j])
            print("similarity: " + str(cosine_similarity(V[i], V[i+j]))+ "\n")

    # for new query, cal emb.transform instead of emb.fit_transform
    query = ["a flying raven"]
    tokenized_query = preprocess(query, tokenizer)
    V_query = emb.transform(tokenized_query)

    print("similarity: " + str(cosine_similarity(V_query[0], V[0]))+ "\n")


