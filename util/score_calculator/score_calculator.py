'''
    split_quiz.py
    Author: Liwei Jiang
    Date: 02/07/2018
    Usage: Refine the 60-question quiz into 54-question quiz
    	   Split the 54-question quiz into two 27-question quiz with same difficulty level.
'''
import csv
import itertools
import random
import numpy
import json

quiz_a_gre_index = [0, 3, 8, 10, 13, 14, 15, 16, 18, 31, 34, 35, 38, 42, 48, 52, 53, 54]
quiz_a_safety_index = [5, 6, 7, 11, 20, 22, 24, 27, 29, 30, 32, 41, 43, 44, 50, 55, 58, 59]
quiz_a_science_index = [1, 2, 4, 9, 19, 21, 26, 28, 33, 36, 37, 39, 40, 45, 46, 49, 51, 57]
quiz_a_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59]
quiz_a_remove = [12, 17, 23, 25, 47, 56]

quiz_b_gre_index = [0, 3, 7, 12, 13, 15, 19, 22, 28, 29, 32, 34, 36, 41, 50, 52, 53, 58]
quiz_b_safety_index = [1, 4, 6, 8, 11, 16, 18, 23, 27, 30, 37, 42, 43, 46, 49, 51, 55, 59]
quiz_b_science_index = [2, 9, 10, 14, 17, 24, 25, 26, 31, 33, 35, 38, 39, 44, 45, 54, 56, 57]
quiz_b_index = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
quiz_b_remove = [5, 20, 21, 40, 47, 48]

a1 = [0, 1, 2, 3, 4, 5, 8, 10, 13, 14, 16, 18, 19, 20, 21, 22, 24, 26, 29, 32, 37, 41, 42, 46, 55, 57, 58]
b1 = [3, 6, 9, 11, 12, 13, 16, 18, 22, 24, 25, 27, 29, 30, 33, 36, 39, 44, 45, 46, 49, 50, 52, 54, 55, 56, 58]

a2 = [6, 7, 9, 11, 15, 27, 28, 30, 31, 33, 34, 35, 36, 38, 39, 40, 43, 44, 45, 48, 49, 50, 51, 52, 53, 54, 59]
b2 = [0, 1, 2, 4, 7, 8, 10, 14, 15, 17, 19, 23, 26, 28, 31, 32, 34, 35, 37, 38, 41, 42, 43, 51, 53, 57, 59]

quiz_a_repeated_index = [0, 3, 4, 6, 8, 9, 14, 15, 19, 21, 24, 26, 30, 32, 34, 37, 40, 43, 44, 54, 58, 59]
quiz_b_repeated_index = [13, 22, 33, 37, 52, 17, 36, 0, 54, 44, 11, 39, 8, 6, 15, 24, 57, 43, 1, 19, 49, 4]

