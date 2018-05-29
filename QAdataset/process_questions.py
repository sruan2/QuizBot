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

pretest_questions = []
posttest_questions = []

for data in [science_questions, gre_questions, safety_questions]:

    random.shuffle(data)
    pre_data = data[:20]
    post_data = data[10:30]

    for i in range(10):
        post_data[i]['v'] = 'old'
    for i in range(10, 20):
        post_data[i]['v'] = 'new'

    pretest_questions.extend(pre_data)
    posttest_questions.extend(post_data)

random.shuffle(pretest_questions)
random.shuffle(posttest_questions)

with open('questions_pretest_60.json', 'w') as out_file:
    json.dump(pretest_questions, out_file)

with open('questions_posttest_60.json', 'w') as out_file:
    json.dump(posttest_questions, out_file)
