'''
    parse_quiz.py
    Author: Liwei Jiang
    Date: 09/08/2018
    Usage: Parse customized quizzes for batch 4 users
'''
import csv
import itertools
import random
import numpy
import json

# batch4 score report and user record files
batch4_score_report_filename = "csv/batch4_score_report.csv"
batch4_user_record_filename = "csv/batch4_user_record.csv"

def parse_answers():
	'''
		parse answers of batch4 pre qualtrics quiz 
	'''
	quiz_answer = []
	quiz_question = []
	with open(batch4_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Total":
					quiz_answer.append(reader[i - 1][1])	

	quiz_answer.pop(63) # remove the attention check question
	return quiz_answer


def parse_user_records():
	'''
		parse user records of batch4 pre qualtrics quiz 
	'''
	user_record = {}
	with open(batch4_user_record_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		quiz = reader[3:]

	for i in range(len(quiz)):
		user_record[quiz[i][17] + "_" + quiz[i][18]] = [quiz[i][j + 29] for j in range(63)]
		user_record[quiz[i][17] + "_" + quiz[i][18]].extend([quiz[i][j + 30] for j in range(63, 96)])
	return user_record

def parse_questions():
	'''
		parse questions of batch4 pre qualtrics quiz 
	'''
	quiz_question = []

	with open(batch4_score_report_filename, 'rb') as csvfile:
		reader = list(csv.reader(csvfile))
		for i in range(len(reader)):
			if len(reader[i]) >= 2:
				if reader[i][1] == "Field":
					quiz_question.append(reader[i - 1][0])

	# remove the prefix tags for each question
	# for i in range(97):
	# 	if i < 11:
	# 		quiz_question[i] = quiz_question[i][5:]
	# 	else:
	# 		quiz_question[i] = quiz_question[i][6:]
	# 	while quiz_question[i][0] == " ":
	# 		quiz_question[i] = quiz_question[i][1:]
	# 	while quiz_question[i][-1] == " ":
	# 		quiz_question[i] = quiz_question[i][:-1]

	quiz_question.pop(63) # remove the attention check question
	return quiz_question


def get_wrong_questions_qualtrics_id():
	'''
		get the qualtrics ids of questions the users got wrong in batch4 pre qualtrics quiz 
	'''
	quiz_answer = parse_answers()
	user_record = parse_user_records()

	user_wrong_qualtrics_id = {}

	users = user_record.keys()
	for user in users:
		wrong_question_qualtrics_id = []
		for i in range(96):
			if user_record[user][i] != quiz_answer[i]:
				wrong_question_qualtrics_id.append(i)
		user_wrong_qualtrics_id[user] = wrong_question_qualtrics_id

	return user_wrong_qualtrics_id

def generate_user_qualtrics_import_txt():
	'''
		generate customized recall question txt files that can be imported by qualtrics surveys
	'''
	quiz_question = parse_questions()
	user_wrong_questions_qualtrics_id = get_wrong_questions_qualtrics_id()

	users = user_wrong_questions_qualtrics_id.keys()
	users.sort()
	print(users)
	for user in users:
		result_string = "[[AdvancedFormat]]"
		result_string += "\n"
		result_string += "[[Question:DB]]"
		result_string += "\n"
		result_string += "Thanks for using our apps for the last few days! Hope you had fun learning and interacting with them. Please do not refer to any external resources, including the apps. Your performance on this exam is only used to evaluate your knowledge gain over the past few days and will not be revealed to anyone else. Now please answer the following questions. If you don't know the answer, please type N/A"
		result_string += "\n"
		result_string += "[[Question:TE]]" 
		result_string += "\n"
		result_string += "Full Name"
		result_string += "\n"
		result_string += "[[Block]]"
		result_string += "\n"

		for i in user_wrong_questions_qualtrics_id[user][:-2]:
			result_string += "[[Question:TE]]" 
			result_string += "\n"
			result_string += quiz_question[i]
			result_string += "\n"
			result_string += "[[Block]]"
			result_string += "\n"

		result_string += "[[Question:TE]]" 
		result_string += "\n"
		result_string += quiz_question[user_wrong_questions_qualtrics_id[user][-1]]

		# print(user)
		# print(result_string)
		f = open("recall_quizzes/" + user + "_quiz.txt", 'w')
		f.write(result_string)
		f.close()


if __name__ == "__main__":
	generate_user_qualtrics_import_txt()















