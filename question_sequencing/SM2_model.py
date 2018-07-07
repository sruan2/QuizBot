'''SuperMemo2 Question Sequencing Model

2018 July 6
'''

from base_model import BaseSequencingModel
import heapq

class Question():
    def __init__(self, id):
        self.easiness = 2.5
        self.num_repetitions = 0
        self.priority = id
        self.id = id

    # for heap item comparison
    def __lt__(self, other):
        return self.id < other.id

class SM2SequencingModel(BaseSequencingModel):
    '''Pick next question using SM2 scheduling algorithm'''

    def __init__(self, qa_kb):
        BaseSequencingModel.__init__(self, qa_kb)
        self.cur_question = None       
        self.num_items = self.QA_KB.KBlength                        
        self.questions = [Question(i) for i in range(self.num_items)]
        self.order = []
        for i in range(self.num_items):
            heapq.heappush(self.order, (self.questions[i].priority, self.questions[i]))

    # get the time until next viewing
    def get_interval(self, n, question):
        ef = question.easiness
        if n == 0:
            return 4
        else:
            return self.get_interval(n-1, question)*ef

    def pickNextQuestion(self):
        priority, question = heapq.heappop(self.order)
        self.cur_question = question
        QID = question.id
        picked_question = self.QA_KB.QKB[QID]
        return picked_question, QID

    def updateHistory(self, outcome):
        '''update the easiness factor and the history'''
        question = self.cur_question
        if not outcome:
            question.num_repetitions = 0
        else:
            question.num_repetitions += 1
            # response should be a variable between 0 and 5, for now defaults to 3 if correct
            response = 3
            # don't update easiness factor lower than 1.3
            if question.easiness >= 1.3:
                question.easiness += 0.1 - (5-response)*(0.08+(5-response)*0.02)

        question.priority += self.get_interval(question.num_repetitions, question)
        heapq.heappush(self.order, (question.priority, question))
