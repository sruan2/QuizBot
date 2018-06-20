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

<<<<<<< HEAD
''' remove the html syntax for the gre support text '''
def process_test():

    test_questions = []
=======

def process_test():
    ''' remove the html syntax for the gre support text '''
    
    test_questions = []

>>>>>>> f51626eb4c1eeb3e9ad991b03de3f8711824b799
    for q in questions:
        if q['subject'] == 'gre':
            cleanr = re.compile('<p>Here are the vocabulary definitions:</p><ul><li>')
            q['support'] = re.sub(cleanr, '', q['support'])
            cleanr = re.compile('</p><ul>')
            q['support'] = re.sub(cleanr, '</p>', q['support'])
            cleanr = re.compile('</li></ul>')
            q['support'] = re.sub(cleanr, '</p>', q['support'])
            cleanr = re.compile('<.*?>')
            q['support'] = re.sub(cleanr, '\n', q['support'])
<<<<<<< HEAD
            cleanr = re.compile(': ')
            q['support'] = re.sub(cleanr, ' -- ', q['support'])
=======
>>>>>>> f51626eb4c1eeb3e9ad991b03de3f8711824b799

    with open('questions_filtered_150_quizbot.json', 'w') as out_file:
        json.dump(questions, out_file, sort_keys=True, indent=4)


<<<<<<< HEAD
process_test()
=======
process_test()
>>>>>>> f51626eb4c1eeb3e9ad991b03de3f8711824b799
