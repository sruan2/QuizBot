'''Random Question Sequencing Model

2018 July 5
'''
from random import randint, choice

from base_model import BaseSequencingModel



class RandomSequencingModel(BaseSequencingModel):
    '''Pick next question randomly'''

    def pickNextQuestion(self, subject = 'random'):
        if subject == 'random':
        	QID = randint(0, self.QA_KB.KBlength)
        # if subject is not random, then pick from the respective subject question bank
        else:
        	QID = choice(self.QA_KB.SubDict[subject])

        picked_question = self.QA_KB.QKB[QID]
        return picked_question, QID
