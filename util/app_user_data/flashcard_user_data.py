'''
    flashcard_time.py
    Author: Liwei Jiang
    Date: 02/08/2018
    Usage: Calculate the usage time of the QuizBot app for a user.
'''
import csv
import sys
import os
from datetime import datetime

dirname = os.path.dirname(__file__)
result_filename = "flashcard_data_analysis.txt"

# Past Pilot Users: "Allie_Blaising", "Phoebe_Kimm", "Nik_Marda"

users = ["Golrokh_Emami", "Cynthia_Torma", "Jordan_Cho", "Laura_Davey", "Courtney_Smith", \
		 "Marianne_Cowherd", "Tugce_Tasci", "Edgar_Rios", "Kimberly_Ha", "Sen_Wu", "Max_Cobb"] 
		 
# time break considered to be a leave
BREAK_TIME = 30 
# indices of useful data entry
TIME_STAMP_INDEX = 5
EVENT_INDEX = 4
QID_INDEX = 3

if len(sys.argv) == 3:
	users = [sys.argv[1] + "_" + sys.argv[2]]

time_report = {} # a disctionary of dates and corresponding daily usage time
question_report = {} # a disctionary of studied question (total studies question, unique studies questions)

for user in users:
	flashcard_filename = os.path.join(dirname, "../../SQL_query/user_data/flashcard_" + user + ".csv")

	with open(flashcard_filename, 'rt') as csvfile:
		reader = list(csv.reader(csvfile))
		flashcard_file = reader[1:]

	sub_time_report = [] 
	day_counter = 0 
	total_usage_time = 0 

	old_time_stamp = flashcard_file[0][TIME_STAMP_INDEX]
	old_time_stamp = datetime.strptime(old_time_stamp, "%Y-%m-%d %H:%M:%S")

	for i in range(1,len(flashcard_file)):
		time_stamp = flashcard_file[i][TIME_STAMP_INDEX]
		time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")	

		if (time_stamp.year, time_stamp.month, time_stamp.day) != (old_time_stamp.year, old_time_stamp.month, old_time_stamp.day):
			day_counter += 1
			sub_time_report.append((old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60))
			total_usage_time = 0

		if (time_stamp - old_time_stamp).total_seconds() <= BREAK_TIME:
			total_usage_time += (time_stamp - old_time_stamp).total_seconds()
		old_time_stamp = time_stamp

	sub_time_report.append((old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60))
	time_report[user] = sub_time_report

	events = [x[QID_INDEX] for x in flashcard_file if x[EVENT_INDEX] == "I don't know" or x[EVENT_INDEX] == "got it"]
	question_report[user] = ((len(events), len(set(events))))

output_string = ""
for user in time_report:
	total_time = 0
	output_string += "----- "
	output_string += user
	output_string += " -----\n"

	for day_report in time_report[user]:
		output_string += str(day_report[0])
		output_string += "."
		output_string += str(day_report[1])
		output_string += "."
		output_string += '{:02}'.format(day_report[2])
		output_string += ": "
		output_string += str(round(day_report[3], 2))
		output_string += " min"
		output_string += "\n"
		total_time += day_report[3]
	output_string += "\n"

	output_string += "Number of questions practiced       : "
	output_string += str(question_report[user][0])
	output_string += "\n"
	output_string += "Number of unique questions practiced: "
	output_string += str(question_report[user][1])
	output_string += "\n"
	output_string += "Total APP Usage Time                : "
	output_string += str(round(total_time, 2))
	output_string += " min"
	output_string += "\n\n"

f = open(result_filename, 'w')
f.write(output_string)
f.close()
print(output_string)

