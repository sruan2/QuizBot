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

# MTurk1 data report from 65 users
quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

# MTurk1 data record from 65 users
quiz_a_user_record_filename = "csv/MTurk1_A_user_record.csv"
quiz_b_user_record_filename = "csv/MTurk1_B_user_record.csv"

# Question pool files
between_subjects_flashcard_filename = "json/questions_between_subjects_flashcard.json"
between_subjects_quizbot_filename = "json/questions_between_subjects_quizbot.json"

# batch4 score report and user record files
batch4_score_report_filename = "csv/batch4_score_report.csv"
batch4_user_record_filename = "csv/batch4_user_record.csv"

# question index in Qualtrics quiz a and quiz b, plus 1 for the Qualtrics question id
quiz_a_gre_index = [0, 3, 8, 10, 13, 14, 15, 16, 18, 31, 34, 35, 38, 42, 48, 52, 53, 54]
quiz_a_safety_index = [5, 6, 7, 11, 20, 22, 24, 27, 29, 30, 32, 41, 43, 44, 50, 55, 58, 59]
quiz_a_science_index = [1, 2, 4, 9, 19, 21, 26, 28, 33, 36, 37, 39, 40, 45, 46, 49, 51, 57]
quiz_a_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59]

# Qualtrics indices for the 6 removed questions in quiz a
quiz_a_remove = [12, 17, 23, 25, 47, 56]

quiz_b_gre_index = [0, 3, 7, 12, 13, 15, 19, 22, 28, 29, 32, 34, 36, 41, 50, 52, 53, 58]
quiz_b_safety_index = [1, 4, 6, 8, 11, 16, 18, 23, 27, 30, 37, 42, 43, 46, 49, 51, 55, 59]
quiz_b_science_index = [2, 9, 10, 14, 17, 24, 25, 26, 31, 33, 35, 38, 39, 44, 45, 54, 56, 57]
quiz_b_index = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]

# Qualtrics indices for the 6 removed questions in quiz b
quiz_b_remove = [5, 20, 21, 40, 47, 48]

# Qualtrics indices of a1, a2, b1, b2, each has 27 questions
a1 = [0, 1, 2, 3, 4, 5, 8, 10, 13, 14, 16, 18, 19, 20, 21, 22, 24, 26, 29, 32, 37, 41, 42, 46, 55, 57, 58]
b1 = [3, 6, 9, 11, 12, 13, 16, 18, 22, 24, 25, 27, 29, 30, 33, 36, 39, 44, 45, 46, 49, 50, 52, 54, 55, 56, 58]

a2 = [6, 7, 9, 11, 15, 27, 28, 30, 31, 33, 34, 35, 36, 38, 39, 40, 43, 44, 45, 48, 49, 50, 51, 52, 53, 54, 59]
b2 = [0, 1, 2, 4, 7, 8, 10, 14, 15, 17, 19, 23, 26, 28, 31, 32, 34, 35, 37, 38, 41, 42, 43, 51, 53, 57, 59]

# there are 22 repeated questions appearing in both quiz a and quiz b
quiz_a_repeated_index = [ 0,    3,  4,  6,   8,  9,  14,  15, 19, 21, 24, 26, 30, 32,  34, 37, 40, 43, 44,  54, 58, 59]
quiz_b_repeated_index = [13,   22, 33, 37,  52, 17,  36,   0, 54, 44, 11, 39,  8,  6,  15, 24, 57, 43,  1,  19, 49,  4]

# qid in the 150 question pool
repeated_question_qid =  [148, 111,  6, 93, 102, 21, 114, 146, 41, 37, 58, 11, 84, 90, 117, 44, 42, 53, 72, 127, 75, 79]

flashcard_qid = [6, 9, 11, 15, 17, 18, 24, 29, 37, 41, 44, 46, 49, 51, 52, 55, 56, 58, 59, 73, 75, 76, 77, 83, 88, 89, 90, 99, 102, 104, 106, 111, 113, 114, 128, 130, 131, 133, 135, 141, 145, 148]
quizbot_qid = [1, 2, 5, 8, 14, 19, 21, 25, 27, 30, 31, 32, 35, 38, 42, 45, 50, 53, 64, 65, 68, 72, 79, 82, 84, 87, 93, 94, 97, 100, 103, 112, 117, 118, 120, 121, 125, 127, 132, 136, 138, 143, 146, 147]

repeated_in_flashcard_qid = [75, 37, 6, 41, 11, 44, 114, 111, 102, 148, 58, 90]
repeated_in_quizbot_qid = [72, 42, 79, 146, 84, 21, 127, 117, 93, 53]

quiz_a_qid = [5, 6, 11, 14, 15, 18, 21, 27, 31, 32, 35, 37, 41, 42, 44, 45, 46, 49, 51, 52, 53, 55, 58, 64, 65, 72, 75, 76, 79, 82, 84, 88, 90, 93, 94, 99, 100, 102, 103, 104, 111, 113, 114, 117, 125, 127, 128, 131, 132, 135, 136, 138, 146, 148]
quiz_b_qid = [1, 2, 6, 8, 9, 11, 17, 19, 21, 24, 25, 29, 30, 37, 38, 41, 42, 44, 50, 53, 56, 58, 59, 68, 72, 73, 75, 77, 79, 83, 84, 87, 89, 90, 93, 97, 102, 106, 111, 112, 114, 117, 118, 120, 121, 127, 130, 133, 141, 143, 145, 146, 147, 148]

