'''QA Model that is responsible for loading QA knowledge base, picking questions,
and computing similarity scores'''


import pickle
import math
from abc import abstractmethod
from gensim.models import Doc2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import tensorflow as tf
from keras.models import model_from_json
from nltk import RegexpTokenizer

from utils import pretty_print
from similarity_model.sif_implementation.wordembeddings import EmbeddingVectorizer
from similarity_model.sif_implementation import utils
from similarity_model import supervised_model
#from similarity_model.princeton_sif import sif_sentence_similarity
from question_sequencing.random_model import RandomSequencingModel
from question_sequencing.leitner_model import LeitnerSequencingModel
from question_sequencing.SM2_model import SM2SequencingModel
from question_sequencing.dash_model import DASHSequencingModel
from question_sequencing.sequential_model import SequentialModel
from QAKnowledgebase import QAKnowlegeBase

class QAModel(object):
    '''Base class of QAModel'''

    def __init__(self, qa_kb, sequencing_model):
        pretty_print("QAModel initialization", mode="QA Model")
        self.QID = 0
        self.QA_KB = qa_kb
        self.AKB = qa_kb.AKB
        self.DKB = qa_kb.DKB

        if sequencing_model == 'dash':
            self.sequencing_model = DASHSequencingModel(qa_kb)
        elif sequencing_model == 'leitner':
            self.sequencing_model = LeitnerSequencingModel(qa_kb)
        elif sequencing_model == 'sm2':
            self.sequencing_model = SM2SequencingModel(qa_kb)
        elif sequencing_model == 'sequential':
            self.sequencing_model = SequentailModel(qa_kb)
        else:
            self.sequencing_model = RandomSequencingModel(qa_kb)

    def pickQuestion(self, user_id, subject):
        '''Pick the next question based on the sequencing_model defined'''
        data = self.sequencing_model.pickNextQuestion(user_id, subject)
        picked_question = data['question']
        QID = data['qid']
        return picked_question, QID

    def updateHistory(self, user_id, user_data, effective_qids):
        self.sequencing_model.updateHistory(user_id, user_data, effective_qids)

    def loadUserData(self, sender_id, user_history_data, effective_qids):
        self.sequencing_model.loadUserData(sender_id, user_history_data, effective_qids)

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
    def computeScore(self, user_answer, QID): pass

class SupervisedSIFModeL(QAModel):
    """semi supervised version of the SIF model"""
    def __init__(self, qa_kb, sequencing_model='random'):
        super(SupervisedSIFModeL, self).__init__(qa_kb, sequencing_model)

        # load the current architecture from json
        with open('similarity_model/data_files/model_architecture.json', 'r') as f:
            self.model = model_from_json(f.read())
        self.graph = tf.get_default_graph()
        self.model.load_weights('similarity_model/data_files/model_weights.h5')

        # fit the embedding and load the glove model
        glove_file = 'similarity_model/data_files/mittens_model.pkl'
        json_file = 'QAdataset/questions_filtered_150_quizbot.json'

        self.emb = supervised_model.fit_model(glove_file, json_file)

    def computeScore(self, user_answer, QID):
        user_answer = [user_answer.lower()]
        picked_answer = [super(SupervisedSIFModeL, self).getAnswer(QID)]

        # returns a score from 1 to 5
        with self.graph.as_default():
            similarity = supervised_model.evaluate_model(self.model, self.emb, user_answer, picked_answer)

        # convert the score to appendn int between 0 and 10
        return round(((similarity - 1) * 10 / 4)[0])


class TFIDFModel(QAModel):
    """a working baseline model: TFIDF"""

    def __init__(self, qa_kb, sequencing_model='random'):
        super(TFIDFModel, self).__init__(qa_kb, sequencing_model)
        self.AKB = qa_kb.AKB
        self.DKB = qa_kb.DKB
        pretty_print('TFIDF Model')

    def computeScore(self, user_answer, QID):
        user_answer = user_answer.lower()
        picked_answer = super(TFIDFModel, self).getAnswer(QID)
        answer = [picked_answer]
        answer.append(user_answer)
        self.tfidf_features = TfidfVectorizer().fit_transform(answer)
        cosine_similarities = linear_kernel(
            self.tfidf_features[0:1], self.tfidf_features).flatten()
        return int(cosine_similarities[1]*10)


class Doc2VecModel(QAModel):
    """Doc2VecModel, pretrained by Zhengneng"""

    def __init__(self, qa_kb, sequencing_model='random'):
        pretrained_model_file = 'model_pre_trained/model_d2v_v1'
        super(Doc2VecModel, self).__init__(qa_kb, sequencing_model)
        # load the model in the very beginning
        self.MODEL = Doc2Vec.load(pretrained_model_file)
        pretty_print('Doc2Vec Model')

    def pickNextSimilarQuestion(self, QID):
        num = randint(0, 1000)
        # among top 1000 questions, pick one and then return question id
        NextQID = self.MODEL.docvecs.most_similar(QID, topn=1000)[num][0]
        picked_answer = super(Doc2VecModel, self).getAnswer(QID)
        return picked_question, NextQID


# Sherry: This is based on Princeton's original implementation. Not sure if this working, haven't tested it out yet.
class SIFModel(QAModel):
    def __init__(self, qa_kb, sequencing_model='random'):
        super(SIFModel, self).__init__(qa_kb, sequencing_model)
        pretty_print('SIF Model')

    def computeScore(self, user_answer, QID):
        user_answer = user_answer.lower()
        picked_answer = super(SIFModel, self).getAnswer(QID)
        score = sif_sentence_similarity.answer_similarity(
            user_answer, picked_answer)
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
        # just use the simple weighted version without removing PCA
        self.emb = EmbeddingVectorizer(
            word_vectors=self.glove, weighted=True, R=False)

    def computeScore(self, user_answer, QID):
        # transform the correct answer
        correct_answer = self.QA_KB.AKB[QID][0]
        tokenized_answer = utils.preprocess([correct_answer], self.tokenizer)
        V_answer = self.emb.transform(tokenized_answer)
        # transform the user's answer
        tokenized_query = utils.preprocess([user_answer], self.tokenizer)
        print(tokenized_query)
        not_empty = False
        for user_word in tokenized_query[0]:  # for out of vocabulary words
            if user_word in self.glove:
                not_empty = True
                break
        if not not_empty:
            # transformed V_query won't exist since it will be empty (nont of the words exist in glove)
            return -1
        V_query = self.emb.transform(tokenized_query)

        # Liwei: this line has a bug, so comment this out and add a fake score for running the app
        # score = math.ceil(utils.cosine_similarity(V_query[0], V_answer[0]) * 10)
        score = 0
        return score
