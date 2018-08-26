'''
    score_calculator.py
    Author: Liwei Jiang
    Date: 02/07/2018
    Usage: calculate user quiz scores

'''
import csv
import itertools
import random
import numpy
import json

# question index in Qualtrics quiz A and quiz B
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

quiz_a_repeated_index = [ 0,    3,  4,  6,   8,  9,  14,  15, 19, 21, 24, 26, 30, 32,  34, 37, 40, 43, 44,  54, 58, 59]
quiz_b_repeated_index = [13,   22, 33, 37,  52, 17,  36,   0, 54, 44, 11, 39,  8,  6,  15, 24, 57, 43,  1,  19, 49,  4]

# unique question id in the 150 question pool
repeated_question_id =  [148, 111,  6, 93, 102, 21, 114, 146, 41, 37, 58, 11, 84, 90, 117, 44, 42, 53, 72, 127, 75, 79]

flashcard_id = [6, 9, 11, 15, 17, 18, 24, 29, 37, 41, 44, 46, 49, 51, 52, 55, 56, 58, 59, 73, 75, 76, 77, 83, 88, 89, 90, 99, 102, 104, 106, 111, 113, 114, 128, 130, 131, 133, 135, 141, 145, 148]
quizbot_id = [1, 2, 5, 8, 14, 19, 21, 25, 27, 30, 31, 32, 35, 38, 42, 45, 50, 53, 64, 65, 68, 72, 79, 82, 84, 87, 93, 94, 97, 100, 103, 112, 117, 118, 120, 121, 125, 127, 132, 136, 138, 143, 146, 147]

repeated_in_flashcard_id = [75, 37, 6, 41, 11, 44, 114, 111, 102, 148, 58, 90]
repeated_in_quizbot_id = [72, 42, 79, 146, 84, 21, 127, 117, 93, 53]

quiz_a_id = [5, 6, 11, 14, 15, 18, 21, 27, 31, 32, 35, 37, 41, 42, 44, 45, 46, 49, 51, 52, 53, 55, 58, 64, 65, 72, 75, 76, 79, 82, 84, 88, 90, 93, 94, 99, 100, 102, 103, 104, 111, 113, 114, 117, 125, 127, 128, 131, 132, 135, 136, 138, 146, 148]
quiz_b_id = [1, 2, 6, 8, 9, 11, 17, 19, 21, 24, 25, 29, 30, 37, 38, 41, 42, 44, 50, 53, 56, 58, 59, 68, 72, 73, 75, 77, 79, 83, 84, 87, 89, 90, 93, 97, 102, 106, 111, 112, 114, 117, 118, 120, 121, 127, 130, 133, 141, 143, 145, 146, 147, 148]

# dictionary mapping Qualtrics id to unique question id in the 150 question pool
quiz_a_to_id = {0: 148, 1: 49, 2: 18, 3: 111, 4: 6, 5: 51, 6: 93, 7: 94, 8: 102, 9: 21, 10: 128, 11: 82, 13: 135, 14: 114, 15: 146, 16: 113, 18: 131, 19: 41, 20: 55, 21: 37, 22: 52, 24: 58, 26: 11, 27: 64, 28: 14, 29: 88, 30: 84, 31: 103, 32: 90, 33: 32, 34: 117, 35: 136, 36: 31, 37: 44, 38: 132, 39: 45, 40: 42, 41: 76, 42: 104, 43: 53, 44: 72, 45: 5, 46: 15, 48: 100, 49: 27, 50: 65, 51: 35, 52: 138, 53: 125, 54: 127, 55: 99, 57: 46, 58: 75, 59: 79}
quiz_b_to_id = {0: 146, 1: 72, 2: 25, 3: 145, 4: 79, 6: 90, 7: 118, 8: 84, 9: 24, 10: 1, 11: 58, 12: 130, 13: 148, 14: 19, 15: 117, 16: 83, 17: 21, 18: 59, 19: 127, 22: 111, 23: 50, 24: 44, 25: 17, 26: 30, 27: 56, 28: 120, 29: 141, 30: 73, 31: 38, 32: 143, 33: 6, 34: 147, 35: 8, 36: 114, 37: 93, 38: 2, 39: 11, 41: 121, 42: 68, 43: 53, 44: 37, 45: 9, 46: 77, 49: 75, 50: 106, 51: 97, 52: 102, 53: 112, 54: 41, 55: 89, 56: 29, 57: 42, 58: 133, 59: 87}

