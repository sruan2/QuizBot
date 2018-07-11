'''Leitner Question Sequencing Model

2018 July 6
'''

from base_model import BaseSequencingModel
from queue import Queue
import numpy as np
import time


class LeitnerSequencingModel(BaseSequencingModel):
    '''Pick next question using leitner sequence model'''

    def __init__(self, qa_kb, arrival_prob = 0.7):
        BaseSequencingModel.__init__(self, qa_kb)
        # probability selecting from group 0
        self.arrival_prob = arrival_prob 
        self.num_items = self.QA_KB.KBlength
        self.subjects = self.QA_KB.SubKB

        # subject queues maps frmo the subjects to the list of queues
        self.subject_queues = {subject : [Queue()] for subject in self.QA_KB.SubKB}
        self.curr_subject = 'random'
        self.curr_q = 0 
        self.curr_item = None
        self.normalize = lambda x: x / x.sum()

        # initialize the queues with all the qids
        for subject, question_list in self.QA_KB.SubDict.items():
            for qid in question_list:
                self.subject_queues[subject][0].put(qid)

    # goes through the queues to figure out the next item
    def pickNextQuestion(self, subject = 'random'):
        # pick a random subject if random
        if subject == 'random':
            subject = np.random.choice(self.subjects)

        # update the current subject
        self.curr_subject = subject

        queues = self.subject_queues[subject]
        num_queues = len(queues)
        # sampling distribution of 1/sqrt(i) for non-empty queues 
        sampling_rates = 1 / np.sqrt(np.arange(1, num_queues))
        sampling_rates = np.array([x if not queues[i+1].empty() else 0 for i,x in enumerate(sampling_rates)])

        # sample bucket 0 with arrival prob
        arrival_prob = self.arrival_prob if not queues[0].empty() else 0
        sampling_rates = np.concatenate((np.array([arrival_prob]), 
                                         self.normalize(sampling_rates)*(1-arrival_prob)))
        p = self.normalize(sampling_rates)
        print("sampling rates are", p)

        if queues[0].qsize() == self.num_items: # no items have been shown yet
          self.curr_q = 0
        else:
          self.curr_q = np.random.choice(range(num_queues), p=p)
        self.curr_item = queues[self.curr_q].get(False)

        picked_question = self.QA_KB.QKB[self.curr_item]
        return picked_question, self.curr_item

    # updates the queues and the history 
    # outcome is either 0 or 1, if the user answered correctly 
    # item is the index of the last item
    def updateHistory(self, outcome):
        # demote 1 if wrong, promote 1 if correct
        next_q = max(1, self.curr_q + 2*outcome - 1)
        # extend num queues
        if next_q == len(self.subject_queues[self.curr_subject]):
            self.subject_queues[self.curr_subject].append(Queue())
        self.subject_queues[self.curr_subject][next_q].put(self.curr_item)