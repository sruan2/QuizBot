'''
    inconsistency_calculator_mturk.py
    Author: Liwei Jiang
    Date: 19/07/2018
    Usage: Check the number of inconsistent answer of the pre- and post- quizzes via Qualtrics.
'''
import csv
import sys
import json

file_name_1 = "QuizA_MTurk_1.csv"
file_name_2 = "QuizB_MTurk_1.csv"
result_file = "user_result_mturk_1.csv"
result_data = []

quiz_a_data = {}
quiz_b_data = {}

quiz_a_repeated_index = [14, 19, 21, 30, 34, 40, 43, 0, 3, 4, 8, 9, 14, 20, 21, 59, 30, 32, 34, 37, 40, 43, 54]
quiz_b_repeated_index = [36, 54, 44, 8, 15, 57, 43, 13, 22, 33, 52, 17, 36, 47, 44, 4, 8, 6, 15, 24, 57, 43, 19]
NUM_REPEATED = len(quiz_a_repeated_index)

with open(file_name_1, 'rt') as csvfile:
	reader = list(csv.reader(csvfile))
	quiz_a = reader[3:]

with open(file_name_2, 'rt') as csvfile:
	reader = list(csv.reader(csvfile))
	quiz_b = reader[3:]

for i in range(len(quiz_a)):
	quiz_a_data[quiz_a[i][17]] = quiz_a[i][22:-1]

for i in range(len(quiz_b)):
	quiz_b_data[quiz_b[i][17]] = quiz_b[i][22:-1]

result_data = [[x] for x in range(NUM_REPEATED)]
all_users = quiz_a_data.keys()
all_users.extend(x for x in quiz_b_data.keys() if x not in quiz_a_data.keys())

title = ["Question"]
stats = ["Insistent Answers"]

for user in all_users:
	if user in quiz_a_data.keys() and user in quiz_b_data.keys():
		title.append(user + ": QuizA")
		title.append(user + ": QuizB")
		inconsistent_count = 0
		for i in range(NUM_REPEATED):
			qa_index = quiz_a_repeated_index[i]
			qb_index = quiz_b_repeated_index[i]
			qa = quiz_a_data[user][5 * qa_index + 4]
			qb = quiz_b_data[user][5 * qb_index + 4]
			result_data[i].append(qa)
			result_data[i].append(qb)

			if qa != qb:
				inconsistent_count += 1

		stats.append(inconsistent_count)
		stats.append("")

result_data.insert(0, title)
result_data.append(stats)

with open(result_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(result_data)
