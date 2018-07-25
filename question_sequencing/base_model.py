'''Base Question Sequencing Model

2018 July 5
'''

import sys
sys.path.append('../')
from abc import abstractmethod

from utils import pretty_print

class BaseSequencingModel():

    def __init__(self, qa_kb):
        '''initialization of the question sequencing Model

        Args:
            qa_kb: knowledge base containing all question data
        '''
        pretty_print("Question sequencing model initialization", mode="Seq Model")
        self.QA_KB = qa_kb
        # list of the users currently loaded into memory
        self.loaded_users = []

    @abstractmethod
    def loadUserData(self, user_id, user_history_data): # user_history_data is a list of tuples (qid, score, time_stamp)
        pass

    @abstractmethod
    def pickNextQuestion(self, user_id = 0, subject = "random"):
        '''Return the next question customized for the given student
        Returns:
            picked_question: str of picked question text.
                Can be accessed using self.QA_KB.QKB[QID]
            QID: index of the picked question
        '''
        return None


    @abstractmethod
    def updateHistory(self, user_id, user_data): # user_data is a tuple (qid, score, time_stamp)
        # TODO:
        # a history of correctness
        pass



