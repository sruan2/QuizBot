import json
import random

# merge questions into one file

questions = []

for data_set in ['sci_data', 'safety_data', 'gre_data']:
    with open(data_set + '_filtered_50.json') as data_file:
        data = json.load(data_file)
        questions.extend(data)

for q in range(len(questions)):
    questions[q]['id'] = q + 1

with open('questions_filtered_150.json', 'w') as out_file:
    json.dump(questions, out_file)


# split questions into pre-test and post-test

def process_test(name, seed):

    random.seed(seed)

    science_questions = []
    gre_questions = []
    safety_questions = []

    for q in questions:
        if q['subject'] == 'gre':
            gre_questions.append(q)
        elif q['subject'] == 'safety':
            safety_questions.append(q)
        else:
            science_questions.append(q)

    test_questions = []

    for data in [science_questions, gre_questions, safety_questions]:

        random.shuffle(data)
        test_questions.extend(data[:20])

    random.shuffle(test_questions)

    with open(name, 'w') as out_file:
        json.dump(test_questions, out_file)

process_test('questions_pretest_60.json', 42)
process_test('questions_posttest_60.json', 448)
