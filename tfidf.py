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
    def __init__(self, qa_kb):
        # self.KB = reader.makeKB('Data/Aristo-Mini-Corpus-Dec2016/Aristo-Mini-Corpus-In-Parts/CurrentWebCorpus-allSources-v1.txt')
        print("\n" + str(os.getpid())+" tfidf initialization begins\n")
        # self.QKB = [] # question
        # self.SKB = [] # support
        # self.AKB = [] # answer
        # self.KBlength = 0
        # self.ASKED = [] # trying to use this array to mark down the quesitons which have been asked to the user, could be removed after db setting
        # self.MODEL = Doc2Vec.load(PreTrainedModel) # load the model in the very beginning
        self.QID = 0
        self.QA_KB = qa_kb
        print("\ntfidf initialization ends\n")
    
    # FIXME --- INCLUDE SUBJECT
    def pickRandomQuestion(self):
        print("=======================================================================================")
        QID = randint(0, self.QA_KB.KBlength)
        picked_question = self.QA_KB.QKB[QID].rstrip()

        # print(picked_question)
        # user_answer = raw_input("Enter Your Answer:")
        # answer.append(user_answer)
        # print("Standard Answer is: "+picked_answer)

        return picked_question, QID

    def pickLastQuestion(self, QID):
        picked_question = self.QA_KB.QKB[QID].rstrip()
        return picked_question

    def pickNextSimilarQuestion(self, QID):
        # FIXME
        # while True:
        # among the 1000 most similar questions, pick one
        num = randint(0, 1000)
        NextQID = self.QA_KB.MODEL.docvecs.most_similar(QID, topn = 1000)[num][0] # among top 1000 questions, pick one and then return question id
            # if NextQID not in self.ASKED:
        picked_question = self.QA_KB.QKB[NextQID].rstrip() # find the question based on the question id
                # self.ASKED.append(NextQID)
            # break                 
        return picked_question, NextQID
    
    # def computeScore(self, user_answer, QID):
    #     user_answer = user_answer.lower()
    #     picked_answer = self.AKB[QID].rstrip()
    #     answer = [picked_answer]
    #     answer.append(user_answer)
    #     self.tfidf_features = TfidfVectorizer().fit_transform(answer)
    #     cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
    #     print("Similarity between the standard answer and yours is: " + str(int(cosine_similarities[1]*10)))
    #     return picked_answer, int(cosine_similarities[1]*10)

    # def get_support(self, QID):
    #     return self.SKB[QID]    



