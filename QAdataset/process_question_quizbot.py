# -*- coding: utf-8 -*-
'''
    process_question_quizbot.py
    Author: Liwei Jiang
    Date: 18/06/2018
    Usage: Remove the HTML syntax in GRE question for the quizbot messenger app.
'''
import json
import random
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
questions = []

with open('questions_filtered_150.json') as data_file:
    data = json.load(data_file)
    questions.extend(data)

def process_test():  
    ''' 
        remove the html syntax for the gre support text 
    '''
    test_questions = []
    for q in questions:
        if q['subject'] == 'gre':
            cleanr = re.compile('</li><li>')
            q['support'] = re.sub(cleanr, '\n\" ', q['support'])
            cleanr = re.compile('<.*?>')
            q['support'] = re.sub(cleanr, '', q['support'])
            cleanr = re.compile(': ')
            q['support'] = re.sub(cleanr, ' -- ', q['support'])
            cleanr = re.compile('Here are the vocabulary definitions:')
            q['support'] = re.sub(cleanr, '\" ', q['support'])

            q['support'] = q['support'].replace('\"', '📌')

    with open('questions_filtered_150_quizbot.json', 'w') as out_file:
        json.dump(questions, out_file, sort_keys=True, indent=4)

process_test()