a1_to_id = {0: 148, 1: 49, 2: 18, 3: 111, 4: 6, 5: 51, 8: 102, 10: 128, 13: 135, 14: 114, 16: 113, 18: 131, 19: 41, 20: 55, 21: 37, 22: 52, 24: 58, 26: 11, 29: 88, 32: 90, 37: 44, 41: 76, 42: 104, 46: 15, 55: 99, 57: 46, 58: 75}
a2_to_id = {6: 93, 7: 94, 9: 21, 11: 82, 15: 146, 27: 64, 28: 14, 30: 84, 31: 103, 33: 32, 34: 117, 35: 136, 36: 31, 38: 132, 39: 45, 40: 42, 43: 53, 44: 72, 45: 5, 48: 100, 49: 27, 50: 65, 51: 35, 52: 138, 53: 125, 54: 127, 59: 79}
b1_to_id = {3: 145, 6: 90, 9: 24, 11: 58, 12: 130, 13: 148, 16: 83, 18: 59, 22: 111, 24: 44, 25: 17, 27: 56, 29: 141, 30: 73, 33: 6, 36: 114, 39: 11, 44: 37, 45: 9, 46: 77, 49: 75, 50: 106, 52: 102, 54: 41, 55: 89, 56: 29, 58: 133}
b2_to_id = {0: 146, 1: 72, 2: 25, 4: 79, 7: 118, 8: 84, 10: 1, 14: 19, 15: 117, 17: 21, 19: 127, 23: 50, 26: 30, 28: 120, 31: 38, 32: 143, 34: 147, 35: 8, 37: 93, 38: 2, 41: 121, 42: 68, 43: 53, 51: 97, 53: 112, 57: 42, 59: 87}

# calculate the quiz A score for the between subject users (out of 54)
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


# calculate the scores of questions users have seen (30 + 20, Quiz B)
def quiz_b_30_20():
	quiz_score_report_filename = "csv/MTurk1_B_score_report.csv"
	quiz_question = []
	quiz_answer = []

	with open(quiz_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_answer.append(reader[i - 1][1])

	user_record_flashcard_filename = "csv/Quiz_B_Flashcards_30_20.csv"
	user_record_quizbot_filename = "csv/Quiz_B_Quizbot_30_20.csv"

	quiz_data = {}

	with open(user_record_flashcard_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 4 + 19] for j in range(60)]

	with open(user_record_quizbot_filename, 'rt') as csvfile:
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
					  'Golrokh': [12, 58, 45, 39, 29, 32, 3, 0, 13, 17, 44, 24, 4, 16, 8, 59, 6, 52, 50, 22, 36, 15, 7, 41, 19],\
					  'Sen': [10, 38, 33, 35, 45, 39, 3, 0, 14, 17, 9, 2, 56, 26, 44, 31, 54, 57, 24, 23, 43, 27, 18, 42, 1, 49, 46, 4, 16, 8, 59, 55, 6, 37, 51, 50, 53, 7, 41]}

	result_data = []
	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append([user, 0])
		for i in question_index[user]:
			if quiz_data[user][i] == quiz_answer[i]:
				result_data[u][1] += 1


	print(result_data)
	print(len(result_data))


# calculate the scores of questions users have seen (40 + 10, Quiz B)
def quiz_b_40_10():
	quiz_score_report_filename = "csv/Quiz_B_40_10_recall_score_report.csv"
	quiz_question = []
	quiz_answer = []

	with open(quiz_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_answer.append(reader[i - 1][1])

	user_record_flashcard_filename = "csv/Quiz_B_Flashcard_40_10.csv"
	user_record_quizbot_filename = "csv/Quiz_B_QuizBot_40_10.csv"

	quiz_data = {}

	with open(user_record_flashcard_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 91] for j in range(54)]
		for j in quiz_b_remove:
			quiz_data[quiz[i][17]].insert(j, '')

	with open(user_record_quizbot_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 100] for j in range(54)]
		for j in quiz_b_remove:
			quiz_data[quiz[i][17]].insert(j, '')

	all_users = quiz_data.keys()

	for i in quiz_b_remove:
		quiz_answer.insert(i, '')

	question_index = {'Yi': [12, 44, 22, 53, 36, 15, 28, 18, 19], \
					  'Tugce': [10, 59, 42, 35, 45, 39, 29, 4, 1, 23, 43, 54, 28, 55, 11, 56], \
					  'Edgar': [10, 12, 58, 33, 35, 45, 39, 29, 32, 3, 34, 13, 17, 9, 2, 56, 26, 44, 31, 54, 57, 24, 23, 27, 38, 42, 1, 49, 46, 8, 59, 55, 6, 52, 25, 14, 19], \
					  'Pingyu': [53, 9, 0, 37, 28], \
					  'Dae Hyun': [12, 44, 33, 25, 50, 24, 29, 32, 53, 3, 0, 34, 13, 15, 7, 28, 41, 6, 22, 52], \
					  'Tzu Yin': [14, 12, 36, 58, 31, 50, 38, 32, 53, 41, 0, 34, 13, 15, 7, 59, 2, 11, 22, 52], \
					  'Marianne': [10, 12, 58, 33, 35, 45, 39, 29, 32, 3, 0, 34, 13, 17, 9, 2, 26, 44, 31, 54, 57, 24, 23, 11, 18, 38, 42, 30, 46, 4, 16, 8, 59, 55, 6, 37, 51, 52, 25, 50, 22, 53, 14, 15, 7, 28, 41, 19],\
					  'Max': [10, 42, 44, 33, 54, 57, 24, 36, 53, 0, 8, 59, 41, 52], \
					  'Kimberly': [10, 38, 44, 33, 51, 35, 45, 57, 24, 12, 3, 25, 36, 34, 13, 17, 54, 28, 2, 41, 26]}

	result_data = []
	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append([user, 0])
		for i in question_index[user]:
			if quiz_data[user][i] == quiz_answer[i]:
				result_data[u][1] += 1


	print(result_data)
	print(len(result_data))