def between_subject():
	quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

	quiz_a_question = []
	quiz_b_question = []

	quiz_a_answer = []
	quiz_b_answer = []

	with open(quiz_a_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_a_answer.append(reader[i - 1][1])
			
	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_b_answer.append(reader[i - 1][1])

	quiz_a_user_record_filename = "csv/between_subject_A.csv"
	quiz_b_user_record_filename = "csv/between_subject_B.csv"

	quiz_a_data = {}

	with open(quiz_a_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz_a = reader[3:]

	for i in range(len(quiz_a)):
		quiz_a_data[quiz_a[i][17]] = [quiz_a[i][5 * j + 4 + 29] for j in range(60)]

	all_users = quiz_a_data.keys()

	result_data = []

	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append([user, 0, 0, 0])

		for i in quiz_a_index:
			if quiz_a_data[user][i] == quiz_a_answer[i]:
				result_data[u][1] += 1

		for i in a1:
			if quiz_a_data[user][i] == quiz_a_answer[i]:
				result_data[u][2] += 1

		for i in a2:
			if quiz_a_data[user][i] == quiz_a_answer[i]:
				result_data[u][3] += 1

	print(result_data)
	print(len(result_data))

# def quiz_b_30_20():
# 	# quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
# 	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

# 	# quiz_a_question = []
# 	quiz_b_question = []

# 	# quiz_a_answer = []
# 	quiz_b_answer = []

# 	# with open(quiz_a_score_report_filename, 'rb') as csvfile:
# 	# 	reader = list(csv.reader(csvfile))
# 	# 	for i in range(len(reader)):
# 	# 		if len(reader[i]) >= 2:
# 	# 			if reader[i][1] == "Total":
# 	# 				quiz_a_answer.append(reader[i - 1][1])
			
# 	with open(quiz_b_score_report_filename, 'rb') as csvfile:
# 		reader = list(csv.reader(csvfile))
# 		for i in range(len(reader)):
# 			if len(reader[i]) >= 2:
# 				if reader[i][1] == "Total":
# 					quiz_b_answer.append(reader[i - 1][1])

# 	quiz_a_user_record_filename = "csv/Quiz_B_Flashcards_30_20.csv"
# 	quiz_b_user_record_filename = "csv/Quiz_B_QuizBot_30_20.csv"

# 	quiz_data = {}

# 	with open(quiz_a_user_record_filename, 'rt') as csvfile:
# 		reader = list(csv.reader(csvfile))
# 		quiz = reader[3:]

# 	for i in range(len(quiz)):
# 		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 4 + 19] for j in range(60)]

# 	with open(quiz_b_user_record_filename, 'rt') as csvfile:
# 		reader = list(csv.reader(csvfile))
# 		quiz = reader[3:]

# 	for i in range(len(quiz)):
# 		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 4 + 19] for j in range(60)]

# 	all_users = list(set(quiz_data.keys()) - set(['Zilin Ma']))

# 	question_index = {'Jacqueline': [51, 52, 35, 30, 57, 49, 53, 25, 23, 16, 17, 7, 59, 9, 2, 6, 18, 50, 15], \
# 					  'Jongho': [44, 45, 39, 24, 17, 26], \
# 					  # 'Zilin Ma': , \
# 					  'Veronica': [41, 35, 45, 49, 36, 37, 4, 53, 23, 13, 43, 30, 27, 55, 6, 56], \
# 					  'Cynthia': [10, 12, 58, 33, 35, 45, 39, 29, 32, 25, 0, 34, 13, 17, 9, 2, 56, 26, 44, 31, 54, 57, 24, 23, 43, 27, 11, 18, 38, 42, 1, 30, 49, 46, 4, 16, 8, 59, 55, 6, 37, 51, 50, 22, 36, 14, 7, 28, 41], \
# 					  'Laura': [12, 58, 33, 35, 45, 39, 29, 32, 3, 0, 34, 17, 9, 2, 56, 26, 44, 31, 54, 57, 24, 23, 43, 27, 11, 18, 38, 42, 1, 30, 49, 46, 4, 16, 8, 59, 55, 6, 37, 51, 52, 50, 22, 53, 36, 14, 15, 7, 28, 41, 19], \
# 					  'Eleni': [10, 12, 58, 35, 32, 25, 17, 9, 2, 56, 44, 54, 57, 23, 27, 18, 30, 8, 59, 51, 52, 50, 22, 53, 36, 15], \
# 					  'Jordan': [12, 33, 35, 45, 39, 29, 3, 0, 34, 17, 2, 56, 26, 44, 31, 54, 24, 23, 43, 27, 11, 18, 38, 42, 1, 30, 49, 4, 16, 8, 55, 6, 37, 51, 25, 53, 36, 14, 28, 41], \
# 					  'Courtney': [10, 12, 58, 35, 45, 39, 29, 32, 25, 34, 13, 9, 2, 26, 44, 31, 54, 57, 24, 23, 38, 3, 22, 53, 14, 7, 41], \
# 					  'Golrokh': [12, 58, 45, 39, 29, 32, 3, 0, 13, 17, 44, 24, 4, 16, 8, 59, 6, 52, 50, 22, 36, 15, 7, 41, 19]}

# 	result_data = []
# 	for u in range(len(all_users)):
# 		user = all_users[u]
# 		result_data.append([user, 0])
# 		for i in question_index[user]:
# 			if quiz_data[user][i] == quiz_b_answer[i]:
# 				result_data[u][1] += 1


# 	print(result_data)
# 	print(len(result_data))

def quiz_b_30_20():
	# quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

	# quiz_a_question = []
	quiz_b_question = []

	# quiz_a_answer = []
	quiz_b_answer = []

	# with open(quiz_a_score_report_filename, 'rb') as csvfile:
	# 	reader = list(csv.reader(csvfile))
	# 	for i in range(len(reader)):
	# 		if len(reader[i]) >= 2:
	# 			if reader[i][1] == "Total":
	# 				quiz_a_answer.append(reader[i - 1][1])
			
	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_b_answer.append(reader[i - 1][1])

	quiz_a_user_record_filename = "csv/Quiz_B_Flashcards_30_20.csv"
	quiz_b_user_record_filename = "csv/Quiz_B_QuizBot_30_20.csv"

	quiz_data = {}

	with open(quiz_a_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 4 + 19] for j in range(60)]

	with open(quiz_b_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 4 + 19] for j in range(60)]

	all_users = list(set(quiz_data.keys()) - set(['Zilin Ma']))

	question_index = {'Jacqueline': [51, 52, 35, 30, 57, 49, 53, 25, 23, 16, 17, 7, 59, 9, 2, 6, 18, 50, 15], \
					  'Jongho': [44, 45, 39, 24, 17, 26], \
					  # 'Zilin Ma': , \
					  'Veronica': [41, 35, 45, 49, 36, 37, 4, 53, 23, 13, 43, 30, 27, 55, 6, 56], \
					  'Cynthia': [10, 12, 58, 33, 35, 45, 39, 29, 32, 25, 0, 34, 13, 17, 9, 2, 56, 26, 44, 31, 54, 57, 24, 23, 43, 27, 11, 18, 38, 42, 1, 30, 49, 46, 4, 16, 8, 59, 55, 6, 37, 51, 50, 22, 36, 14, 7, 28, 41], \
					  'Laura': [12, 58, 33, 35, 45, 39, 29, 32, 3, 0, 34, 17, 9, 2, 56, 26, 44, 31, 54, 57, 24, 23, 43, 27, 11, 18, 38, 42, 1, 30, 49, 46, 4, 16, 8, 59, 55, 6, 37, 51, 52, 50, 22, 53, 36, 14, 15, 7, 28, 41, 19], \
					  'Eleni': [10, 12, 58, 35, 32, 25, 17, 9, 2, 56, 44, 54, 57, 23, 27, 18, 30, 8, 59, 51, 52, 50, 22, 53, 36, 15], \
					  'Jordan': [12, 33, 35, 45, 39, 29, 3, 0, 34, 17, 2, 56, 26, 44, 31, 54, 24, 23, 43, 27, 11, 18, 38, 42, 1, 30, 49, 4, 16, 8, 55, 6, 37, 51, 25, 53, 36, 14, 28, 41], \
					  'Courtney': [10, 12, 58, 35, 45, 39, 29, 32, 25, 34, 13, 9, 2, 26, 44, 31, 54, 57, 24, 23, 38, 3, 22, 53, 14, 7, 41], \
					  'Golrokh': [12, 58, 45, 39, 29, 32, 3, 0, 13, 17, 44, 24, 4, 16, 8, 59, 6, 52, 50, 22, 36, 15, 7, 41, 19]}

	result_data = []
	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append([user, 0])
		for i in question_index[user]:
			if quiz_data[user][i] == quiz_b_answer[i]:
				result_data[u][1] += 1


	print(result_data)
	print(len(result_data))


