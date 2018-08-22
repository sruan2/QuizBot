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

quiz_a_repeated_index = [0,  3,   4,  6,  8,  9, 14, 15, 19, 21, 24, 26, 30, 32, 34, 37, 40, 43, 44, 54, 58, 59]
quiz_b_repeated_index = [13, 22, 33, 37, 52, 17, 36,  0, 54, 44, 11, 39,  8,  6, 15, 24, 57, 43,  1, 19, 49,  4]

quiz_a_to_id = {0: 148, 1: 49, 2: 18, 3: 111, 4: 6, 5: 51, 6: 93, 7: 94, 8: 102, 9: 21, 10: 128, 11: 82, 13: 135, 14: 114, 15: 146, 16: 113, 18: 131, 19: 41, 20: 55, 21: 37, 22: 52, 24: 58, 26: 11, 27: 64, 28: 14, 29: 88, 30: 84, 31: 103, 32: 90, 33: 32, 34: 117, 35: 136, 36: 31, 37: 44, 38: 132, 39: 45, 40: 42, 41: 76, 42: 104, 43: 53, 44: 72, 45: 5, 46: 15, 48: 100, 49: 27, 50: 65, 51: 35, 52: 138, 53: 125, 54: 127, 55: 99, 57: 46, 58: 75, 59: 79}
quiz_b_to_id = {0: 146, 1: 72, 2: 25, 3: 145, 4: 79, 6: 90, 7: 118, 8: 84, 9: 24, 10: 1, 11: 58, 12: 130, 13: 148, 14: 19, 15: 117, 16: 83, 17: 21, 18: 59, 19: 127, 22: 111, 23: 50, 24: 44, 25: 17, 26: 30, 27: 56, 28: 120, 29: 141, 30: 73, 31: 38, 32: 143, 33: 6, 34: 147, 35: 8, 36: 114, 37: 93, 38: 2, 39: 11, 41: 121, 42: 68, 43: 53, 44: 37, 45: 9, 46: 77, 49: 75, 50: 106, 51: 97, 52: 102, 53: 112, 54: 41, 55: 89, 56: 29, 57: 42, 58: 133, 59: 87}

def get_sub_score(all_users, quiz_data, quiz_answer, quiz_sub_index):
	result_data = []

	for u in range(len(all_users)):
		user = all_users[u]
		result_data.append(0)

		for i in quiz_sub_index:
			q_user_answer = quiz_data[user][5 * i + 4]

			if q_user_answer == quiz_answer[i]:
				result_data[u] += 1
	return result_data


def refine_quiz():
	quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

	quiz_a_gre_index = [0, 3, 8, 10, 12, 13, 14, 15, 16, 17, 18, 31, 34, 35, 38, 42, 48, 52, 53, 54]
	quiz_a_safety_index = [5, 6, 7, 11, 20, 22, 23, 24, 27, 29, 30, 32, 41, 43, 44, 47, 50, 55, 58, 59]
	quiz_a_science_index = [1, 2, 4, 9, 19, 21, 25, 26, 28, 33, 36, 37, 39, 40, 45, 46, 49, 51, 56, 57]

	quiz_b_gre_index = [0, 3, 7, 12, 13, 15, 19, 21, 22, 28, 29, 32, 34, 36, 40, 41, 50, 52, 53, 58]
	quiz_b_safety_index = [1, 4, 6, 8, 11, 16, 18, 23, 27, 30, 37, 42, 43, 46, 47, 48, 49, 51, 55, 59]
	quiz_b_science_index = [2, 5, 9, 10, 14, 17, 20, 24, 25, 26, 31, 33, 35, 38, 39, 44, 45, 54, 56, 57]

	quiz_a_repeated_index = [0, 3, 4, 6, 8, 9, 14, 15, 19, 21, 24, 26, 30, 32, 34, 37, 40, 43, 44, 54, 58, 59]
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

	quiz_a_user_record_filename = "csv/MTurk1_A_user_record.csv"
	quiz_b_user_record_filename = "csv/MTurk1_B_user_record.csv"

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

	print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, sub_questions_a))
	print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, sub_questions_b))

	print(numpy.mean(get_sub_score(all_user, quiz_a_data, quiz_a_answer, sub_questions_a)))
	print(numpy.mean(get_sub_score(all_user, quiz_b_data, quiz_b_answer, sub_questions_b)))

	print(quiz_a_gre_index)
	print(quiz_a_safety_index)
	print(quiz_a_science_index)
	print(quiz_b_gre_index)
	print(quiz_b_safety_index)
	print(quiz_b_science_index)

	print(len(quiz_a_gre_index))
	print(len(quiz_a_safety_index))
	print(len(quiz_a_science_index))
	print(len(quiz_b_gre_index))
	print(len(quiz_b_safety_index))
	print(len(quiz_b_science_index))

	quiz_a = list(quiz_a_gre_index + quiz_a_safety_index + quiz_a_science_index)
	quiz_b = list(quiz_b_gre_index + quiz_b_safety_index + quiz_b_science_index)

	a_all = [i for i in range(60)]
	quiz_a_remove = list(set(a_all) - set(quiz_a))
	b_all = [i for i in range(60)]
	quiz_b_remove = list(set(b_all) - set(quiz_b))

	quiz_a.sort()
	quiz_b.sort()

	print(quiz_a)
	print(quiz_b)
	print(quiz_a_remove)
	print(quiz_b_remove)

	return quiz_a_gre_index, quiz_a_safety_index, quiz_a_science_index, quiz_a, quiz_a_remove, \
		   quiz_b_gre_index, quiz_b_safety_index, quiz_b_science_index, quiz_b, quiz_b_remove


