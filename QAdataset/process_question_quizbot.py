'''
    process_question_quizbot.py
    Author: Liwei Jiang
    Date: 18/06/2018
    Usage: Remove the HTML syntax in GRE question for the quizbot messenger app.
'''

import json
import random
import re

questions = []

with open('questions_filtered_150.json') as data_file:
    data = json.load(data_file)
    questions.extend(data)

'''  '''

def process_test():

    test_questions = []

    for q in questions:
        if q['subject'] == 'gre':
            cleanr = re.compile('</p><ul>')
            q['support'] = re.sub(cleanr, '</p>', q['support'])
            cleanr = re.compile('</li></ul>')
            q['support'] = re.sub(cleanr, '</p>', q['support'])
            cleanr = re.compile('</li><li>')
            q['support'] = re.sub(cleanr, '</p>', q['support'])
            cleanr = re.compile('<.*?>')
            q['support'] = re.sub(cleanr, '\n', q['support'])

    with open('questions_filtered_150_quizbot.json', 'w') as out_file:
        json.dump(questions, out_file, sort_keys=True, indent=4)


process_test()