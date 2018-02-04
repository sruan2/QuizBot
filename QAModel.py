import sys
from abc import ABCMeta, abstractmethod
from gensim.models import Doc2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from similarity_model.sif_implementation.wordembeddings import EmbeddingVectorizer
from similarity_model.sif_implementation import utils
from similarity_model.princeton_sif import sif_sentence_similarity
import random
from random import randint
import os
import pickle
from nltk import RegexpTokenizer


class QAModel(object):

    def __init__(self, qa_kb):
        print("[QUIZBOT] PID " + str(os.getpid())+": QAModel initialization begins")
        self.QID = 0
        self.QA_KB = qa_kb
        print("[QUIZBOT] PID " + str(os.getpid())+": QAModel initialization ends")

    def pickSubjectRandomQuestion(self, subject):
        subject = subject.lower()
        QID = random.choice(self.QA_KB.SubDict[subject])
        picked_question = self.QA_KB.QKB[QID]
        return picked_question, QID

    def pickRandomQuestion(self):
        QID = randint(0, self.QA_KB.KBlength)
        picked_question = self.QA_KB.QKB[QID]
        return picked_question, QID

    def pickLastQuestion(self, QID):
        picked_question = self.QA_KB.QKB[QID]
        return picked_question

    def getAnswer(self, QID):
        try:
            answer = self.QA_KB.AKB[QID][0]
        except:
            answer = ""
            print("[BUG] PID " + str(os.getpid())+": Index %d does not exist in AKB" % QID)
        return answer

    def getSupport(self, QID):
        try:
            support = self.QA_KB.SKB[QID]
        except:
            support = ""
            print("[BUG] PID " + str(os.getpid())+": Index %d does not exist in SKB" % QID)
        return support
    
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
        picked_answer = super(TFIDFModel, self).getAnswer(QID)
        answer = [picked_answer]
        answer.append(user_answer)
        self.tfidf_features = TfidfVectorizer().fit_transform(answer)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        return int(cosine_similarities[1]*10)   

class Doc2VecModel(QAModel):
    """docstring for Doc2VecModel"""
    def __init__(self, qa_kb, PreTrainedModel):
        super(Doc2VecModel, self).__init__(qa_kb)
        self.MODEL = Doc2Vec.load(PreTrainedModel) # load the model in the very beginning

    def pickNextSimilarQuestion(self, QID):
        num = randint(0, 1000)
        NextQID = self.MODEL.docvecs.most_similar(QID, topn = 1000)[num][0] # among top 1000 questions, pick one and then return question id
        picked_answer = super(Doc2VecModel, self).getAnswer(QID)
        return picked_question, NextQID

class SIFModel(QAModel):
    """docstring for SIFModel"""
    def __init__(self, qa_kb):
        super(SIFModel, self).__init__(qa_kb)

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        picked_answer = super(SIFModel, self).getAnswer(QID)
        score = sif_sentence_similarity.answer_similarity(user_answer, picked_answer)
        return score

################### Sherry is fixing this, please do not touch ######################
class SIF2Model(QAModel):
    """docstring for SIF2Model"""
    def __init__(self, qa_kb, pkl_file):
        super(SIF2Model, self).__init__(qa_kb)
        self.AKB = qa_kb.AKB
        self.init_model(qa_kb.SKB, pkl_file)  # use support to fit


    def init_model(self, akb, pkl_file):
        self.tokenizer = RegexpTokenizer(r'[\w]+')
        self.tokenized_sentences = utils.preprocess(akb, self.tokenizer)
        pkl = open(pkl_file, 'rb')
        glove = pickle.load(pkl, encoding='latin1')
        print("="*80+"\nloaded glove")
        self.emb = EmbeddingVectorizer(word_vectors=glove, weighted=True, R=False) # just use the simple weighted version without removing PCA

    def compute_score(self, user_answer, QID):
        with open("log", "a+") as f:
            tokenized_query = utils.preprocess([user_answer], self.tokenizer)
            V_query = self.emb.transform(tokenized_query)

            tokenized_answer = utils.preprocess([self.AKB[QID]], self.tokenizer)
            V_answer = self.emb.transform(tokenized_answer)          
        score = utils.cosine_similarity(V_query[0], V_answer[0])
        return score