from abc import ABCMeta, abstractmethod
from gensim.models import Doc2Vec
from sentence_similarity.princeton_sif import sif_sentence_similarity
from sentence_similarity.sif_implementation import model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sentence_similarity.sif_implementation.wordembeddings import EmbeddingVectorizer
import random
from random import randint
import os
import pickle
from nltk import RegexpTokenizer


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
        picked_answer = super(TFIDFModel, self).getAnswer(QID)
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
        picked_answer = super(Doc2VecModel, self).getAnswer(QID)
        return picked_question, NextQID

class SIFModel(QAModel):
    """docstring for SIFModel"""
    def __init__(self, qa_kb):
        super(SIFModel, self).__init__(qa_kb)

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        #picked_answer = self.QA_KB.AKB[QID].rstrip()
        picked_answer = super(SIFModel, self).getAnswer(QID)
        score = sif_sentence_similarity.answer_similarity(user_answer, picked_answer)
        print("Similarity between the standard answer and yours is: " + str(int(score)))
        return score

class SIF2Model(QAModel):
    """docstring for SIF2Model"""
    def __init__(self, qa_kb, pkl_file):
        super(SIF2Model, self).__init__(qa_kb)
        self.tokenization(qa_kb.QKB, pkl_file)


    def tokenization(self, qkb, pkl_file):
        self.tokenizer = RegexpTokenizer(r'[\w]+')
        self.tokenized_sentences = model.preprocess(qkb, self.tokenizer)
        pkl = open(pkl_file, 'rb')
        glove = pickle.load(pkl)
        print("="*80+"\nloaded glove")
        self.emb = EmbeddingVectorizer(word_vectors=glove, weighted=True, R=True)
        self.V = self.emb.fit_transform(self.tokenized_sentences) # for QuizBot replace tokenized_sentences with the entire KB answers

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        #picked_answer = self.QA_KB.AKB[QID].rstrip()
        #picked_answer = super(SIF2Model, self).getAnswer(QID)
        picked_answer_tokenized = self.tokenized_sentences[QID]
        query = [user_answer]
        tokenized_query = model.preprocess(query, self.tokenizer)
        V_query = emb.transform(tokenized_query)
        #print("similarity: " + str(cosine_similarity(V_query[0], V[0]))+ "\n")

        score = model.cosine_similarity(V_query[0], picked_answer_tokenized)
        print("Similarity between the standard answer and yours is: " + str(int(score)))
        return score