'''SuperMemo2 Question Sequencing Model

2018 July 6
'''
import heapq
from base_model import BaseSequencingModel

class Question():
	def __init__(self, id):
		self.last_rep = 0
		self.next_rep = 0
		self.time = 0
		self.easiness = 2.5
		self.id = id

class SM2SequencingModel(BaseSequencingModel):
    '''Pick next question randomly'''

    def __init__(self):
    	self.questionOrder = []
		self.num_items = self.QA_KB.KBlength			    		
		self.questions = [Question(i) for i in range(self.num_items)]

    def pickNextQuestion(self):
        picked_question = self.QA_KB.QKB[QID]
        return picked_question, QID
