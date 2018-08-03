'''Leitner Question Sequencing Model
2018 July 6
'''
import numpy as np
import time
from queue import Queue
from collections import defaultdict

from .base_model import BaseSequencingModel


class Question():
    '''Question object that stores question id, subject and current queue
    '''

    def __init__(self, id, subject):
        # initially put everything in queue 0
        self.queue = 0
        self.id = id
        self.subject = subject


class LeitnerSequencingModel(BaseSequencingModel):
    '''Pick next question using leitner sequence model
    '''

    def __init__(self, qa_kb, arrival_prob=0.7):
        BaseSequencingModel.__init__(self, qa_kb)
        # probability selecting from group 0
        self.arrival_prob = arrival_prob
        self.num_items = self.QA_KB.KBlength
        self.subjects = self.QA_KB.SubKB
        self.normalize = lambda x: x / x.sum()

        def init_queues():
            '''initialize the queues with all the qids
            '''
            subject_queues = {subject: [Queue()]
                              for subject in self.QA_KB.SubKB}
            for subject, question_list in self.QA_KB.SubDict.items():
                for qid in question_list:
                    subject_queues[subject][0].put(Question(qid, subject))
            return(subject_queues)

        # subject queues maps from user to subjects to the list of queues
        self.curr_q = {}
        self.curr_subject = {}
        self.curr_question = {}
        self.user_subject_queues = defaultdict(init_queues)

    def pickNextQuestion(self, subject='random', user_id=0):
        '''goes through the queues to figure out the next item
        '''

        # pick a random subject if random
        if subject == 'random':
            subject = np.random.choice(self.subjects)

        # update the current subject
        self.curr_subject[user_id] = subject
        queues = self.user_subject_queues[user_id][subject]
        num_queues = len(queues)

        # sampling distribution of 1/sqrt(i) for non-empty queues
        sampling_rates = 1 / np.sqrt(np.arange(1, num_queues))
        sampling_rates = np.array(
            [x if not queues[i+1].empty() else 0 for i, x in enumerate(sampling_rates)])

        # sample bucket 0 with arrival prob
        arrival_prob = self.arrival_prob if not queues[0].empty() else 0
        sampling_rates = np.concatenate((np.array([arrival_prob]),
                                         self.normalize(sampling_rates)*(1-arrival_prob)))
        p = self.normalize(sampling_rates)
        print("sampling rates are", p)

        if queues[0].qsize() == self.num_items:  # no items have been shown yet
            self.curr_q[user_id] = 0
        else:
            self.curr_q[user_id] = np.random.choice(range(num_queues), p=p)
        # get the next question from the respective queue
        self.curr_question[user_id] = queues[self.curr_q[user_id]].get(False)

        QID = self.curr_question[user_id].id

        data = {'question': self.QA_KB.QKB[QID],
                'qid': QID,
                'correct_answer': self.QA_KB.AKB[QID],
                'support': self.QA_KB.SKB[QID],
                'distractor': self.QA_KB.DKB[QID]}

        return data

 
    def updateHistory(self, user_id, user_data):
        '''updates the queues and the history
        outcome is either 0 or 1, if the user answered correctly
        item is the index of the last item

        Args:
           user_data: tuples of qid(int), outcome (float [0,1]), timestamp (str) 
        '''
        _, outcome, timestamp = user_data
        question = self.curr_question[user_id]
        subject = question.subject

        # demote 1 if wrong, promote 1 if correct
        next_q = max(1, question.queue + 2*outcome - 1)

        # extend num queues
        if next_q == len(self.user_subject_queues[user_id][subject]):
            self.user_subject_queues[user_id][subject].append(Queue())
        self.user_subject_queues[user_id][subject][next_q].put(question)
