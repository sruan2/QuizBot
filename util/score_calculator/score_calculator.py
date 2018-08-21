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

def dump_correct_rate():
	quiz_a_score_report_filename = "csv/MTurk1_A_score_report.csv"
	quiz_b_score_report_filename = "csv/MTurk1_B_score_report.csv"

	quiz_a_gre_index = [0, 3, 8, 10, 13, 14, 15, 16, 18, 31, 34, 35, 38, 42, 48, 52, 53, 54]
	quiz_a_safety_index = [5, 6, 7, 11, 20, 22, 24, 27, 29, 30, 32, 41, 43, 44, 50, 55, 58, 59]
	quiz_a_science_index = [1, 2, 4, 9, 19, 21, 26, 28, 33, 36, 37, 39, 40, 45, 46, 49, 51, 57]
	quiz_a_remove = [12, 47, 17, 23, 56, 25]
	quiz_a_index = list(quiz_a_gre_index + quiz_a_safety_index + quiz_a_science_index)

	quiz_b_gre_index = [0, 3, 7, 12, 13, 15, 19, 22, 28, 29, 32, 34, 36, 41, 50, 52, 53, 58]
	quiz_b_safety_index = [1, 4, 6, 8, 11, 16, 18, 23, 27, 30, 37, 42, 43, 46, 49, 51, 55, 59]
	quiz_b_science_index = [2, 9, 10, 14, 17, 24, 25, 26, 31, 33, 35, 38, 39, 44, 45, 54, 56, 57]
	quiz_b_remove = [5, 40, 47, 48, 20, 21]
	quiz_b_index = list(quiz_b_gre_index + quiz_b_safety_index + quiz_b_science_index)

	a1 = [0, 1, 2, 3, 4, 5, 8, 10, 13, 14, 16, 18, 19, 20, 21, 22, 24, 26, 29, 32, 37, 41, 42, 46, 55, 57, 58]
	b1 = [3, 6, 9, 11, 12, 13, 16, 18, 22, 24, 25, 27, 29, 30, 33, 36, 39, 44, 45, 46, 49, 50, 52, 54, 55, 56, 58]
	
	a2 = [6, 7, 9, 11, 15, 27, 28, 30, 31, 33, 34, 35, 36, 38, 39, 40, 43, 44, 45, 48, 49, 50, 51, 52, 53, 54, 59]
	b2 = [0, 1, 2, 4, 7, 8, 10, 14, 15, 17, 19, 23, 26, 28, 31, 32, 34, 35, 37, 38, 41, 42, 43, 51, 53, 57, 59]

	quiz_a_repeated_index = [0, 3, 4, 6, 8, 9, 14, 15, 19, 21, 24, 26, 30, 32, 34, 37, 40, 43, 44, 54, 58, 59]
	quiz_b_repeated_index = [13, 22, 33, 37, 52, 17, 36, 0, 54, 44, 11, 39, 8, 6, 15, 24, 57, 43, 1, 19, 49, 4]

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

	quiz_a_user_record_filename = "csv/between_subject_A.csv"
	# quiz_b_user_record_filename = "csv/MTurk1_B_user_record.csv"

	quiz_a_data = {}
	# quiz_b_data = {}

	with open(quiz_a_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz_a = reader[3:]

	# with open(quiz_b_user_record_filename, 'rt') as csvfile:
	# 	reader = list(csv.reader(csvfile))
	# 	quiz_b = reader[3:]

	for i in range(len(quiz_a)):
		quiz_a_data[quiz_a[i][17]] = quiz_a[i][22:-1]

	# for i in range(len(quiz_b)):
	# 	quiz_b_data[quiz_b[i][17]] = quiz_b[i][22:-1]


	print(quiz_a_data)

	# all_users_temp = quiz_a_data.keys()
	# all_users_temp.extend(x for x in quiz_b_data.keys() if x not in quiz_a_data.keys())
	# all_user = []

	# for user in all_users_temp:
	# 	if user in quiz_a_data.keys() and user in quiz_b_data.keys():
	# 		all_user.append(user)


	# result_data = []

	# for u in range(len(all_users)):
	# 	user = all_users[u]
	# 	result_data.append(0)

	# 	for i in quiz_sub_index:
	# 		q_user_answer = quiz_data[user][5 * i + 4]

	# 		if q_user_answer == quiz_answer[i]:
	# 			result_data[u] += 1




if __name__ == "__main__":
	dump_correct_rate()








