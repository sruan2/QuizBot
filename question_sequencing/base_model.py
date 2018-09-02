'''Base Question Sequencing Model which other sequencing models inherit
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
        pretty_print("Question sequencing model initialization",
                     mode="Seq Model")
        self.QA_KB = qa_kb
        # list of the users currently loaded into memory
        self.loaded_users = []

    def loadUserData(self, user_id, user_history_data, effective_qids):
        '''load the user data from a history file

        Args:
            user_history_data: a list of tuples representing qid (int), outcome (float [0,1]), timestamp (str)
        '''
        for user_data in user_history_data:
            self.updateHistory(user_id, user_data, effective_qids)

    @abstractmethod
    def pickNextQuestion(self, user_id=0, subject="random"):
        '''Return the next question customized for the given student
        Returns:
            Data dictionary: {'question':
                              'qid' :
                              'correct_answer' :
                              'support' :
                              'distractor' : }
        '''
        return None

    @abstractmethod
    def updateHistory(self, user_id, user_data, effective_qids):
        '''Update the model parameters after user answers question
        Args:
            user_data: tuples off qid(int), outcome (float [0,1]), timestamp (str)
            timestamp in form: "%Y-%m-%d %H:%M:%S"
        '''
        pass