# calculate the scores of the repeated questions (30 + 20, Quiz A)
def quiz_a_30_20():
	quiz_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_question = []
	quiz_answer = []

	with open(quiz_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_answer.append(reader[i - 1][1])

	user_record_flashcard_filename = "csv/Quiz_A_Flashcard_30_20.csv"
	user_record_quizbot_filename = "csv/Quiz_A_Quizbot_30_20.csv"

	quiz_data = {}

	with open(user_record_flashcard_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 31] for j in range(60)]

	with open(user_record_quizbot_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 26] for j in range(60)]

	all_users = list(set(quiz_data.keys()))

	quiz_a_repeated_index = [0,     3,  4,  6,   8,  9,  14,  15, 19, 21, 24, 30, 32,  34, 37, 40, 43, 44,  58]
	# quiz_b_repeated_index = [13,   22, 33, 37,  52, 17,  36,   0, 54, 44, 11,  8,  6,  15, 24, 57, 43,  1,  49]

	result_data = []
	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append([user, 0])
		for i in quiz_a_repeated_index:
			if quiz_data[user][i] == quiz_answer[i]:
				result_data[u][1] += 1

	print(result_data)
	print(len(result_data))


# calculate the scores of the repeated questions (40 + 10, Quiz A)
def quiz_a_40_10():
	quiz_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_question = []
	quiz_answer = []

	with open(quiz_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_answer.append(reader[i - 1][1])

	user_record_flashcard_filename = "csv/Quiz_A_Flashcard_40_10.csv"
	user_record_quizbot_filename = "csv/Quiz_A_Quizbot_40_10.csv"

	quiz_data = {}

	with open(user_record_flashcard_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 32] for j in range(60)]

	with open(user_record_quizbot_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 33] for j in range(60)]

	all_users = list(set(quiz_data.keys()))

	quiz_a_repeated_index = [0,     3,  4,  6,   8,  9,  14,  15, 19, 21, 24, 30, 32,  34, 37, 40, 43, 44,  58]
	# quiz_b_repeated_index = [13,   22, 33, 37,  52, 17,  36,   0, 54, 44, 11,  8,  6,  15, 24, 57, 43,  1,  49]

	result_data = []
	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append([user, 0])
		for i in quiz_a_repeated_index:
			if quiz_data[user][i] == quiz_answer[i]:
				result_data[u][1] += 1

	print(result_data)
	print(len(result_data))


# calculate the scores of the repeated questions (5 * 10, Quiz B)
def quiz_b_between_subject():
	quiz_score_report_filename = "csv/MTurk1_B_score_report.csv"
	quiz_question = []
	quiz_answer = []

	with open(quiz_score_report_filename, 'r') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_answer.append(reader[i - 1][1])

	user_record_filename = "csv/Quiz_B_between_subject.csv"

	quiz_data = {}

	with open(user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		quiz_data[quiz[i][17]] = [quiz[i][5 * j + 47] for j in range(19)]
		after_attention_check = [quiz[i][5 * j + 48] for j in range(19, 54)]
		quiz_data[quiz[i][17]] = quiz_data[quiz[i][17]] + after_attention_check

		for j in quiz_b_remove:
			quiz_data[quiz[i][17]].insert(j, "None")

	print(quiz_data)

	all_users = list(set(quiz_data.keys()))

	result_data = []
	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append([user, 0])
		for i in b1:
			if quiz_data[user][i].lower() == quiz_answer[i].lower():
				result_data[u][1] += 1

	print("------ b1: ")
	print(result_data)


	result_data = []
	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append([user, 0])
		for i in b2:
			if quiz_data[user][i].lower() == quiz_answer[i].lower():
				result_data[u][1] += 1

	print("------ b2: ")
	print(result_data)


if __name__ == "__main__":
	quiz_b_between_subject()

















