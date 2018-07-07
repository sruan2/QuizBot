'''This is the test function for different question sequencing algorithms

2018 July 6
'''

from random_model import RandomSequencingModel
from leitner_model import LeitnerSequencingModel
from SM2_model import SM2SequencingModel
from QAKnowledgebase import QAKnowlegeBase
import random

'''Module-level constants'''
ITERATIONS = 20


if __name__ == '__main__':
    # Read QA json data and construct the QA knowledge base
    json_file = '../QAdataset/questions_filtered_150_quizbot.json'
    qa_kb = QAKnowlegeBase(json_file)

    # Construct the question sequencing model from here
    model = LeitnerSequencingModel(qa_kb)

    # Run the simulation for 20 iterations
    for i in range(ITERATIONS):
        picked_question, QID = model.pickNextQuestion()
        outcome = 1 if random.random() < 0.9 else 0 
        model.updateHistory(outcome)
        print("item {} outcome {} current queue {}".format(QID, outcome, model.curr_q))

    model = SM2SequencingModel(qa_kb)

    for i in range(ITERATIONS):
    	picked_question, QID = model.pickNextQuestion()
    	outcome = 1 if random.random() < 0.9 else 0
    	model.updateHistory(outcome)
    	print("priority {}".format(model.order[0][0]))
    	print("item {} outcome {}".format(QID, outcome))
