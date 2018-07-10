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
        self.queues = [Queue()]
        self.curr_q = 0 
        self.curr_item = None
        self.normalize = lambda x: x / x.sum()

        for i in range(self.num_items):
            self.queues[0].put(i)

    # goes through the queues to figure out the next item
    def pickNextQuestion(self):
        num_queues = len(self.queues)
        # sampling distribution of 1/sqrt(i) for non-empty queues 
        sampling_rates = 1 / np.sqrt(np.arange(1, num_queues))
        sampling_rates = np.array([x if not self.queues[i+1].empty() else 0 for i,x in enumerate(sampling_rates)])

        # sample bucket 0 with arrival prob
        arrival_prob = self.arrival_prob if not self.queues[0].empty() else 0
        sampling_rates = np.concatenate((np.array([arrival_prob]), 
                                         self.normalize(sampling_rates)*(1-arrival_prob)))
        p = self.normalize(sampling_rates)
        print("sampling rates are", p)

        if self.queues[0].qsize() == self.num_items: # no items have been shown yet
          self.curr_q = 0
        else:
          self.curr_q = np.random.choice(range(num_queues), p=p)
        self.curr_item = self.queues[self.curr_q].get(False)

        picked_question = self.QA_KB.QKB[self.curr_item]
        return picked_question, self.curr_item

    # updates the queues and the history 
    # outcome is either 0 or 1, if the user answered correctly 
    # item is the index of the last item
    def updateHistory(self, outcome):
        # demote 1 if wrong, promote 1 if correct
        next_q = max(1, self.curr_q + 2*outcome - 1)
        # extend num queues
        if next_q == len(self.queues):
            self.queues.append(Queue())
        self.queues[next_q].put(self.curr_item)