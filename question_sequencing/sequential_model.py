'''Sequential Model

Sherry Ruan
2018 September
'''
from base_model import BaseSequencingModel
from collections import defaultdict
import random
from utils import SubjectEnoughQuestions, EnoughForToday, FinishFixQuestionsStudy


class SequentialModel(BaseSequencingModel):

    def __init__(self, qa_kb):
        BaseSequencingModel.__init__(self, qa_kb)
        # a dictionary mapping user id to a dictionary mapping qids to counts
        self.user_questions_counts = {"science":{}, "safety":{}, "gre":{}}
        self.block_counts = {}

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
            self.user_questions_counts[subject][user_id][question_idx] = 1

        if user_id not in self.block_counts:
            self.block_counts[user_id] = [80, 60, 40, 20]

    def pickNextQuestion(self, user_id=0, subject='random'):
        '''Pick next question randomly

        Returns:
            Data dictionary: {'question':
                              'qid' :
                              'correct_answer' :
                              'support' :
                              'distractor' : }
        '''
        # Initialize if the user does not existed in our dictionary
        for s in ('science', 'gre', 'safety'):
            if user_id not in self.user_questions_counts[s]:
                self.user_questions_counts[s][user_id] = {QID: 0 for QID in self.QA_KB.SubDict[s]}
        if user_id not in self.block_counts:
            self.block_counts[user_id] = [80, 60, 40, 20]

        # Get count of practices for each subject
        count = {}
        count['science'] = sum([count for count in self.user_questions_counts["science"][user_id].values()])
        count['gre'] = sum([count for count in self.user_questions_counts["gre"][user_id].values()])
        count['safety'] = sum([count for count in self.user_questions_counts["safety"][user_id].values()])
        total_count = sum(count.values())
        print('Sci count:', count['science'])
        print('GRE count:', count['gre'])
        print('Safety count:', count['safety'])
        print('All safety:', self.user_questions_counts["safety"][user_id])
        print('Total:', total_count)

        if total_count in self.block_counts[user_id]:
            print(self.block_counts[user_id])
            self.block_counts[user_id].pop()
            print(self.block_counts[user_id])
            raise EnoughForToday

        if total_count >= 96:
            raise FinishFixQuestionsStudy

        if subject == 'random':
            _QID_counts = {}
            _QID_subject ={}
            for _subject in ('science', 'safety', 'gre'):
                _subject_d = self.user_questions_counts[_subject][user_id]
                _qid = min(_subject_d, key=_subject_d.get)
                _QID_counts[_qid] = _subject_d[_qid]
                _QID_subject[_qid] = _subject
            QID = min(_QID_counts, key=_QID_counts.get)
            d = self.user_questions_counts[_QID_subject[QID]][user_id]
            d[QID] += 1
        else:
            d = self.user_questions_counts[subject][user_id]
            print(subject, d)
            # if subject is not random, then pick from the respective subject question bank
            QID = min(d, key=d.get)
            if d[QID] >= 2:
                raise SubjectEnoughQuestions
            d[QID] += 1
        print("Select {} (prev count={})".format(QID, d[QID]-1))

        data = {'question': self.QA_KB.QKB[QID],
                'qid': [QID, self.QA_KB.QID[QID]],
                'correct_answer': self.QA_KB.AKB[QID],
                'support': self.QA_KB.SKB[QID],
                'distractor': self.QA_KB.DKB[QID]}
        return data
