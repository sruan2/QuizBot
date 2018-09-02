'''Sequential Model

Sherry Ruan
2018 September
'''
from base_model import BaseSequencingModel
from collections import defaultdict
import random
from utils import EnoughQuestions


class SequentialModel(BaseSequencingModel):

    def __init__(self, qa_kb):
        BaseSequencingModel.__init__(self, qa_kb)
        # a dictionary mapping user id to a dictionary mapping qids to counts
        self.user_questions_counts = {'science':{}, "safety":{}, "gre":{}}

    def updateHistory(self, user_id, user_data, effective_qids):
        '''outcome is either 0 or 1, if the user answered correctly
        item is the index of the last item
        Args:
           user_data: tuples of qid(int), outcome (float [0,1]), timestamp (str)
        '''
        question, outcome, timestamp = user_data
        if question not in effective_qids.keys():
            return
        question_idx = effective_qids[question]
        subject = self.QA_KB.SubKB[question_idx]
        if user_id in self.user_questions_counts[subject]:
            if question_idx in self.user_questions_counts[subject][user_id]:
                self.user_questions_counts[subject][user_id][question_idx] += 1
            else:
                self.user_questions_counts[subject][user_id][question_idx] = 1
        else:  # not in any dicts
            self.user_questions_counts[subject][user_id] = {QID: 0 for QID in self.QA_KB.SubDict[subject]}
            self.user_questions_counts[subject][user_id] = {question_idx: 1}

    def pickNextQuestion(self, user_id=0, subject='random'):
        '''Pick next question randomly

        Returns:
            Data dictionary: {'question':
                              'qid' :
                              'correct_answer' :
                              'support' :
                              'distractor' : }
        '''
        if subject == 'random':
            subject = random.choice(['science', 'gre', 'safety'])
            #QID = min(d, key=d.get)
            #QID = randint(0, self.QA_KB.KBlength-1)
        if user_id not in self.user_questions_counts[subject]:
            self.user_questions_counts[subject][user_id] = {QID: 0 for QID in self.QA_KB.SubDict[subject]}
            QID = random.choice(self.QA_KB.SubDict[subject])
            self.user_questions_counts[subject][user_id][QID] = 1
        else:
            d = self.user_questions_counts[subject][user_id]
            print(d)
            # if subject is not random, then pick from the respective subject question bank
            QID = min(d, key=d.get)
            if d[QID] >= 2:
                raise EnoughQuestions
            print("Count of {} is: {}".format(QID, d[QID]))
            d[QID] += 1

        data = {'question': self.QA_KB.QKB[QID],
                'qid': [QID, self.QA_KB.QID[QID]],
                'correct_answer': self.QA_KB.AKB[QID],
                'support': self.QA_KB.SKB[QID],
                'distractor': self.QA_KB.DKB[QID]}
        return data
