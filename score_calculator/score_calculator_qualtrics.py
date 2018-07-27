'''
    score_calculator.py
    Author: Liwei Jiang
    Date: 19/07/2018
    Usage: Check the number of inconsistent answer of the pre- and post- quizzes.
'''
import csv
import sys
import json

file_name_1 = sys.argv[1]
file_name_2 = sys.argv[2]
result_file = "user_result_qualtrics.csv"
result_data = []


with open(file_name_1, 'rt') as csvfile:
	reader = list(csv.reader(csvfile))
	reader = len(reader[3:])
	print(reader)





with open(file_name_2, 'rt') as csvfile:
	reader = list(csv.reader(csvfile))
	reader = len(reader[3:])
	# print(reader)


with open(result_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(result_data)




