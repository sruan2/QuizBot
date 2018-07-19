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
        # a dictionary mapping 150 questions to user's answer history
        self.correct_history = {}


    @abstractmethod
    def pickNextQuestion(self, subject = "random"):
        '''Return the next question customized for the given student
        Returns:
            picked_question: str of picked question text.
                Can be accessed using self.QA_KB.QKB[QID]
            QID: index of the picked question
        '''
        return None


    @abstractmethod
    def updateHistory(self, outcome):
        # TODO:
        # a history of correctness
        pass



