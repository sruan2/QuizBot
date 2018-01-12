from abc import ABCMeta, abstractmethod
from gensim.models import Doc2Vec
from sentence_similarity.princeton_sif import sif_sentence_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random
from random import randint
import os

class QAModel(object):

    def __init__(self, qa_kb):
        print("\n" + str(os.getpid())+" tfidf QAModel begins\n")
        self.QID = 0
        self.QA_KB = qa_kb
        print("\ntfidf initialization ends\n")

    def pickSubjectRandomQuestion(self, subject):
        print("=======================================================================================")
        subject = subject.lower()
        QID = random.choice(self.QA_KB.SubKB[subject])
        picked_question = self.QA_KB.QKB[QID].rstrip()
        return picked_question, QID

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

    def getAnswer(self, QID):
        return self.QA_KB.AKB[QID].rstrip()

    def getSupport(self, QID):
        return self.QA_KB.SKB[QID].rstrip()
    
    @abstractmethod
    def pickNextSimilarQuestion(self): pass

    @abstractmethod
    def computeScore(self): pass


class TFIDFModel(QAModel):
    """docstring for TFIDFModel"""
    def __init__(self, qa_kb):
        super(TFIDFModel, self).__init__(qa_kb)

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        #picked_answer = self.QA_KB.AKB[QID].rstrip()
        picked_answer = super().getAnswer(QID)
        answer = [picked_answer]
        answer.append(user_answer)
        self.tfidf_features = TfidfVectorizer().fit_transform(answer)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        print("Similarity between the standard answer and yours is: " + str(int(cosine_similarities[1]*10)))
        return int(cosine_similarities[1]*10)   

class Doc2VecModel(QAModel):
    """docstring for Doc2VecModel"""
    def __init__(self, qa_kb, PreTrainedModel):
        super(Doc2VecModel, self).__init__(qa_kb)
        self.MODEL = Doc2Vec.load(PreTrainedModel) # load the model in the very beginning

    def pickNextSimilarQuestion(self, QID):
        num = randint(0, 1000)
        NextQID = self.MODEL.docvecs.most_similar(QID, topn = 1000)[num][0] # among top 1000 questions, pick one and then return question id
        #picked_question = self.QA_KB.QKB[NextQID].rstrip() # find the question based on the question id
        picked_answer = getAnswer(QID)
        return picked_question, NextQID

class SIFModel(QAModel):
    """docstring for Doc2VecModel"""
    def __init__(self, qa_kb):
        super(SIFModel, self).__init__(qa_kb)

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        #picked_answer = self.QA_KB.AKB[QID].rstrip()
        picked_answer = super().getAnswer(QID)
        score = sif_sentence_similarity.answer_similarity(user_answer, picked_answer)
        print("Similarity between the standard answer and yours is: " + str(int(score)))
        return score