def split_refined_quiz():
	quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

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

	quiz_a_gre_index_combo = list(itertools.combinations(quiz_a_gre_index, 9))
	quiz_a_safety_index_combo = list(itertools.combinations(quiz_a_safety_index, 9))
	quiz_a_science_index_combo = list(itertools.combinations(quiz_a_science_index, 9))

	average_a_half_1 = 10
	average_a_half_2 = 20

	average_b_half_1 = 30
	average_b_half_2 = 40

	while abs(average_a_half_1 - average_b_half_1) > 0.34 or \
		  abs(average_a_half_2 - average_b_half_2) > 0.34:

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

	quiz_a_user_record_filename = "csv/MTurk1_A_user_record.csv"
	quiz_b_user_record_filename = "csv/MTurk1_B_user_record.csv"

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

	print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_half_1_index))
	print(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_half_2_index))
	print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_half_1_index))
	print(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_half_2_index))

	print(numpy.mean(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_half_1_index)))
	print(numpy.mean(get_sub_score(all_user, quiz_a_data, quiz_a_answer, quiz_a_half_2_index)))
	print(numpy.mean(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_half_1_index)))
	print(numpy.mean(get_sub_score(all_user, quiz_b_data, quiz_b_answer, quiz_b_half_2_index)))


def get_repeated_questions():
	quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

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

	# for i in range(len(quiz_a_question)):
	# 	print(quiz_a_question[i])
	# for i in range(len(quiz_b_question)):
	# 	print(quiz_b_question[i])

	for q in quiz_a_question:
		if q in quiz_b_question:
			quiz_a_repeated_index.append(quiz_a_question.index(q))
			quiz_b_repeated_index.append(quiz_b_question.index(q))

	print(quiz_a_repeated_index)
	print(quiz_b_repeated_index)
	# print(len(quiz_a_repeated_index))
	# print(len(quiz_b_repeated_index))

	# for i in range(22):
	# 	print(quiz_a_question[quiz_a_repeated_index[i]])
	# 	print(quiz_b_question[quiz_b_repeated_index[i]])


def verify():
	quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

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

	quiz_a_user_record_filename = "csv/MTurk1_A_user_record.csv"
	quiz_b_user_record_filename = "csv/MTurk1_B_user_record.csv"

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
	quiz_between_subjects_flashcard_filename = "json/questions_between_subjects_flashcard.json"
	quiz_between_subjects_quizbot_filename = "json/questions_between_subjects_quizbot.json"
	quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

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

	a1_question = [quiz_a_question_temp[i] for i in a1]
	a2_question = [quiz_a_question_temp[i] for i in a2]
	b1_question = [quiz_b_question_temp[i] for i in b1]
	b2_question = [quiz_b_question_temp[i] for i in b2]

	flashcard_question = numpy.unique(a1_question + b1_question)
	quizbot_question = numpy.unique(a2_question + b2_question)

	# print(flashcard_question)
	# print(quizbot_question)

	flashcard_gre = []
	flashcard_safety = []
	flashcard_science = []
	quizbot_gre = []
	quizbot_safety = []
	quizbot_science = []

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

	# with open(quiz_between_subjects_flashcard_filename, 'w') as outfile:
	# 	json.dump(flashcard_question_json, outfile, indent=4, sort_keys=True)

	# with open(quiz_between_subjects_quizbot_filename, 'w') as outfile:
	# 	json.dump(quizbot_question_json, outfile, indent=4, sort_keys=True)


def verify_question_pool():
	quiz_between_subjects_flashcard_filename = "json/questions_between_subjects_flashcard.json"
	quiz_between_subjects_quizbot_filename = "json/questions_between_subjects_quizbot.json"	

	with open(quiz_between_subjects_flashcard_filename) as data_file:
	    flashcard_data = json.load(data_file)

	with open(quiz_between_subjects_quizbot_filename) as data_file:
	    quizbot_data = json.load(data_file)

	print(len(flashcard_data))
	print(len(quizbot_data))


def dump_correct_rate():
	quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

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
			sub_result.append(35)
		else:
			sub_result.append(all_questions[q]["id"])
		sub_result.append(q)
		sub_result.append(question_correct_rate_pair[q])

		result.append(sub_result)

	result.insert(0, ["id", "question", "correct_rate"])

	with open("csv/question_correct_rate.csv", 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerows(result)


def get_quiz_id():
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

	# quiz_b_index = quiz_a_index
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
			result[quiz_b_index[i]] = 35
		else:
			result[quiz_b_index[i]] = all_questions[q]["id"]

	print(result)
	print(len(result))


if __name__ == "__main__":
	get_quiz_id()

