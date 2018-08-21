'''Dash Question Sequencing Model
2018 July 6
'''
import numpy as np
import time
import random
from collections import defaultdict
from base_model import BaseSequencingModel

np.random.seed(42)


def window_weights(num_windows):
    '''Returns:
        the weights for the windows, right now based on 1/sqrt(W-w+1)
    '''
    weights = 1 / (np.arange(1, num_windows + 1, 1))**0.5
    return weights[::-1]


def sigmoid(x):
    '''sigmoid function'''
    return 1 / (1 + np.exp(-x))


class DASHSequencingModel(BaseSequencingModel):
    def __init__(self, qa_kb, max_steps=1000, num_windows=100, threshold=0.01,
                 student_ability=0, decay_student_ability=0, verbose=False):
        '''Sequencing model that uses DASH: Difficulty, Ability, Student History parameters
        to find memory likelihood probabilities for each question
        '''
        BaseSequencingModel.__init__(self, qa_kb)
        self.verbose = verbose
        self.num_items = self.QA_KB.KBlength
        self.num_windows = num_windows
        self.window_size = max_steps // self.num_windows
        self.max_steps = max_steps

        # threshold indicates the value where we want to select recall probability closest to threshold
        self.threshold = threshold

        # mapping from user id to users current step
        self.curr_step = defaultdict(int)
        self.curr_item = defaultdict(int)
        self.update_time = {}
        self.last_viewed = defaultdict(
            lambda: np.ones(self.num_items) * time.time())
        self.num_correct = defaultdict(
            lambda: np.zeros((self.num_items, self.num_windows)))
        self.num_attempts = defaultdict(
            lambda: np.zeros((self.num_items, self.num_windows)))

        # parameters to be adjusted, set to default values for now
        # self.delay_coeff = np.exp(np.random.normal(0, 0.01))
        self.delay_coeff = .01
        self.student_ability = student_ability
        self.decay_student_ability = decay_student_ability
        self.item_difficulties = np.random.normal(1, 1, self.num_items)
        self.decay_item_difficulties = np.exp(
            np.random.normal(1, 1, self.num_items))
        window_cw = window_weights(self.num_windows)
        window_nw = window_weights(self.num_windows)
        self.window_weights_cw = np.tile(window_cw, self.num_items).reshape(
            (self.num_items, self.num_windows))
        self.window_weights_nw = np.tile(window_nw, self.num_items).reshape(
            (self.num_items, self.num_windows))

    def get_current_window(self, step):
        '''Return: current window of the current step'''
        return (step % self.max_steps // self.window_size)

    def get_study_histories(self, user_id):
        '''study history function to account for impact on recall
        formula: sum_w (window_weight_cw * log(1+c_w) + window_weight_nw * log(1+n_w))
        '''
        curr_window = self.get_current_window(self.curr_step[user_id])
        # do calculations up to the current window
        return (self.window_weights_cw[:, :curr_window]*np.log(1 + self.num_correct[user_id][:, :curr_window]) +
                self.window_weights_nw[:, :curr_window]*np.log(1 + self.num_attempts[user_id][:, :curr_window])).sum(axis=1)

    def get_likelihoods(self, user_id):
        '''
        formula to get likelihoods m(1+r*D)^{-f})
        D is the time since the last review
        r is delay coefficient
        m = sigmoid(student_ability - item_difficulty + study_history)
        f = exp(decay_student_ability - decay_item_difficulty)
        '''
        study_histories = self.get_study_histories(user_id)
        m = sigmoid(self.student_ability -
                    self.item_difficulties + study_histories)
        f = np.exp(self.decay_item_difficulties - self.decay_student_ability)
        # time difference from last viewed
        self.update_time[user_id] = time.time()
        delays = self.update_time[user_id] - self.last_viewed[user_id]
        return m * np.power(1 + self.delay_coeff * delays, -f)

    def pickRandomQuestion(self, user_id, subject):
        '''Method to select a random question, for breadth selection purposes

        Returns:
            Data dictionary: {'question':  
                              'qid' :  
                              'correct_answer' :
                              'support' : 
                              'distractor' : } 
        '''
        if subject == 'random':
            QID = random.randint(0, self.QA_KB.KBlength)
        else:
            # if subject is not random, then pick from the respective subject question bank
            QID = random.choice(self.QA_KB.SubDict[subject])

        data = {'question': self.QA_KB.QKB[QID],
                'qid': int(QID),
                'correct_answer': self.QA_KB.AKB[QID],
                'support': self.QA_KB.SKB[QID],
                'distractor': self.QA_KB.DKB[QID]}

        return data

    def thresholdPickQuestion(self, user_id, subject):
        '''Method to select a question given a threshold, figures out the most urgent question to review

        Returns:
            Data dictionary: {'question':  
                              'qid' :  
                              'correct_answer' :
                              'support' : 
                              'distractor' : }
        '''
        likelihoods = self.get_likelihoods(user_id)

        # prints out the likelihoods if verbose flag on
        if self.verbose:
            np.set_printoptions(suppress=True)
            print(likelihoods)

        # pick next item by closest to threshold
        if subject == 'random':
            id_list = list(range(self.num_items))
        else:
            id_list = self.QA_KB.SubDict[subject]

        # only set the threshold distances of the ids of the current subject
        threshold_distances = np.full(self.num_items, 999.0)
        distances = np.abs(likelihoods - self.threshold)
        np.put(threshold_distances, id_list, list(distances[id_list]))

        QID = np.argmin(threshold_distances)
        print('likelihood is ', likelihoods[QID])

        data = {'question': self.QA_KB.QKB[QID],
                'qid': int(QID),
                'correct_answer': self.QA_KB.AKB[QID],
                'support': self.QA_KB.SKB[QID],
                'distractor': self.QA_KB.DKB[QID]}

        return data

    def pickNextQuestion(self, user_id=0, subject='random'):
        '''pick threshold based review every 5 steps, otherwise pick random

        Returns:
            Data dictionary: {'question':  
                              'qid' :  
                              'correct_answer' :
                              'support' : 
                              'distractor' : } 
        '''
        if self.curr_step[user_id] % 5 == 0:
            data = self.thresholdPickQuestion(user_id, subject)
        else:
            data = self.pickRandomQuestion(user_id, subject)

        # ensure no repeated questions
        if data['qid'] == self.curr_item[user_id]:
            data = self.pickNextQuestion(user_id, subject)

        self.curr_item[user_id] = data['qid']

        return data    

    def updateHistory(self, user_id, user_data):
        '''outcome is either 0 or 1, if the user answered correctly
        item is the index of the last item

        Args:
           user_data: tuples of qid(int), outcome (float [0,1]), timestamp (str) 
        '''
        question, outcome, timestamp = user_data

        step = self.curr_step[user_id]
        self.curr_step[user_id] += 1
        curr_window = self.get_current_window(step)

        # convert timestamp string to seconds
        time_object = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        time_seconds = time.mktime(time_object)

        if outcome:
            self.num_correct[user_id][question, curr_window] += 1
        self.num_attempts[user_id][question, curr_window] += 1
        self.last_viewed[user_id][question] = time_seconds
    
