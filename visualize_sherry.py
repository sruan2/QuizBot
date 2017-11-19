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
    def __init__(self, PreTrainedModel):
        # self.KB = reader.makeKB('Data/Aristo-Mini-Corpus-Dec2016/Aristo-Mini-Corpus-In-Parts/CurrentWebCorpus-allSources-v1.txt')
        print("\n" + str(os.getpid())+" tfidf initialization begins\n")
        self.QKB = [] # question
        self.SKB = [] # support
        self.AKB = [] # answer
        self.KBlength = 0
        self.QCNT = 0
        self.QID = 0
        self.ASKED = []
        self.MODEL = Doc2Vec.load(PreTrainedModel)
        print("\ntfidf initialization ends\n")
    
    def appendQuestionKB(self, QuestionFile):
        with open(QuestionFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+QuestionFile)
            for line in f:
                self.QKB.append(line)
        print("="*87+"\n"+"Question KB is appended. Length is: "+str(len(self.QKB)))
        self.KBlength = len(self.QKB)

    def appendSupportKB(self, SupportFile):
        with open(SupportFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+SupportFile)
            for line in f:
                self.SKB.append(line)
        print("="*87+"\n"+"Support KB is appended. Length is: "+str(len(self.SKB)))

    def appendCorrectAnswerKB(self, CorrectAnswerFile):
        with open(CorrectAnswerFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+CorrectAnswerFile)
            for line in f:
                self.AKB.append(line)
        print("="*87+"\n"+"Correct Answer KB is appended. Length is: "+str(len(self.AKB)))

    def LoadQuery(self):
        query = raw_input("="*87+"\n"+"Enter a query: ")
        print("="*87+"\n"+"Your query is: "+query)
        self.QKB = [query] + self.QKB # concat
        self.query = query
        return query 
    
    def Featurize(self, query):
        self.QKB = [query] + self.QKB # concat
        #self.query = query

        self.tfidf_features = TfidfVectorizer().fit_transform(self.QKB)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-10:-1]
        # print("=======================================================================================")
        # print("QUERY:{}".format(self.query)) 
        # print("=======================================================================================")
        # i = 1
        index = related_docs_indices[1]
        # for index in related_docs_indices[1:]:
        #     print("Candidate {} - (Index: {}; Similarity: {:5.4f})".format(i, index, cosine_similarities[index]))
        #     question = self.QKB[index]
        #     # if len(question) > 80:
        #     #     question = question[:80] + '...'
        #     print(question)
        #     i += 1
        #     print("---------------------------------------------------------------------------------------")
        # index = raw_input("="*87+"\n"+"Enter an Index: ")
        # support = self.SKB[int(index)-1]
        # print(support)
        print("Here is the answer!\n")
        return self.AKB[int(index)-1]

    def pickRandomQuestion(self):
        print("=======================================================================================")
        QID = randint(0, self.KBlength)
        picked_question = self.QKB[QID].rstrip()

        # print(picked_question)
        # user_answer = raw_input("Enter Your Answer:")
        # answer.append(user_answer)
        # print("Standard Answer is: "+picked_answer)

        return picked_question, QID

    def pickNextSimilarQuestion(self, QID):
        # FIXME
        index = 0
        while True:
            num = randint(0, 1000)
            NextQID = self.MODEL.docvecs.most_similar(QID, topn = 1000)[index][num]
            if NextQID not in self.ASKED:
                picked_question = self.QKB[NextQID].rstrip()
                self.ASKED.append(NextQID)
                break
            else:
                index += 1
                            
        return pick_question, NextQID
    
    def computeScore(self, user_answer, QID):
        picked_answer = self.AKB[QID].rstrip()
        answer = [picked_answer]
        answer.append(user_answer)
        self.tfidf_features = TfidfVectorizer().fit_transform(answer)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        print("Similarity between the standard answer and yours is: " + str(cosine_similarities[1]))
        return picked_answer, cosine_similarities[1]

    def get_support(self, QID):
        return self.SKB[QID]    
               
if __name__ == '__main__':
    tfidf = tfidfTransform('model_pre_trained/model_d2v_v1')
    tfidf.appendQuestionKB('Data/SciQdataset-23/question_file_2.txt')
    tfidf.appendSupportKB('Data/SciQdataset-23/support_file_2.txt')  
    tfidf.appendCorrectAnswerKB('Data/SciQdataset-23/correct_answer_file_2.txt')
    while True: 
        if self.QCNT == 0:
            quesiton, qid = tfidf.pickRandomQuestion()
        quesiton, qid = tfidf.pickNextSimilarQuestion(qid)
        self.QCNT += 1
        # tfidf.LoadQuery()
        # tfidf.Featurize()


