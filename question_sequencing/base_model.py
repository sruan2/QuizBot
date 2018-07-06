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
        self.correct_history = None

    @abstractmethod
    def pickNextQuestion(self):
        '''Return the next question customized for the given student
        Returns:
            picked_question: str of picked question text.
                Can be accessed using self.QA_KB.QKB[QID]
            QID: index of the picked question
        '''
        return None

    def updateHistory(self):
        # TODO:
        # a history of correctness
        pass



