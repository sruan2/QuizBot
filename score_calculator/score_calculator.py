'''
    score_calculator.py
    Author: Liwei Jiang
    Date: 02/07/2018
    Usage: Calculate Scores for the pretest and posttest quizzes.
'''
import csv
import sys
import json

file_name_1 = sys.argv[1]
file_name_2 = sys.argv[2]
result_file = "user_result.csv"

pre_gre_index = [0, 4, 7, 12, 13, 15, 19, 21, 22, 28, 29, 32, 34, 36, 40, 41, 50, 52, 53, 58]
pre_safety_index = [1, 3, 6, 8, 11, 16, 18, 23, 27, 30, 37, 42, 43, 46, 47, 48, 49, 51, 55, 59]
pre_science_inex = [2, 5, 9, 10, 14, 17, 20, 24, 25, 26, 31, 33, 35, 38, 39, 44, 45, 54, 56, 57]

post_gre_index = [0, 4, 7, 12, 13, 15, 19, 21, 22, 28, 29, 32, 34, 36, 40, 41, 50, 52, 53, 58]
post_safety_index = [1, 3, 6, 8, 11, 16, 18, 23, 27, 30, 37, 42, 43, 46, 47, 48, 49, 51, 55, 59]
post_science_inex = [2, 5, 9, 10, 14, 17, 20, 24, 25, 26, 31, 33, 35, 38, 39, 44, 45, 54, 56, 57]

pre_gre = []
pre_safety = []
pre_science = []
pre_questions = []
pre_user_result = {}

post_gre = []
post_safety = []
post_science = []
post_questions = []
post_user_result = {}

with open(file_name_1, 'rb') as csvfile:
	reader = list(csv.reader(csvfile))
	for i in range(len(reader[0])):
		if i % 3 == 2:
			index = i/3 - 1
			if index < 60 and index > -1:
				pre_questions.append(reader[0][i])

	for i in range(1, len(reader)):
		pre_user_result[reader[i][2]] = reader[i][5:]

with open(file_name_2, 'rb') as csvfile:
	reader = list(csv.reader(csvfile))
	for i in range(len(reader[0])):
		if i % 3 == 2:
			index = i/3 - 1
			if index < 60 and index > -1:
				post_questions.append(reader[0][i])

	for i in range(1, len(reader)):
		post_user_result[reader[i][2]] = reader[i][5:]

pre_gre = [pre_questions[r] for r in pre_gre_index]
pre_safety = [pre_questions[r] for r in pre_safety_index]
pre_science = [pre_questions[r] for r in pre_science_inex]

post_gre = [post_questions[r] for r in post_gre_index]
post_safety = [post_questions[r] for r in post_safety_index]
post_science = [post_questions[r] for r in post_science_inex]

all_questions = [x for x in pre_questions]
all_questions.extend(x for x in post_questions if x not in pre_questions)

result_data = [[x] for x in pre_questions]
result_data.extend([x] for x in post_questions if x not in pre_questions)

all_users = pre_user_result.keys()
all_users.extend([x] for x in post_user_result.keys() if x not in pre_user_result.keys())

title = ["Question"]
stats = ["Insistent Answers"]

for user in all_users:
	title.append(user + ": pretest")
	title.append(user + ": posttest")
	inconsistent_count = 0
	if user in pre_user_result.keys() and user in post_user_result.keys():
		for q in all_questions:
			i = all_questions.index(q)

			answer_pre = ""
			answer_post = ""

			if q in pre_questions:
				index_pre = pre_questions.index(q)
				if pre_user_result[user][3 * index_pre + 1] == "0.00 / 1":
					result_data[i].append(pre_user_result[user][3 * index_pre])
					answer_pre = pre_user_result[user][3 * index_pre]
				else:
					result_data[i].append(pre_user_result[user][3 * index_pre + 1])
			else:
				result_data[i].append("")

			if q in post_questions:
				index_post = post_questions.index(q)
				if post_user_result[user][3 * index_post + 1] == "0.00 / 1":
					result_data[i].append(post_user_result[user][3 * index_post])
					answer_post = post_user_result[user][3 * index_post]
				else:
					result_data[i].append(post_user_result[user][3 * index_post + 1])
			else:
				result_data[i].append("")

			if answer_pre != "" and answer_post != "":
				if answer_pre != answer_post:
					inconsistent_count += 1;

	stats.append(inconsistent_count)
	stats.append("")

result_data.insert(0, title)
result_data.append(stats)

with open(result_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(result_data)




