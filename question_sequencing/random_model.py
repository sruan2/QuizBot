'''Random Question Sequencing Model

2018 July 5
'''
from random import randint, choice

from base_model import BaseSequencingModel
					  


class RandomSequencingModel(BaseSequencingModel):
	'''Pick next question randomly'''

	def pickNextQuestion(self, user_id = 0, subject = 'random'):
		if subject == 'random':
			QID = randint(0, self.QA_KB.KBlength)
		# if subject is not random, then pick from the respective subject question bank
		else:
			QID = choice(self.QA_KB.SubDict[subject])

		data = {'question' : self.QA_KB.QKB[QID],
				'qid' : QID,
				'correct_answer': self.QA_KB.AKB[QID],
				'support' : self.QA_KB.SKB[QID],
				'distractor' : self.QA_KB.DKB[QID]}
				
		return data
