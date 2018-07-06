'''Random Question Sequencing Model

2018 July 5
'''

from base_model import BaseSequencingModel


class RandomSequencingModel(BaseSequencingModel):
    '''Pick next question randomly'''

    def pickNextQuestion(self):
        QID = randint(0, self.QA_KB.KBlength)
        picked_question = self.QA_KB.QKB[QID]
        return picked_question, QID
