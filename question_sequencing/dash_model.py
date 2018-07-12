'''Leitner Question Sequencing Model

2018 July 6
'''

from base_model import BaseSequencingModel
from queue import Queue
import numpy as np
import time

np.random.seed(42)

# set the weights for the windows, right now based on 1/sqrt(W-w+1)
def window_weights(num_windows):
    weights = 1 / (np.arange(1, num_windows + 1, 1))**0.5
    return weights[::-1] 

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class DASHSequencingModel(BaseSequencingModel):
    '''Pick next question using leitner sequence model'''
    def __init__(self, qa_kb, max_steps = 1000, num_windows = 100, threshold = 0.01, student_ability = 0, decay_student_ability = 0):
        BaseSequencingModel.__init__(self, qa_kb)
        self.num_items = self.QA_KB.KBlength
        self.num_windows = num_windows
        self.window_size = max_steps // self.num_windows
        self.curr_step = 0

        # set the last viewed time to be time at initialization
        self.last_viewed = np.ones(self.num_items) * time.time()

        # threshold indicates the value where we want to select recall probability closest to threshold
        self.threshold = threshold 

        # number correct and num attempts over all items
        self.num_correct = np.zeros((self.num_items, self.num_windows))
        self.num_attempts = np.zeros((self.num_items, self.num_windows))

        # parameters to be adjusted
        self.delay_coeff = np.exp(np.random.normal(0, 0.01))
        self.student_ability = student_ability
        self.decay_student_ability = decay_student_ability
        self.item_difficulties = np.random.normal(1,1,self.num_items) 
        self.decay_item_difficulties = np.exp(np.random.normal(1,1,self.num_items))
        window_cw = window_weights(self.num_windows)
        window_nw = window_weights(self.num_windows)
        self.window_weights_cw = np.tile(window_cw, self.num_items).reshape((self.num_items, self.num_windows))
        self.window_weights_nw = np.tile(window_nw, self.num_items).reshape((self.num_items, self.num_windows))

    # current window of the current step
    def current_window(self):
        return min(self.num_windows - 1, self.curr_step // self.window_size)

    # study history function to account for impact on recall 
    # sum_w (window_weight_cw * log(1+c_w) + window_weight_nw * log(1+n_w))
    def get_study_histories(self):
        curr_window = self.current_window()
        # do calculations up to the current window
        return (self.window_weights_cw[:,:curr_window]*np.log(1 + self.num_correct[:,:curr_window]) + 
            self.window_weights_nw[:,:curr_window]*np.log(1 + self.num_attempts[:,:curr_window])).sum(axis = 1)

    '''
    formula to get likelihoods m(1+r*D)^{-f})
    D is the time since the last review
    r is delay coefficient
    m = sigmoid(student_ability - item_difficulty + study_history)
    f = exp(decay_student_ability - decay_item_difficulty)
    '''
    def get_likelihoods(self):
        study_histories = self.get_study_histories()
        m = sigmoid(self.student_ability - self.item_difficulties + study_histories)
        f = np.exp(self.decay_item_difficulties - self.decay_student_ability)
        # time difference from last viewed
        self.update_time = time.time()
        delays = self.update_time - self.last_viewed
        return m / (1 + self.delay_coeff * delays)**f

    # random question selection
    def pickRandomQuestion(self, subject):
        if subject == 'random':
            QID = np.random.randint(0, self.QA_KB.KBlength)
        # if subject is not random, then pick from the respective subject question bank
        else:
            QID = np.random.choice(self.QA_KB.SubDict[subject])

        # set current item 
        self.curr_item = QID

        picked_question = self.QA_KB.QKB[QID]
        return picked_question, QID
 
    def thresholdPickQuestion(self, subject = 'random'):
        likelihoods = self.get_likelihoods() 
        # pick next item by closest to threshold
        if subject == 'random':
            id_list = list(range(self.num_items))
        else:
            id_list = self.QA_KB.SubDict[subject]

        # only set the threshold distances of the ids of the current subject
        threshold_distances = np.full(self.num_items, 999.0)
        distances = np.abs(likelihoods - self.threshold)
        np.put(threshold_distances, id_list, list(distances[id_list]))

        # self.curr_item = np.argmin(threshold_distances)
        self.curr_item = np.argmin(threshold_distances)
        print('likelihood is ', likelihoods[self.curr_item])
        picked_question = self.QA_KB.QKB[self.curr_item]
        return picked_question, self.curr_item

    # pick threshold based review every 10 steps, otherwise pick random
    def pickNextQuestion(self, subject = 'random'):
        if self.curr_step % 10 == 0:
            return self.thresholdPickQuestion(subject)
        else:
            return self.pickRandomQuestion(subject)
         
    # updates the queues and the history 
    # outcome is either 0 or 1, if the user answered correctly 
    # item is the index of the last item
    def updateHistory(self, outcome):
        curr_window = self.current_window()
        if outcome:
            self.num_correct[self.curr_item, curr_window] += 1
        self.num_attempts[self.curr_item, curr_window] += 1
        self.last_viewed[self.curr_item] = self.update_time
        self.curr_step += 1
