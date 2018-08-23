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

# users = ["Golrokh_Emami", "Cynthia_Torma", "Jordan_Cho", "Laura_Davey", "Courtney_Smith", \
#           "Marianne_Cowherd", "Tugce_Tasci", "Edgar_Rios", "Kimberly_Ha", "Sen_Wu", "Max_Cobb"]

#users = ["Kimberly_Ha", "Sen_Wu", "Max_Cobb"]

# within-subject users
users = ["Yinuo_Yao", "Dee Dee_Thao", "Jenn_Hu", "jingyi_li", "Joy_Yuzuriha", "Tyler_Yep", \
         "Andrew_Ying", "Henry_Qin", "Nina_Horowitz", "Daniel_Do", "Claire_Yang", "Olivia_Yang"]
         # "Francis_Yan"]


# 54 questions in post-study quiz (quiz B)
postquiz_qid = set([146, 145, 118, 130, 148, 117, 127, 111, 120, 141, 143, 147, 114, 121, \
                   106, 102, 112, 133, 72, 79, 90, 84, 58, 83, 59, 50, 56, 73, 93, 68, 53, \
                   77, 75, 97, 89, 87, 25, 24, 1, 19, 21, 44, 17, 30, 38, 6, 8, 2, 11, 37, \
                   9, 41, 29, 42])

qualtricsID_2_qid = {0: 146, 1: 72, 2: 25, 3: 145, 4: 79, 6: 90, 7: 118, 8: 84, 9: 24, 10: 1, \
                    11: 58, 12: 130, 13: 148, 14: 19, 15: 117, 16: 83, 17: 21, 18: 59, 19: 127, \
                    22: 111, 23: 50, 24: 44, 25: 17, 26: 30, 27: 56, 28: 120, 29: 141, 30: 73, 31: 38, \
                    32: 143, 33: 6, 34: 147, 35: 8, 36: 114, 37: 93, 38: 2, 39: 11, 41: 121, 42: 68, \
                    43: 53, 44: 37, 45: 9, 46: 77, 49: 75, 50: 106, 51: 97, 52: 102, 53: 112, 54: 41, \
                    55: 89, 56: 29, 57: 42, 58: 133, 59: 87}

qid_2_qualtricsID_dict = {value: key for key, value in qualtricsID_2_qid.items()}

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

    events = [int(x[QID_INDEX]) for x in flashcard_file if x[EVENT_INDEX] == "I don't know" or x[EVENT_INDEX] == "got it"]
    qid_in_postquiz_seen = set(events)&postquiz_qid
    qualtricsID_in_postquiz_seen = [qid_2_qualtricsID_dict[qid] for qid in qid_in_postquiz_seen]
    question_report[user] = (len(events), len(set(events)), len(qid_in_postquiz_seen), qualtricsID_in_postquiz_seen)

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
    output_string += "Number of post-quiz questions seen  : "
    output_string += str(question_report[user][2])
    output_string += "\n"
    output_string += '['+', '.join(str(e) for e in question_report[user][3]) + ']\n'
    output_string += "Total APP Usage Time                : "
    output_string += str(round(total_time, 2))
    output_string += " min"
    output_string += "\n\n"

f = open(result_filename, 'w')
f.write(output_string)
f.close()
print(output_string)



# for user in users:
#     flashcard_filename = os.path.join(dirname, "../../SQL_query/user_data/flashcard_" + user + ".csv")

#     print(user)

#     with open(flashcard_filename, 'rt') as csvfile:
#         reader = list(csv.reader(csvfile))
#         flashcard_file = reader[1:]

#     sub_time_report = []
#     day_counter = 0
#     total_usage_time = 0

#     old_time_stamp = flashcard_file[0][TIME_STAMP_INDEX]
#     old_time_stamp = datetime.strptime(old_time_stamp, "%Y-%m-%d %H:%M:%S")

#     for i in range(1,len(flashcard_file)):
#         time_stamp = flashcard_file[i][TIME_STAMP_INDEX]
#         time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")

#         if (time_stamp.year, time_stamp.month, time_stamp.day) == (2018, 8, 21):

#             if time_stamp.hour == 21 or time_stamp.hour == 22:
#                 if (time_stamp - old_time_stamp).total_seconds() <= BREAK_TIME:
#                     total_usage_time += (time_stamp - old_time_stamp).total_seconds()
#         old_time_stamp = time_stamp

#     print(total_usage_time/60)