# dictionaries mapping Qualtrics id to qid in the 150 question pool, 54 questions
quiz_a_to_qid = {0: 148, 1: 49, 2: 18, 3: 111, 4: 6, 5: 51, 6: 93, 7: 94, 8: 102, 9: 21, 10: 128, 11: 82, 13: 135, 14: 114, 15: 146, 16: 113, 18: 131, 19: 41, 20: 55, 21: 37, 22: 52, 24: 58, 26: 11, 27: 64, 28: 14, 29: 88, 30: 84, 31: 103, 32: 90, 33: 32, 34: 117, 35: 136, 36: 31, 37: 44, 38: 132, 39: 45, 40: 42, 41: 76, 42: 104, 43: 53, 44: 72, 45: 5, 46: 15, 48: 100, 49: 27, 50: 65, 51: 35, 52: 138, 53: 125, 54: 127, 55: 99, 57: 46, 58: 75, 59: 79}
quiz_b_to_qid = {0: 146, 1: 72, 2: 25, 3: 145, 4: 79, 6: 90, 7: 118, 8: 84, 9: 24, 10: 1, 11: 58, 12: 130, 13: 148, 14: 19, 15: 117, 16: 83, 17: 21, 18: 59, 19: 127, 22: 111, 23: 50, 24: 44, 25: 17, 26: 30, 27: 56, 28: 120, 29: 141, 30: 73, 31: 38, 32: 143, 33: 6, 34: 147, 35: 8, 36: 114, 37: 93, 38: 2, 39: 11, 41: 121, 42: 68, 43: 53, 44: 37, 45: 9, 46: 77, 49: 75, 50: 106, 51: 97, 52: 102, 53: 112, 54: 41, 55: 89, 56: 29, 57: 42, 58: 133, 59: 87}

a1_to_qid = {0: 148, 1: 49, 2: 18, 3: 111, 4: 6, 5: 51, 8: 102, 10: 128, 13: 135, 14: 114, 16: 113, 18: 131, 19: 41, 20: 55, 21: 37, 22: 52, 24: 58, 26: 11, 29: 88, 32: 90, 37: 44, 41: 76, 42: 104, 46: 15, 55: 99, 57: 46, 58: 75}
a2_to_qid = {6: 93, 7: 94, 9: 21, 11: 82, 15: 146, 27: 64, 28: 14, 30: 84, 31: 103, 33: 32, 34: 117, 35: 136, 36: 31, 38: 132, 39: 45, 40: 42, 43: 53, 44: 72, 45: 5, 48: 100, 49: 27, 50: 65, 51: 35, 52: 138, 53: 125, 54: 127, 59: 79}
b1_to_qid = {3: 145, 6: 90, 9: 24, 11: 58, 12: 130, 13: 148, 16: 83, 18: 59, 22: 111, 24: 44, 25: 17, 27: 56, 29: 141, 30: 73, 33: 6, 36: 114, 39: 11, 44: 37, 45: 9, 46: 77, 49: 75, 50: 106, 52: 102, 54: 41, 55: 89, 56: 29, 58: 133}
b2_to_qid = {0: 146, 1: 72, 2: 25, 4: 79, 7: 118, 8: 84, 10: 1, 14: 19, 15: 117, 17: 21, 19: 127, 23: 50, 26: 30, 28: 120, 31: 38, 32: 143, 34: 147, 35: 8, 37: 93, 38: 2, 41: 121, 42: 68, 43: 53, 51: 97, 53: 112, 57: 42, 59: 87}

# dictionaries mapping question pool index to qid

flashcard_index_qid = {0: 15, 1: 135, 2: 55, 3: 51, 4: 56, 5: 141, 6: 128, 7: 106, 8: 111, 9: 114, 10: 59, 11: 9, 12: 131, 13: 145, 14: 18, 15: 102, 16: 11, 17: 133, 18: 130, 19: 83, 20: 41, 21: 148, 22: 75, 23: 90, 24: 99, 25: 113, 26: 104, 27: 46, 28: 37, 29: 44, 30: 49, 31: 58, 32: 24, 33: 52, 34: 73, 35: 6, 36: 29, 37: 88, 38: 17, 39: 76, 40: 77, 41: 89, 42: 144, 43: 142, 44: 92, 45: 10, 46: 3, 47: 40}
quizbot_index_qid = {0: 147, 1: 100, 2: 138, 3: 118, 4: 112, 5: 64, 6: 32, 7: 50, 8: 136, 9: 143, 10: 121, 11: 132, 12: 120, 13: 8, 14: 5, 15: 30, 16: 117, 17: 125, 18: 14, 19: 103, 20: 19, 21: 27, 22: 84, 23: 93, 24: 79, 25: 72, 26: 2, 27: 31, 28: 42, 29: 35, 30: 65, 31: 25, 32: 1, 33: 21, 34: 38, 35: 97, 36: 94, 37: 53, 38: 45, 39: 82, 40: 87, 41: 127, 42: 146, 43: 68, 44: 139, 45: 85, 46: 74, 47: 70}

# qid of flashcard and quizbot question pool
flashcard_qid = [15, 135, 55, 51, 56, 141, 128, 106, 111, 114, 59, 9, 131, 145, 18, 102, 11, 133, 130, 83, 41, 148, 75, 90, 99, 113, 104, 46, 37, 44, 49, 58, 24, 52, 73, 6, 29, 88, 17, 76, 77, 89, 144, 142, 92, 10, 3, 40]
quizbot_qid = [147, 100, 138, 118, 112, 64, 32, 50, 136, 143, 121, 132, 120, 8, 5, 30, 117, 125, 14, 103, 19, 27, 84, 93, 79, 72, 2, 31, 42, 35, 65, 25, 1, 21, 38, 97, 94, 53, 45, 82, 87, 127, 146, 68, 139, 85, 74, 70]


