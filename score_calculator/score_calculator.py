'''
    score_calculator.py
    Author: Liwei Jiang
    Date: 02/07/2018
    Usage: Calculate Scores for the pretest and posttest quizzes.
'''
import csv
import sys

file_name = sys.argv[1]

post_gre_index = [0, 4, 7, 12, 13, 15, 19, 21, 22, 28, 29, 32, 34, 36, 40, 41, 50, 52, 53, 58]
post_safety_index = [1, 3, 6, 8, 11, 16, 18, 23, 27, 30, 37, 42, 43, 46, 47, 48, 49, 51, 55, 59]
post_science_inex = [2, 5, 9, 10, 14, 17, 20, 24, 25, 26, 31, 33, 35, 38, 39, 44, 45, 54, 56, 57]

post_gre = []
post_safety = []
post_science = []

users = {}
questions = []

with open(file_name, 'rb') as csvfile:
	reader = list(csv.reader(csvfile))
	for i in range(len(reader[0])):
		if i % 3 == 0:
			index = i/3 - 1
			if index < 60 and index > -1:
				questions.append(reader[0][i])

post_gre = [questions[r] for r in post_gre_index]
post_safety = [questions[r] for r in post_safety_index]
post_science = [questions[r] for r in post_science_inex]


