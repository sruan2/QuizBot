import sys
import os
from abc import ABCMeta, abstractmethod
from gensim.models import Doc2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random
import pickle
from nltk import RegexpTokenizer
import math

from utils import pretty_print
from similarity_model.sif_implementation.wordembeddings import EmbeddingVectorizer
from similarity_model.sif_implementation import utils
#from similarity_model.princeton_sif import sif_sentence_similarity
from question_sequencing.random_model import RandomSequencingModel


class QAModel(object):

    def __init__(self, qa_kb):
        pretty_print("QAModel initialization", mode="QA Model")
        self.QID = 0
        self.QA_KB = qa_kb
        self.sequencing_model = RandomSequencingModel(qa_kb)

    def pickSubjectRandomQuestion(self, subject):
        subject = subject.lower()
        QID = random.choice(self.QA_KB.SubDict[subject])
        picked_question = self.QA_KB.QKB[QID]
        return picked_question, QID

    def pickRandomQuestion(self):
        return self.sequencing_model.pickNextQuestion()

    def pickQuestion(self, subject):

        if subject == "random":
            return self.sequencing_model.pickNextQuestion()
        else:
            subject = subject.lower()
            QID = random.choice(self.QA_KB.SubDict[subject])
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
            pretty_print("Index %d does not exist in AKB" % QID, mode='BUG!')
        return answer

    def getSupport(self, QID):
        try:
            support = self.QA_KB.SKB[QID]
        except:
            support = ""
            pretty_print("[Index %d does not exist in SKB" % QID, mode='BUG!')
        return support

    @abstractmethod
    def pickNextSimilarQuestion(self): pass

    @abstractmethod
    def computeScore(self): pass


class TFIDFModel(QAModel):
    """a working baseline model: TFIDF"""
    def __init__(self, qa_kb):
        super(TFIDFModel, self).__init__(qa_kb)
        self.AKB = qa_kb.AKB
        self.DKB = qa_kb.DKB
        pretty_print('TFIDF Model')

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        picked_answer = super(TFIDFModel, self).getAnswer(QID)
        answer = [picked_answer]
        answer.append(user_answer)
        self.tfidf_features = TfidfVectorizer().fit_transform(answer)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        return int(cosine_similarities[1]*10)


class Doc2VecModel(QAModel):
    """Doc2VecModel, pretrained by Zhengneng"""
    def __init__(self, qa_kb):
        pretrained_model_file = 'model_pre_trained/model_d2v_v1'
        super(Doc2VecModel, self).__init__(qa_kb)
        self.MODEL = Doc2Vec.load(pretrained_model_file) # load the model in the very beginning
        pretty_print('Doc2Vec Model')

    def pickNextSimilarQuestion(self, QID):
        num = randint(0, 1000)
        NextQID = self.MODEL.docvecs.most_similar(QID, topn = 1000)[num][0] # among top 1000 questions, pick one and then return question id
        picked_answer = super(Doc2VecModel, self).getAnswer(QID)
        return picked_question, NextQID

# Sherry: This is based on Princeton's original implementation. Not sure if this working, haven't tested it out yet.
class SIFModel(QAModel):
    def __init__(self, qa_kb):
        super(SIFModel, self).__init__(qa_kb)
        pretty_print('SIF Model')

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        picked_answer = super(SIFModel, self).getAnswer(QID)
        score = sif_sentence_similarity.answer_similarity(user_answer, picked_answer)
        return score

################### Sherry is fixing this, please do not touch ######################
class SIF2Model(QAModel):
    def __init__(self, qa_kb):
        pkl_file = 'model_pre_trained/glove/glove.6B.100d.pkl'
        super(SIF2Model, self).__init__(qa_kb)
        self.AKB = qa_kb.AKB
        self.DKB = qa_kb.DKB
        pkl = open(pkl_file, 'rb')
        self.glove = pickle.load(pkl, encoding='latin1')
        self.init_model(qa_kb.SKB)  # use support to fit
        pretty_print("Loaded "+pkl_file, mode="QA Model")
        pretty_print('SIF2 Model')

    def init_model(self, sentences):
        self.tokenizer = RegexpTokenizer(r'[\w]+')
        self.tokenized_sentences = utils.preprocess(sentences, self.tokenizer)
        self.emb = EmbeddingVectorizer(word_vectors=self.glove, weighted=True, R=False) # just use the simple weighted version without removing PCA

    def compute_score(self, user_answer, QID):
        # transform the correct answer
        correct_answer = self.QA_KB.AKB[QID][0]
        tokenized_answer = utils.preprocess([correct_answer], self.tokenizer)
        V_answer = self.emb.transform(tokenized_answer)
        # transform the user's answer
        tokenized_query = utils.preprocess([user_answer], self.tokenizer)
        print(tokenized_query)
        not_empty = False
        for user_word in tokenized_query[0]: # for out of vocabulary words
            if user_word in self.glove:
                not_empty = True
                break
        if not not_empty:
            return -1 # transformed V_query won't exist since it will be empty (nont of the words exist in glove)
        V_query = self.emb.transform(tokenized_query)

        # Liwei: this line has a bug, so comment this out and add a fake score for running the app
        # score = math.ceil(utils.cosine_similarity(V_query[0], V_answer[0]) * 10)
        score = 0
        return score





