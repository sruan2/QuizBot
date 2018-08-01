'''This is the test function for different question sequencing algorithms

2018 July 6
'''

import random
import time

from random_model import RandomSequencingModel
from leitner_model import LeitnerSequencingModel
from SM2_model import SM2SequencingModel
from dash_model import DASHSequencingModel
from QAKnowledgebase import QAKnowlegeBase


'''Module-level constants'''
ITERATIONS = 100


if __name__ == '__main__':
    # Read QA json data and construct the QA knowledge base
    json_file = '../QAdataset/questions_filtered_150_quizbot.json'
    qa_kb = QAKnowlegeBase(json_file)

    model = RandomSequencingModel(qa_kb)

    for i in range(ITERATIONS):
        data = model.pickNextQuestion(user_id = 5, subject = 'science')
        print(data['qid'])
        
    # Construct the question sequencing model from here
    model = LeitnerSequencingModel(qa_kb)

    # Run the simulation for 20 iterations
    for i in range(ITERATIONS):
        data = model.pickNextQuestion(user_id = 5, subject = 'science')
        outcome = 1 if random.random() < 0.9 else 0

        user_data = (data['qid'], outcome, "")
        model.updateHistory(5, user_data)

        print("item {} outcome {} ".format(data['qid'], outcome))

    model = SM2SequencingModel(qa_kb)

    for i in range(ITERATIONS):
        data = model.pickNextQuestion(subject = 'science', user_id = 5)
        outcome = 1 if random.random() < 0.6 else 0

        user_data = (data['qid'], outcome, "")
        model.updateHistory(5, user_data)
        
        print("item {} outcome {}".format(data['qid'], outcome))

    user_id = 5

    model = DASHSequencingModel(qa_kb, verbose = False)
    for i in range(ITERATIONS):
        data = model.pickNextQuestion(user_id, 'science')
        outcome = 1 if random.random() < 0.5 else 0

        current_time = model.update_time[user_id]
        time_object = time.localtime(int(current_time))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time_object)

        user_data = (data['qid'], outcome, timestamp)
        model.updateHistory(5, user_data)
        time.sleep(0.5)
        print("item {} outcome {}".format(data['qid'], outcome))