def quiz_b_40_10():
	# quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

	# quiz_a_question = []
	quiz_b_question = []

	# quiz_a_answer = []
	quiz_b_answer = []

	# with open(quiz_a_score_report_filename, 'rb') as csvfile:
	# 	reader = list(csv.reader(csvfile))
	# 	for i in range(len(reader)):
	# 		if len(reader[i]) >= 2:
	# 			if reader[i][1] == "Total":
	# 				quiz_a_answer.append(reader[i - 1][1])
			
	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_b_answer.append(reader[i - 1][1])

	quiz_a_user_record_filename = "csv/Quiz_B_Flashcard_40_10.csv"
	quiz_b_user_record_filename = "csv/Quiz_B_QuizBot_40_10.csv"

	quiz_data = {}

	with open(quiz_a_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	# for i in range(len(quiz)):
	# 	quiz_data[quiz[i][17]] = [quiz[i][5 * j + 17 + 60] for j in range(60)]

	print(len(quiz[0]))

	# with open(quiz_b_user_record_filename, 'rt') as csvfile:
	# 	reader = list(csv.reader(csvfile))
	# 	quiz = reader[3:]

	# for i in range(len(quiz)):
	# 	quiz_data[quiz[i][17]] = [quiz[i][5 * j + 4 + 54] for j in range(60)]

	all_users = quiz_data.keys()

	# print(quiz_data)
	# print(len(quiz[i]))

	# print(len(quiz_data['Tugce']))
	# print(len(quiz[i]))
	

	# question_index = {'Yi': [12, 44, 22, 53, 36, 15, 28, 18, 19], \
	# 				  'Tugce': [10, 59, 42, 35, 45, 39, 29, 4, 1, 23, 43, 54, 28, 55, 11, 56], \
	# 				  'Edgar': [10, 12, 58, 33, 35, 45, 39, 29, 32, 3, 34, 13, 17, 9, 2, 56, 26, 44, 31, 54, 57, 24, 23, 27, 38, 42, 1, 49, 46, 8, 59, 55, 6, 52, 25, 14, 19], \
	# 				  'Pingyu': [53, 9, 0, 37, 28], \
	# 				  'Dae Hyun': [12, 44, 33, 25, 50, 24, 29, 32, 53, 3, 0, 34, 13, 15, 7, 28, 41, 6, 22, 52], \
	# 				  'Tzu Yin': [14, 12, 36, 58, 31, 50, 38, 32, 53, 41, 0, 34, 13, 15, 7, 59, 2, 11, 22, 52], \
	# 				  'Marianne': [10, 12, 58, 33, 35, 45, 39, 29, 32, 3, 0, 34, 13, 17, 9, 2, 26, 44, 31, 54, 57, 24, 23, 11, 18, 38, 42, 30, 46, 4, 16, 8, 59, 55, 6, 37, 51, 52, 25, 50, 22, 53, 14, 15, 7, 28, 41, 19]}

	# result_data = []
	# for u in range(len(all_users)):
	# 	user = all_users[u]
	# 	result_data.append([user, 0])
	# 	for i in question_index[user]:
	# 		if quiz_data[user][i] == quiz_b_answer[i]:
	# 			result_data[u][1] += 1


	# print(result_data)
	# print(len(result_data))


if __name__ == "__main__":
	quiz_b_40_10()
