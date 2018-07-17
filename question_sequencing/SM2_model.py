'''SuperMemo2 Question Sequencing Model

2018 July 6
'''

from base_model import BaseSequencingModel
import heapq
import random

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
        self.subjects = self.QA_KB.SubKB
        self.current_subject = 'random'
        self.subject_order = {subject : [] for subject in self.QA_KB.SubKB}

        for subject, question_list in self.QA_KB.SubDict.items():
            for qid in question_list:
                heapq.heappush(self.subject_order[subject], (self.questions[qid].priority, self.questions[qid]))

    # get the time until next viewing
    def get_interval(self, n, question):
        ef = question.easiness
        if n == 0:
            return 4
        else:
            return self.get_interval(n-1, question)*ef

    def pickNextQuestion(self, subject = 'random'):
        # pick a random subject if random
        if subject == 'random':
            subject = random.choice(self.subjects)

        # update the current subject
        self.current_subject = subject
        order = self.subject_order[self.current_subject]

        priority, question = heapq.heappop(order)
        self.cur_question = question
        QID = question.id
        
        data = {'question' : self.QA_KB.QKB[QID],
                'qid' : QID,
                'correct_answer': self.QA_KB.AKB[QID],
                'support' : self.QA_KB.SKB[QID],
                'distractor' : self.QA_KB.DKB[QID]}

        return data

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
        heapq.heappush(self.subject_order[self.current_subject], (question.priority, question))
