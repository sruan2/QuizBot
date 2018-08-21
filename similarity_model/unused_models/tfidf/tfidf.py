import pickle as pkl 
import re 
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import unicodedata
from sklearn.metrics.pairwise import linear_kernel
from random import randint
from gensim.models import Doc2Vec
import os

class tfidfTransform():
    # initialize the object with the offline-trained model file as an input
    def __init__(self, qa_kb, qa_md):
        print("\n" + str(os.getpid())+" tfidf initialization begins\n")
        self.QID = 0
        self.QA_KB = qa_kb
        self.QA_MD = qa_md
        print("\ntfidf initialization ends\n")
    
    # FIXME --- INCLUDE SUBJECT
    def pickRandomQuestion(self):
        print("=======================================================================================")
        QID = randint(0, self.QA_KB.KBlength)
        picked_question = self.QA_KB.QKB[QID].rstrip()
        return picked_question, QID

    def pickLastQuestion(self, QID):
        picked_question = self.QA_KB.QKB[QID].rstrip()
        return picked_question

    def pickNextSimilarQuestion(self, QID):
        # FIXME
        # while True:
        # among the 1000 most similar questions, pick one
        num = randint(0, 1000)
        NextQID = self.QA_MD.MODEL.docvecs.most_similar(QID, topn = 1000)[num][0] # among top 1000 questions, pick one and then return question id
            # if NextQID not in self.ASKED:
        picked_question = self.QA_KB.QKB[NextQID].rstrip() # find the question based on the question id
                # self.ASKED.append(NextQID)
            # break                 
        return picked_question, NextQID
    
    def getAnswer(self, QID):
        return self.QA_KB.AKB[QID].rstrip()

    def computeScore(self, user_answer, QID):
        user_answer = user_answer.lower()
        picked_answer = self.AKB[QID].rstrip()
        answer = [picked_answer]
        answer.append(user_answer)
        self.tfidf_features = TfidfVectorizer().fit_transform(answer)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        print("Similarity between the standard answer and yours is: " + str(int(cosine_similarities[1]*10)))
        return picked_answer, int(cosine_similarities[1]*10)
