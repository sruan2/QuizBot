'''SuperMemo2 Question Sequencing Model

2018 July 6
'''
import heapq
import random
from collections import defaultdict

from base_model import BaseSequencingModel

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
        self.num_items = self.QA_KB.KBlength                        
        self.subjects = self.QA_KB.SubKB

        def init_order():
            subject_order = {subject : [] for subject in self.QA_KB.SubKB}
            questions = [Question(i) for i in range(self.num_items)]
            for subject, question_list in self.QA_KB.SubDict.items():
                for qid in question_list:
                    heapq.heappush(subject_order[subject], (qid, questions[qid]))
            return subject_order

        # maps from user id to the respective parameters necessary for the model
        self.cur_question = {}
        self.current_subject = {}
        self.user_subject_order = defaultdict(init_order)

    # get the time until next viewing
    def get_interval(self, n, question):
        ef = question.easiness
        if n == 0:
            return 4
        else:
            return self.get_interval(n-1, question)*ef

    def pickNextQuestion(self, user_id = 0, subject = 'random'):
        # pick a random subject if rando    m
        if subject == 'random':
            subject = random.choice(self.subjects)

        # update the current subject and get the order
        self.current_subject[user_id] = subject
        order = self.user_subject_order[user_id][subject]

        priority, question = heapq.heappop(order)
        self.cur_question[user_id] = question
        QID = question.id
        
        data = {'question' : self.QA_KB.QKB[QID],
                'qid' : QID,
                'correct_answer': self.QA_KB.AKB[QID],
                'support' : self.QA_KB.SKB[QID],
                'distractor' : self.QA_KB.DKB[QID]}

        return data

    # subjection to do update simulations to parameters
    def updateParameters(self, subject, question, outcome, user_id):
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
        heapq.heappush(self.user_subject_order[user_id][subject], (question.priority, question))
 

    def updateHistory(self, outcome, user_id = 0):
        '''update the easiness factor and the history'''
        question = self.cur_question[user_id]
        subject = self.current_subject[user_id]

        self.updateParameters(subject, question, outcome, user_id)
