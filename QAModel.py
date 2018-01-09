from abc import ABCMeta, abstractmethod
from gensim.models import Doc2Vec
from sentence_similarity.princeton_sif import sif_sentence_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from random import randint

class QAModel:

    def __init__(self, qa_kb):
        print("\n" + str(os.getpid())+" tfidf initialization begins\n")
        self.QID = 0
        self.QA_KB = qa_kb
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

    def getAnswer(self):
		return self.QA_KB.AKB[QID].rstrip()
    
    @abstractmethod
    def pickNextSimilarQuestion(self): pass

    @abstractmethod
    def computeScore(self): pass


class TFIDFModel(qa_model):
    """docstring for TFIDFModel"""
    def __init__(self, qa_kb):
        super(TFIDFModel, self).__init__(qa_kb)

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        picked_answer = self.QA_KB.AKB[QID].rstrip()
        answer = [picked_answer]
        answer.append(user_answer)
        self.tfidf_features = TfidfVectorizer().fit_transform(answer)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        print("Similarity between the standard answer and yours is: " + str(int(cosine_similarities[1]*10)))
        return picked_answer, int(cosine_similarities[1]*10)   

class Doc2VecModel(qa_model):
    """docstring for Doc2VecModel"""
    def __init__(self, qa_kb, PreTrainedModel):
        super(Doc2VecModel, self).__init__(qa_model)
        self.MODEL = Doc2Vec.load(PreTrainedModel) # load the model in the very beginning

    def pickNextSimilarQuestion(self, QID):
        num = randint(0, 1000)
        NextQID = self.MODEL.docvecs.most_similar(QID, topn = 1000)[num][0] # among top 1000 questions, pick one and then return question id
        picked_question = self.QA_KB.QKB[NextQID].rstrip() # find the question based on the question id
        return picked_question, NextQID

class SIFModel(qa_model):
    """docstring for Doc2VecModel"""
    def __init__(self, qa_kb):
        super(SIFModel, self).__init__(qa_model)

    def compute_score(self, user_answer, QID):
        user_answer = user_answer.lower()
        picked_answer = self.QA_KB.AKB[QID].rstrip()
        score = sif_sentence_similarity.answer_similarity(user_answer, picked_answer)
        print("Similarity between the standard answer and yours is: " + str(int(score)))
        return picked_answer, int(score) 