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

# a list of finished users
finished_users = ["shuo_han", "Yun_Zhang", "zhiyuan_lin", "Yunan_Xu", "Heidi_He","Xuebing_Leng", "Jackie_Yang", "Kebing_Li", \
				  "Irene_Lai", "Jeongeun_Park", "Ran_Gong", "Jerry_Hong", "Fangjie_Cao", "Miao_Zhang", "Jacqueline_Hang", \
				  "Xiaoou_Wang", "Yin_Li"]

# "", "Harry_Liu"

# recall result filename
recall_result_filename = "recall_result.csv"

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
		user = quiz[i][17] + "_" + quiz[i][18]
		user = user.replace(" ", "")
		user_record[user] = [quiz[i][j + 29] for j in range(63)]
		user_record[user].extend([quiz[i][j + 30] for j in range(63, 96)])
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

		for i in user_wrong_questions_qualtrics_id[user][:-1]:
			result_string += "[[Question:TE]]" 
			result_string += "\n"
			result_string += quiz_question[i]
			result_string += "\n"
			result_string += "[[PageBreak]]"
			result_string += "\n"

		result_string += "[[Question:TE]]" 
		result_string += "\n"
		result_string += quiz_question[user_wrong_questions_qualtrics_id[user][-1]]

		f = open("recall_quizzes/" + user + "_quiz.txt", 'w')
		f.write(result_string)
		f.close()


def parse_user_recall_result():
	'''
		parse user's recall results
	'''
	user_result = {}
	for user in finished_users:
		with open("result/" + user + ".csv", 'rt') as csvfile:
			reader = list(csv.reader(csvfile))
			result = reader[3:]
		user_result[user] = result[0][18:]

	return user_result


def get_user_answer_list(quiz_answer, wrong_questions_qualtrics_id, recall_result, user):
	'''
		get a list of user's answers (including placeholdera for questions not appearing in their recall quiz)
	'''
	user_answer = ['------------------------' for i in range(96)]
	for i in range(len(wrong_questions_qualtrics_id)):
		try:
			user_answer[wrong_questions_qualtrics_id[i]] = recall_result[i]
		except:
			user_answer[wrong_questions_qualtrics_id[i-1]] = "NA"
			user_answer[wrong_questions_qualtrics_id[i]] = recall_result[i-1]
			print("Missing 1 Question")
	user_answer.insert(0, user)

	return user_answer

def generate_user_recall_result_csv():
	'''
		generate a csv containing user's recall result
	'''
	quiz_answer = parse_answers()
	quiz_question = parse_questions()
	user_wrong_questions_qualtrics_id = get_wrong_questions_qualtrics_id()
	user_recall_result = parse_user_recall_result()

	result_report = []
	quiz_question.insert(0, "Question")
	result_report.append(quiz_question)
	result_report.append(quiz_answer)
	result_report[1].insert(0, "Answer")

	for user in finished_users:
		print(user)
		user_answer = get_user_answer_list(quiz_answer, user_wrong_questions_qualtrics_id[user], user_recall_result[user], user)
		result_report.append(user_answer)

	result_report = zip(*result_report)
	with open(recall_result_filename, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(result_report)

if __name__ == "__main__":
	generate_user_recall_result_csv()