def get_sub_score(all_users, quiz_data, quiz_answer, quiz_sub_index):
	'''
		get the user subscores of a set of questions 
	'''

	sub_score = []

	for u in range(len(all_users)):
		user = all_users[u]
		sub_score.append(0)

		for i in quiz_sub_index:
			q_user_answer = quiz_data[user][5 * i + 4]

			if q_user_answer == quiz_answer[i]:
				sub_score[u] += 1
	return sub_score


def refine_quiz():
	'''
		pick 54 questions respectively from 60-question quiz a and quiz b so that the two 54-question quizzes are similar in difficulty
	'''

	# Qualtrics id for the original 60-question quiz a
	quiz_a_gre_index = [0, 3, 8, 10, 12, 13, 14, 15, 16, 17, 18, 31, 34, 35, 38, 42, 48, 52, 53, 54]
	quiz_a_safety_index = [5, 6, 7, 11, 20, 22, 23, 24, 27, 29, 30, 32, 41, 43, 44, 47, 50, 55, 58, 59]
	quiz_a_science_index = [1, 2, 4, 9, 19, 21, 25, 26, 28, 33, 36, 37, 39, 40, 45, 46, 49, 51, 56, 57]

	quiz_a_repeated_index = [0, 3, 4, 6, 8, 9, 14, 15, 19, 21, 24, 26, 30, 32, 34, 37, 40, 43, 44, 54, 58, 59]

	# Qualtrics id for the original 60-question quiz b
	quiz_b_gre_index = [0, 3, 7, 12, 13, 15, 19, 21, 22, 28, 29, 32, 34, 36, 40, 41, 50, 52, 53, 58]
	quiz_b_safety_index = [1, 4, 6, 8, 11, 16, 18, 23, 27, 30, 37, 42, 43, 46, 47, 48, 49, 51, 55, 59]
	quiz_b_science_index = [2, 5, 9, 10, 14, 17, 20, 24, 25, 26, 31, 33, 35, 38, 39, 44, 45, 54, 56, 57]

	quiz_b_repeated_index = [13, 22, 33, 37, 52, 17, 36, 0, 54, 44, 11, 39, 8, 6, 15, 24, 57, 43, 1, 19, 49, 4]

	quiz_a_correct_rate = []
	quiz_b_correct_rate = []

	quiz_a_answer = []
	quiz_b_answer = []

	with open(quiz_a_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_a_correct_rate.append(float(reader[i - 1][3]) / float(70))
					quiz_a_answer.append(reader[i - 1][1])
			
	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_b_correct_rate.append(float(reader[i - 1][3]) / float(70))
					quiz_b_answer.append(reader[i - 1][1])

	quiz_a_correct_rate_sorted_index = sorted(range(len(quiz_a_correct_rate)),key=quiz_a_correct_rate.__getitem__)
	quiz_b_correct_rate_sorted_index = sorted(range(len(quiz_b_correct_rate)),key=quiz_b_correct_rate.__getitem__)

	sub_questions_a = [i for i in range(60)]
	gre_a = 0
	safety_a = 0
	science_a = 0

	# remove the 2 most difficult questions from quiz a
	while len(sub_questions_a) > 58:
		index = quiz_a_correct_rate_sorted_index.pop()

		if index not in quiz_a_repeated_index:
			if index in quiz_a_gre_index:
				gre_a += 1
				quiz_a_gre_index.remove(index)
				sub_questions_a.remove(index)

			if index in quiz_a_safety_index:
				safety_a += 1
				quiz_a_safety_index.remove(index)
				sub_questions_a.remove(index)

			if index in quiz_a_science_index:
				science_a += 1
				quiz_a_science_index.remove(index)
				sub_questions_a.remove(index)

	# randomly remove 4 questions from quiz a
	# remove same number questions in each subject
	while len(sub_questions_a) > 54:
		random.shuffle(quiz_a_correct_rate_sorted_index)
		index = quiz_a_correct_rate_sorted_index.pop()

		if index not in quiz_a_repeated_index:
			if index in quiz_a_gre_index and gre_a < 2:
				gre_a += 1
				quiz_a_gre_index.remove(index)
				sub_questions_a.remove(index)

			if index in quiz_a_safety_index and safety_a < 2:
				safety_a += 1
				quiz_a_safety_index.remove(index)
				sub_questions_a.remove(index)

			if index in quiz_a_science_index and science_a < 2:
				science_a += 1
				quiz_a_science_index.remove(index)
				sub_questions_a.remove(index)
			

	sub_questions_b = [i for i in range(60)]
	removed_index_b = []
	gre_b = 0
	safety_b = 0
	science_b = 0

	# remove the 2 most difficult questions from quiz a
	while len(sub_questions_b) > 58:
		index = quiz_b_correct_rate_sorted_index.pop()

		if index not in quiz_b_repeated_index:
			if index in quiz_b_gre_index:
				gre_b += 1
				quiz_b_gre_index.remove(index)
				sub_questions_b.remove(index)

			if index in quiz_b_safety_index:
				safety_b += 1
				quiz_b_safety_index.remove(index)
				sub_questions_b.remove(index)

			if index in quiz_b_science_index:
				science_b += 1
				quiz_b_science_index.remove(index)
				sub_questions_b.remove(index)
	
	# randomly remove 4 questions from quiz a
	# remove same number questions in each subject
	while len(sub_questions_b) > 54:
		random.shuffle(quiz_b_correct_rate_sorted_index)
		index = quiz_b_correct_rate_sorted_index.pop()

		if index not in quiz_b_repeated_index:
			if index in quiz_b_gre_index and gre_b < 2:
				gre_b += 1
				quiz_b_gre_index.remove(index)
				sub_questions_b.remove(index)

			if index in quiz_b_safety_index and safety_b < 2:
				safety_b += 1
				quiz_b_safety_index.remove(index)
				sub_questions_b.remove(index)

			if index in quiz_b_science_index and science_b < 2:
				science_b += 1
				quiz_b_science_index.remove(index)
				sub_questions_b.remove(index)

	quiz_a_data = {}
	quiz_b_data = {}

	with open(quiz_a_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz_a = reader[3:]

	with open(quiz_b_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz_b = reader[3:]

	# create a quiz record entry for each user
	for i in range(len(quiz_a)):
		quiz_a_data[quiz_a[i][17]] = quiz_a[i][22:-1]

	for i in range(len(quiz_b)):
		quiz_b_data[quiz_b[i][17]] = quiz_b[i][22:-1]

	# id for all users
	all_users_temp = quiz_a_data.keys()
	all_users_temp.extend(x for x in quiz_b_data.keys() if x not in quiz_a_data.keys())
	all_user = []

	# filter out the users who have done both quiz a and quiz b
	for user in all_users_temp:
		if user in quiz_a_data.keys() and user in quiz_b_data.keys():
			all_user.append(user)

	# print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, sub_questions_a))
	# print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, sub_questions_b))

	# print(numpy.mean(get_sub_score(all_user, quiz_a_data, quiz_a_answer, sub_questions_a)))
	# print(numpy.mean(get_sub_score(all_user, quiz_b_data, quiz_b_answer, sub_questions_b)))

	# print(quiz_a_gre_index)
	# print(quiz_a_safety_index)
	# print(quiz_a_science_index)
	# print(quiz_b_gre_index)
	# print(quiz_b_safety_index)
	# print(quiz_b_science_index)

	# print(len(quiz_a_gre_index))
	# print(len(quiz_a_safety_index))
	# print(len(quiz_a_science_index))
	# print(len(quiz_b_gre_index))
	# print(len(quiz_b_safety_index))
	# print(len(quiz_b_science_index))

	# the refined quizzes with 54 questions each
	quiz_a = list(quiz_a_gre_index + quiz_a_safety_index + quiz_a_science_index)
	quiz_b = list(quiz_b_gre_index + quiz_b_safety_index + quiz_b_science_index)

	quiz_a.sort()
	quiz_b.sort()

	a_all = [i for i in range(60)]
	quiz_a_remove = list(set(a_all) - set(quiz_a))
	b_all = [i for i in range(60)]
	quiz_b_remove = list(set(b_all) - set(quiz_b))

	# print(quiz_a)
	# print(quiz_b)
	# print(quiz_a_remove)
	# print(quiz_b_remove)

	return quiz_a_gre_index, quiz_a_safety_index, quiz_a_science_index, quiz_a, quiz_a_remove, \
		   quiz_b_gre_index, quiz_b_safety_index, quiz_b_science_index, quiz_b, quiz_b_remove


def split_refined_quiz():
	'''
		split 54-question quiz a and quiz b to four quizzes a1, a2, b1, b2
		a1, a2, b1, b2 are similar in difficulty and each have 27 questions
		a1 and b1, a2 and b2 each contain the same set of repeated questions
		a = a1 + a2
		b = b1 + b2
	'''
	quiz_a_correct_rate = []
	quiz_b_correct_rate = []

	quiz_a_answer = []
	quiz_b_answer = []

	with open(quiz_a_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_a_correct_rate.append(float(reader[i - 1][3]) / float(70))
					quiz_a_answer.append(reader[i - 1][1])
			
	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_b_correct_rate.append(float(reader[i - 1][3]) / float(70))
					quiz_b_answer.append(reader[i - 1][1])

	# get all the index combinations when choosing 9 questions from 18 questions for each subject
	quiz_a_gre_index_combo = list(itertools.combinations(quiz_a_gre_index, 9))
	quiz_a_safety_index_combo = list(itertools.combinations(quiz_a_safety_index, 9))
	quiz_a_science_index_combo = list(itertools.combinations(quiz_a_science_index, 9))

	average_a_half_1 = 10
	average_a_half_2 = 20

	average_b_half_1 = 30
	average_b_half_2 = 40

	# try out different partitions (a1, a2, b1, b2) until we find one partition with four quizzes similar in difficulty
	while abs(average_a_half_1 - average_b_half_1) > 0.34 or \
		  abs(average_a_half_2 - average_b_half_2) > 0.34:

		# pick random combinations for each subject
		i = random.randint(0, 48619)
		j = random.randint(0, 48619)
		k = random.randint(0, 48619)

		all_index = [i for i in range(60)]
		quiz_a_half_1_index = list(quiz_a_gre_index_combo[i] + quiz_a_safety_index_combo[j] + quiz_a_science_index_combo[k])
		quiz_a_half_2_index = list(set(all_index) - set(quiz_a_half_1_index) - set(quiz_a_remove))

		quiz_a_half_1 = [quiz_a_correct_rate[s] for s in quiz_a_half_1_index]
		quiz_a_half_2 = [quiz_a_correct_rate[s] for s in quiz_a_half_2_index]

		quiz_b_gre_half_1 = []
		quiz_b_safety_half_1 = []
		quiz_b_science_half_1 = []

		# add repeated questions in a1 to b1, add repeated questions in a2 to b2
		# a1 and b2, a2 and b1 are mutually exclusive
		for p in range(9):
			if quiz_a_gre_index_combo[i][p] in quiz_a_repeated_index:
				repeat_index = quiz_a_repeated_index.index(quiz_a_gre_index_combo[i][p])
				quiz_b_gre_half_1.append(quiz_b_repeated_index[repeat_index])

			if quiz_a_safety_index_combo[j][p] in quiz_a_repeated_index:
				repeat_index = quiz_a_repeated_index.index(quiz_a_safety_index_combo[j][p])
				quiz_b_safety_half_1.append(quiz_b_repeated_index[repeat_index])

			if quiz_a_science_index_combo[k][p] in quiz_a_repeated_index:
				repeat_index = quiz_a_repeated_index.index(quiz_a_science_index_combo[k][p])
				quiz_b_science_half_1.append(quiz_b_repeated_index[repeat_index])

		quiz_b_gre_half_2 = list(set(quiz_b_gre_index[:]) - set(quiz_b_repeated_index))
		quiz_b_safety_half_2 = list(set(quiz_b_safety_index[:]) - set(quiz_b_repeated_index)) 
		quiz_b_science_half_2 = list(set(quiz_b_science_index[:]) - set(quiz_b_repeated_index)) 

		random.shuffle(quiz_b_gre_half_2)
		random.shuffle(quiz_b_safety_half_2)
		random.shuffle(quiz_b_science_half_2)

		# add non-repeated questions to make a1, a2, b1, b2 each have 9 questions in gre. safety, and science
		num_append = 9 - len(quiz_b_gre_half_1)
		for i in range(num_append):
			quiz_b_gre_half_1.append(quiz_b_gre_half_2[i])

		num_append = 9 - len(quiz_b_safety_half_1)
		for i in range(num_append):
			quiz_b_safety_half_1.append(quiz_b_safety_half_2[i])

		num_append = 9 - len(quiz_b_science_half_1)
		for i in range(num_append):
			quiz_b_science_half_1.append(quiz_b_science_half_2[i])

		all_index = [i for i in range(60)]
		quiz_b_half_1_index = quiz_b_gre_half_1 + quiz_b_safety_half_1 + quiz_b_science_half_1
		quiz_b_half_2_index = list(set(all_index) - set(quiz_b_half_1_index) - set(quiz_b_remove))

		quiz_b_half_1 = [quiz_b_correct_rate[s] for s in quiz_b_half_1_index]
		quiz_b_half_2 = [quiz_b_correct_rate[s] for s in quiz_b_half_2_index]

		average_a_half_1 = sum(quiz_a_half_1) 
		average_a_half_2 = sum(quiz_a_half_2)

		average_b_half_1 = sum(quiz_b_half_1)
		average_b_half_2 = sum(quiz_b_half_2)

		print("-------------------------------------")
		quiz_a_half_1_index.sort()
		quiz_a_half_2_index.sort()
		quiz_b_half_1_index.sort()
		quiz_b_half_2_index.sort()

		print(quiz_a_half_1_index)
		print(quiz_a_half_2_index)
		print(quiz_b_half_1_index)
		print(quiz_b_half_2_index)

		# # print("a1 - a2: " + str(average_a_half_1 - average_a_half_2))
		print("a1 - b1: " + str(average_a_half_1 - average_b_half_1))
		# # print("a1 - b2: " + str(average_a_half_1 - average_b_half_2))
		# # print("a2 - b1: " + str(average_a_half_2 - average_b_half_1))
		print("a2 - b2: " + str(average_a_half_2 - average_b_half_2))
		# # print("b1 - b2: " + str(average_b_half_1 - average_b_half_2))

	quiz_a_data = {}
	quiz_b_data = {}

	# get MTurk user's subscores for a1, a2, b1, b2
	with open(quiz_a_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz_a = reader[3:]

	with open(quiz_b_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz_b = reader[3:]

	for i in range(len(quiz_a)):
		quiz_a_data[quiz_a[i][17]] = quiz_a[i][22:-1]

	for i in range(len(quiz_b)):
		quiz_b_data[quiz_b[i][17]] = quiz_b[i][22:-1]

	# MTurk id for all users
	all_users_temp = quiz_a_data.keys()
	all_users_temp.extend(x for x in quiz_b_data.keys() if x not in quiz_a_data.keys())
	all_user = []

	# filter out the users who have done both Quiz A and Quiz B
	for user in all_users_temp:
		if user in quiz_a_data.keys() and user in quiz_b_data.keys():
			all_user.append(user)

	# print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_half_1_index))
	# print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_half_2_index))
	# print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_half_1_index))
	# print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_half_2_index))

	print(numpy.mean(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_half_1_index)))
	print(numpy.mean(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_half_2_index)))
	print(numpy.mean(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_half_1_index)))
	print(numpy.mean(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_half_2_index)))

	# print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, a1))
	# print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, a2))
	# print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, b1))
	# print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, b2))

	# print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_index))
	# print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_index))


def get_repeated_questions():
	'''
		get the qualtrics index of the repeated questions in quiz a and quiz b
	'''
	quiz_a_repeated_index = []
	quiz_b_repeated_index = []

	quiz_a_question = []
	quiz_b_question = []

	with open(quiz_a_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Field":
					quiz_a_question.append(reader[i - 1][0])
			
	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Field":
					quiz_b_question.append(reader[i - 1][0])

	# remove the prefix tags for each question
	for i in range(60):
		if i < 11:
			quiz_a_question[i] = quiz_a_question[i][5:]
		else:
			quiz_a_question[i] = quiz_a_question[i][6:]
		while quiz_a_question[i][0] == " ":
			quiz_a_question[i] = quiz_a_question[i][1:]
		while quiz_a_question[i][-1] == " ":
			quiz_a_question[i] = quiz_a_question[i][:-1]

	for i in range(60):
		if i < 11:
			quiz_b_question[i] = quiz_b_question[i][5:]
		else:
			quiz_b_question[i] = quiz_b_question[i][6:]
		while quiz_b_question[i][0] == " ":
			quiz_b_question[i] = quiz_b_question[i][1:]
		while quiz_b_question[i][-1] == " ":
			quiz_b_question[i] = quiz_b_question[i][:-1]

	quiz_a_question = quiz_a_question[:-1]
	quiz_b_question = quiz_b_question[:-1]

	# get the Qualtrics id for the repeated questions in quiz a and quiz b
	for q in quiz_a_question:
		if q in quiz_b_question:
			quiz_a_repeated_index.append(quiz_a_question.index(q))
			quiz_b_repeated_index.append(quiz_b_question.index(q))

	print(quiz_a_repeated_index)
	print(quiz_b_repeated_index)

	# confirm if the corresponding questions are the same
	for i in range(22):
		print(quiz_a_question[quiz_a_repeated_index[i]])
		print(quiz_b_question[quiz_b_repeated_index[i]])


def verify():
	'''
		confirm the questions partition is correct
	'''

	quiz_a_all = set(quiz_a_remove + quiz_a_index)
	quiz_b_all = set(quiz_b_remove + quiz_b_index)

	all_60 = [i for i in range(60)]

	print(quiz_a_all == set(all_60))
	print(quiz_b_all == set(all_60))

	print(quiz_a_index)
	print(quiz_b_index)

	a1_a2 = set(a1 + a2)
	b1_b2 = set(b1 + b2)

	print(a1_a2 == set(quiz_a_index))
	print(b1_b2 == set(quiz_b_index))

	a1_repeated = []
	a2_repeated = []
	b1_repeated = []
	b2_repeated = []

	for q in a1:
		if q in quiz_a_repeated_index:
			a1_repeated.append(q)

	for q in b1:
		if q in quiz_b_repeated_index:
			b1_repeated.append(q)

	for q in a2:
		if q in quiz_a_repeated_index:
			a2_repeated.append(q)

	for q in b2:
		if q in quiz_b_repeated_index:
			b2_repeated.append(q)

	print(a1_repeated)
	print(b1_repeated)
	print(len(a1_repeated))
	print(len(b1_repeated))
	print(a2_repeated)
	print(b2_repeated)
	print(len(a2_repeated))
	print(len(b2_repeated))

	b1_repeated_copy = b1_repeated[:]
	b2_repeated_copy = b2_repeated[:]

	print(b1_repeated_copy)
	print(b2_repeated_copy)

	for i in a1_repeated:
		index = a1_repeated.index(i)
		el = b1_repeated[index]
		b1_repeated_copy.remove(el)

	for i in a2_repeated:
		index = a2_repeated.index(i)
		el = b2_repeated[index]
		b2_repeated_copy.remove(el)

	print(b1_repeated_copy)
	print(b2_repeated_copy)

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

	quiz_a_data = {}
	quiz_b_data = {}

	with open(quiz_a_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz_a = reader[3:]

	with open(quiz_b_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz_b = reader[3:]

	for i in range(len(quiz_a)):
		quiz_a_data[quiz_a[i][17]] = quiz_a[i][22:-1]

	for i in range(len(quiz_b)):
		quiz_b_data[quiz_b[i][17]] = quiz_b[i][22:-1]

	all_users_temp = quiz_a_data.keys()
	all_users_temp.extend(x for x in quiz_b_data.keys() if x not in quiz_a_data.keys())
	all_user = []

	for user in all_users_temp:
		if user in quiz_a_data.keys() and user in quiz_b_data.keys():
			all_user.append(user)

	print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_index))
	print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_index))


def split_question_pool():
	'''
		spliting the question pool for quizbot and flashcard
		each contains 16 questions in gre, safety, science
		these two question pools are mutually exclusive
	'''
	quiz_a_question = []
	quiz_b_question = []

	with open(quiz_a_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Field":
					quiz_a_question.append(reader[i - 1][0])
			
	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Field":
					quiz_b_question.append(reader[i - 1][0])

	for i in range(60):
		if i < 11:
			quiz_a_question[i] = quiz_a_question[i][5:]
		else:
			quiz_a_question[i] = quiz_a_question[i][6:]
		while quiz_a_question[i][0] == " ":
			quiz_a_question[i] = quiz_a_question[i][1:]
		while quiz_a_question[i][-1] == " ":
			quiz_a_question[i] = quiz_a_question[i][:-1]

	for i in range(60):
		if i < 11:
			quiz_b_question[i] = quiz_b_question[i][5:]
		else:
			quiz_b_question[i] = quiz_b_question[i][6:]
		while quiz_b_question[i][0] == " ":
			quiz_b_question[i] = quiz_b_question[i][1:]
		while quiz_b_question[i][-1] == " ":
			quiz_b_question[i] = quiz_b_question[i][:-1]

	quiz_a_question_temp = quiz_a_question[:-1]
	quiz_b_question_temp = quiz_b_question[:-1]

	quiz_a_question = [quiz_a_question_temp[i] for i in quiz_a_index]
	quiz_b_question = [quiz_b_question_temp[i] for i in quiz_b_index]

	# get the question text
	a1_question = [quiz_a_question_temp[i] for i in a1]
	a2_question = [quiz_a_question_temp[i] for i in a2]
	b1_question = [quiz_b_question_temp[i] for i in b1]
	b2_question = [quiz_b_question_temp[i] for i in b2]

	# remove the repeated indices
	flashcard_question = numpy.unique(a1_question + b1_question)
	quizbot_question = numpy.unique(a2_question + b2_question)

	flashcard_gre = []
	flashcard_safety = []
	flashcard_science = []
	quizbot_gre = []
	quizbot_safety = []
	quizbot_science = []

	# get the question text in each subject
	for i in a1:
		if i in quiz_a_gre_index:	
			flashcard_gre.append(quiz_a_question_temp[i])
		if i in quiz_a_safety_index:
			flashcard_safety.append(quiz_a_question_temp[i])
		if i in quiz_a_science_index:
			flashcard_science.append(quiz_a_question_temp[i])

	for i in b1:
		if i in quiz_b_gre_index:
			flashcard_gre.append(quiz_b_question_temp[i])
		if i in quiz_b_safety_index:
			flashcard_safety.append(quiz_b_question_temp[i])
		if i in quiz_b_science_index:
			flashcard_science.append(quiz_b_question_temp[i])

	for i in a2:
		if i in quiz_a_gre_index:
			quizbot_gre.append(quiz_a_question_temp[i])
		if i in quiz_a_safety_index:
			quizbot_safety.append(quiz_a_question_temp[i])
		if i in quiz_a_science_index:
			quizbot_science.append(quiz_a_question_temp[i])

	for i in b2:
		if i in quiz_b_gre_index:
			quizbot_gre.append(quiz_b_question_temp[i])
		if i in quiz_b_safety_index:
			quizbot_safety.append(quiz_b_question_temp[i])
		if i in quiz_b_science_index:
			quizbot_science.append(quiz_b_question_temp[i])

	# print(flashcard_gre)
	# print(flashcard_safety)
	# print(flashcard_science)
	# print(quizbot_gre)
	# print(quizbot_safety)
	# print(quizbot_science)

	# flashcard_gre = set(flashcard_gre)
	# flashcard_safety = set(flashcard_safety)
	# flashcard_science = set(flashcard_science)
	# quizbot_gre = set(quizbot_gre)
	# quizbot_safety = set(quizbot_safety)
	# quizbot_science = set(quizbot_science)

	flashcard_gre = list(set(flashcard_gre))
	flashcard_safety = list(set(flashcard_safety))
	flashcard_science = list(set(flashcard_science))
	quizbot_gre = list(set(quizbot_gre))
	quizbot_safety = list(set(quizbot_safety))
	quizbot_science = list(set(quizbot_science))

	# flashcard_question_combine = flashcard_gre + flashcard_safety + flashcard_science
	# quizbot_question_combine = quizbot_gre + quizbot_safety + quizbot_science

	# print(set(flashcard_question_combine) == set(flashcard_question))
	# print(set(quizbot_question_combine) == set(quizbot_question))

	# print(len(flashcard_gre))
	# print(len(flashcard_safety))
	# print(len(flashcard_science))
	# print(len(quizbot_gre))
	# print(len(quizbot_safety))
	# print(len(quizbot_science))

	flashcard_question_json = []
	quizbot_question_json = []

	# print(len(flashcard_question))
	# print(len(quizbot_question))

	# print(flashcard_question)
	# print(quizbot_question)

	quiz_all_filename = "json/questions_filtered_150_quizbot.json"
	all_questions = {}

	with open(quiz_all_filename) as data_file:
	    data = json.load(data_file)

	for i in range(150):
		all_questions[str(data[i]['question'])] = data[i]

	for q in flashcard_question:
		flashcard_question_json.append(all_questions[q])
		
	for q in quizbot_question:
		quizbot_question_json.append(all_questions[q])

	# print(len(flashcard_question_json))
	# print(len(quizbot_question_json))

	# print(flashcard_question_json)
	# print(quizbot_question_json)

	# with open(between_subjects_flashcard_filename, 'w') as outfile:
	# 	json.dump(flashcard_question_json, outfile, indent=4, sort_keys=True)

	# with open(between_subjects_quizbot_filename, 'w') as outfile:
	# 	json.dump(quizbot_question_json, outfile, indent=4, sort_keys=True)


def verify_question_pool():
	'''
		verify the question pool
	'''

	with open(between_subjects_flashcard_filename) as data_file:
	    flashcard_data = json.load(data_file)

	with open(between_subjects_quizbot_filename) as data_file:
	    quizbot_data = json.load(data_file)

	print(len(flashcard_data))
	print(len(quizbot_data))


def dump_correct_rate():
	'''
		dump the question rate to a csv file
	'''
	quiz_a_correct_rate = []
	quiz_b_correct_rate = []
	quiz_a_question = []
	quiz_b_question = []

	with open(quiz_a_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_a_correct_rate.append(float(reader[i - 1][3]) / float(70))
				if reader[i][1] == "Field":
					quiz_a_question.append(reader[i - 1][0])
			
	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_b_correct_rate.append(float(reader[i - 1][3]) / float(70))
				if reader[i][1] == "Field":
					quiz_b_question.append(reader[i - 1][0])

	for i in range(60):
		if i < 11:
			quiz_a_question[i] = quiz_a_question[i][5:]
		else:
			quiz_a_question[i] = quiz_a_question[i][6:]
		while quiz_a_question[i][0] == " ":
			quiz_a_question[i] = quiz_a_question[i][1:]
		while quiz_a_question[i][-1] == " ":
			quiz_a_question[i] = quiz_a_question[i][:-1]

	for i in range(60):
		if i < 11:
			quiz_b_question[i] = quiz_b_question[i][5:]
		else:
			quiz_b_question[i] = quiz_b_question[i][6:]
		while quiz_b_question[i][0] == " ":
			quiz_b_question[i] = quiz_b_question[i][1:]
		while quiz_b_question[i][-1] == " ":
			quiz_b_question[i] = quiz_b_question[i][:-1]

	quiz_a_question = quiz_a_question[:-1]
	quiz_b_question = quiz_b_question[:-1]

	question_correct_rate_pair = {}

	for i in range(60):
		question_correct_rate_pair[quiz_a_question[i]] = quiz_a_correct_rate[i]

	for i in range(60):
		q = quiz_b_question[i]
		if q not in question_correct_rate_pair.keys():
			question_correct_rate_pair[q] = quiz_b_correct_rate[i]

	quiz_all_filename = "json/questions_filtered_150_quizbot.json"
	all_questions = {}

	result = []

	with open(quiz_all_filename) as data_file:
	    data = json.load(data_file)

	for i in range(150):
		all_questions[str(data[i]['question'])] = data[i]

	for q in question_correct_rate_pair.keys():
		sub_result = []
		if q == "Arrange in the correct order the following treatment steps for somebody who has lost consciousness: (i) call 911 or inform someone of the situation, (ii) begin CPR, (iii) check the patient's airway to make sure it is clear, (iv) place the victim on his/her back, (v) check signs of life (coughing, breathing, or movement).":
			sub_result.append(55)
		else:
			sub_result.append(all_questions[q]["id"])
		sub_result.append(q)
		sub_result.append(question_correct_rate_pair[q])

		result.append(sub_result)

	result.insert(0, ["id", "question", "correct_rate"])

	with open("csv/question_correct_rate.csv", 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerows(result)


def get_quiz_qid():
	'''
		get the qid for questions in quizzes
	'''
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"
	quiz_b_question = []

	with open(quiz_b_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		counter = 0
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Field":
					quiz_b_question.append(reader[i - 1][0])
					counter += 1

	# quiz_b_index = quiz_b_index
	quiz_b_question_temp = [quiz_b_question[i] for i in quiz_b_index]
	quiz_b_question = quiz_b_question_temp[:]

	for i in range(len(quiz_b_question)):
		quiz_b_question[i] = quiz_b_question[i][5:]
		while quiz_b_question[i][0] == " ":
			quiz_b_question[i] = quiz_b_question[i][1:]
		while quiz_b_question[i][-1] == " ":
			quiz_b_question[i] = quiz_b_question[i][:-1]

	quiz_all_filename = "json/questions_filtered_150_quizbot.json"
	all_questions = {}

	result = {}

	with open(quiz_all_filename) as data_file:
	    data = json.load(data_file)

	for i in range(150):
		all_questions[str(data[i]['question'])] = data[i]

	for i in range(len(quiz_b_question)):
		q = quiz_b_question[i]
		if q == "Arrange in the correct order the following treatment steps for somebody who has lost consciousness: (i) call 911 or inform someone of the situation, (ii) begin CPR, (iii) check the patient's airway to make sure it is clear, (iv) place the victim on his/her back, (v) check signs of life (coughing, breathing, or movement).":
			result[quiz_b_index[i]] = 55
		else:
			result[quiz_b_index[i]] = all_questions[q]["id"]

	result = []

	with open(quiz_all_filename) as data_file:
	    data = json.load(data_file)

	for i in range(150):
		all_questions[str(data[i]['question'])] = data[i]

	for i in range(len(quiz_b_question)):
		q = quiz_b_question[i]
		if q == "Arrange in the correct order the following treatment steps for somebody who has lost consciousness: (i) call 911 or inform someone of the situation, (ii) begin CPR, (iii) check the patient's airway to make sure it is clear, (iv) place the victim on his/her back, (v) check signs of life (coughing, breathing, or movement).":
			result.append(55)
		else:
			result.append(all_questions[q]["id"])

	print(result)
	print(len(result))


def get_question_pool_qid():
	a1_question_qid = a1_to_qid.values()
	a2_question_qid = a2_to_qid.values()
	b1_question_qid = b1_to_qid.values()
	b2_question_qid = b2_to_qid.values()

	flashcard_question_qid = numpy.unique(a1_question_qid + b1_question_qid)
	quizbot_question_qid = numpy.unique(a2_question_qid + b2_question_qid)

	print(list(flashcard_question_qid))
	print(len(flashcard_question_qid))
	print(list(quizbot_question_qid))
	print(len(quizbot_question_qid))


def get_repeated_in_pool():
	repeated_in_flashcard = list(set(repeated_question_qid)&set(flashcard_qid))
	repeated_in_quizbot = list(set(repeated_question_qid)&set(quizbot_qid))

	print(repeated_in_flashcard)
	print(len(repeated_in_flashcard))
	print(repeated_in_quizbot)
	print(len(repeated_in_quizbot))


def map_question_pool_index_qid():

	with open(between_subjects_flashcard_filename, 'r') as flashcard_question_json:
		flashcard_data = json.load(flashcard_question_json)

	with open(between_subjects_quizbot_filename, 'r') as quizbot_question_json:
		quizbot_data = json.load(quizbot_question_json)

	flashcard_question_pool_index_to_qid = {}
	quizbot_question_pool_index_to_qid = {}

	flashcard_question_pool_id = []
	quizbot_question_pool_id = []


	for i in range(len(flashcard_data)):
		flashcard_question_pool_index_to_qid[flashcard_data[i]["id"]] = i
		flashcard_question_pool_id.append(flashcard_data[i]["id"])

	for i in range(len(quizbot_data)):
		quizbot_question_pool_index_to_qid[quizbot_data[i]["id"]] = i
		quizbot_question_pool_id.append(quizbot_data[i]["id"])

	print(flashcard_question_pool_index_to_qid)
	print(quizbot_question_pool_index_to_qid)

	print(flashcard_question_pool_id)
	print(quizbot_question_pool_id)

if __name__ == "__main__":
	map_question_pool_index_qid()
