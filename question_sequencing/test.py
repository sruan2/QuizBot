'''This is the test function for different question sequencing algorithms

2018 July 6
'''

from random_model import RandomSequencingModel
from QAKnowledgebase import QAKnowlegeBase


'''Module-level constants'''
ITERATIONS = 20


if __name__ == '__main__':
    # Read QA json data and construct the QA knowledge base
    json_file = '../QAdataset/questions_filtered_150_quizbot.json'
    qa_kb = QAKnowlegeBase(json_file)

    # Construct the question sequencing model from here
    random_model = RandomSequencingModel(qa_kb)


    # Run the simulation for 20 iterations
    for i in range(ITERATIONS):
        picked_question, QID = random_model.pickNextQuestion()
        print(QID)

