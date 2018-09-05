'''
    quizbot_time.py
    Author: Liwei Jiang
    Date: 02/08/2018
    Usage: Calculate the usage time of the QuizBot app for a user.
'''
import csv
import sys
import os
import numpy
from datetime import datetime
from collections import Counter
import math

dirname = os.path.dirname(__file__)
result_filename = "quizbot_data_analysis.txt"
practice_question_file = "practice_question.csv"
correctness_rate_file = "correctness_rate.csv"

users = ["Sherry_Ruan", "Jeongeun_Park", "Shuo_Han"]

# a dictionary of the number of times user studied each question
practice_question_count = {}

# a dictionary of the correctness rate of each question
question_correctness_rate = {}

# qid of all 96 questions appeared in either quiz a or quiz b
all_appeared_question_qid = [1, 2, 3, 5, 6, 8, 9, 10, 11, 14, 15, 17, 18, 19, 21, 24, 25, 27, 29, 30, 31, 32, 35, 37, 38, 40, 41, 42, 44, 45, 46, 49, 50, 51, 52, 53, 55, 56, 58, 59, 64, 65, 68, 70, 72, 73, 74, 75, 76, 77, 79, 82, 83, 84, 85, 87, 88, 89, 90, 92, 93, 94, 97, 99, 100, 102, 103, 104, 106, 111, 112, 113, 114, 117, 118, 120, 121, 125, 127, 128, 130, 131, 132, 133, 135, 136, 138, 139, 141, 142, 143, 144, 145, 146, 147, 148]

# 54 questions in post-study quiz (quiz B)
postquiz_qid = set([146, 145, 118, 130, 148, 117, 127, 111, 120, 141, 143, 147, 114, 121, \
                   106, 102, 112, 133, 72, 79, 90, 84, 58, 83, 59, 50, 56, 73, 93, 68, 53, \
                   77, 75, 97, 89, 87, 25, 24, 1, 19, 21, 44, 17, 30, 38, 6, 8, 2, 11, 37, \
                   9, 41, 29, 42])

quiz_a_to_id = {0: 148, 1: 49, 2: 18, 3: 111, 4: 6, 5: 51, 6: 93, 7: 94, 8: 102, 9: 21, \
                10: 128, 11: 82, 13: 135, 14: 114, 15: 146, 16: 113, 18: 131, 19: 41, \
                20: 55, 21: 37, 22: 52, 24: 58, 26: 11, 27: 64, 28: 14, 29: 88, 30: 84, \
                31: 103, 32: 90, 33: 32, 34: 117, 35: 136, 36: 31, 37: 44, 38: 132, 39: 45, \
                40: 42, 41: 76, 42: 104, 43: 53, 44: 72, 45: 5, 46: 15, 48: 100, 49: 27, 50: 65, \
                51: 35, 52: 138, 53: 125, 54: 127, 55: 99, 57: 46, 58: 75, 59: 79}

quiz_b_to_id = {0: 146, 1: 72, 2: 25, 3: 145, 4: 79, 6: 90, 7: 118, 8: 84, 9: 24, 10: 1, \
                11: 58, 12: 130, 13: 148, 14: 19, 15: 117, 16: 83, 17: 21, 18: 59, 19: 127, \
                22: 111, 23: 50, 24: 44, 25: 17, 26: 30, 27: 56, 28: 120, 29: 141, 30: 73, 31: 38, \
                32: 143, 33: 6, 34: 147, 35: 8, 36: 114, 37: 93, 38: 2, 39: 11, 41: 121, 42: 68, \
                43: 53, 44: 37, 45: 9, 46: 77, 49: 75, 50: 106, 51: 97, 52: 102, 53: 112, 54: 41, \
                55: 89, 56: 29, 57: 42, 58: 133, 59: 87}

quizbot_index_2_qid_dict = {0: 147, 1: 100, 2: 138, 3: 118, 4: 112, 5: 64, 6: 32, 7: 50, 8: 136, \
                            9: 143, 10: 121, 11: 132, 12: 120, 13: 8, 14: 5, 15: 30, 16: 117, \
                            17: 125, 18: 14, 19: 103, 20: 19, 21: 27, 22: 84, 23: 93, 24: 79, 25: 72, \
                            26: 2, 27: 31, 28: 42, 29: 35, 30: 65, 31: 25, 32: 1, 33: 21, 34: 38, \
                            35: 97, 36: 94, 37: 53, 38: 45, 39: 82, 40: 87, 41: 127, 42: 146, 43: 68, \
                            44: 139, 45: 85, 46: 74, 47: 70}

quizbot_qid = [147, 100, 138, 118, 112, 64, 32, 50, 136, 143, 121, 132, 120, 8, 5, 30, 117, 125, 14, \
               103, 19, 27, 84, 93, 79, 72, 2, 31, 42, 35, 65, 25, 1, 21, 38, 97, 94, 53, 45, 82, 87, \
               127, 146, 68, 139, 85, 74, 70]

qid_2_qualtricsID_dict = {value: key for key, value in quiz_b_to_id.items()}
qid_2_qualtricsID_dict_A = {value: key for key, value in quiz_a_to_id.items()}

postquiz_qid_A = set(qid_2_qualtricsID_dict_A.keys())


# time break considered to be a leave
BREAK_TIME = 30
# indices of useful data entry
SENDER_INDEX = 4
RECIPIENT_INDEX = 5
TIME_STAMP_INDEX = 8
QID_INDEX = 3
SCORE_INDEX = 5
TYPE_INDEX = 6
BEGIN_UID_INDEX = 7
END_UID_INDEX = 8
UID_INDEX = 3

if len(sys.argv) == 3:
    users = [sys.argv[1] + "_" + sys.argv[2]]

time_report = {} # a disctionary of dates and corresponding daily usage time
practice_report = {}
question_report = {} # a disctionary of studied question (total studies question, unique studies questions)

for user in users:
    conversation_filename = os.path.join(
        dirname, "../../SQL_query/user_data/quizbot_conversation_" + user + ".csv")

    user_history_filename = os.path.join(
        dirname, "../../SQL_query/user_data/quizbot_user_history_" + user + ".csv")

    # open the conversation data file
    with open(conversation_filename, 'rt') as csvfile:
        reader = list(csv.reader(csvfile))
        conversation_file = reader[1:]

    # open the user history data file
    with open(user_history_filename, 'rt') as csvfile:
        reader = list(csv.reader(csvfile))
        user_history_file = reader[1:]

    # unique user id and unique chatbot id
    user_id = conversation_file[0][0]
    chatbot_id = "854518728062939"

    sub_time_report = []  # a disctionary of dates and corresponding daily usage time
    sub_practice_report = []
    # list of tuples of (0 if chatbot to user / 1 if user to chatbot <which is not used for now> , time breaks in second)
    analysis = [[]]
    day_counter = 0  # counter of total usage days
    total_usage_time = 0  # counter of total usage time

    sender = conversation_file[0][SENDER_INDEX]
    recipient = conversation_file[0][RECIPIENT_INDEX]
    old_time_stamp = conversation_file[0][TIME_STAMP_INDEX]
    old_time_stamp = datetime.strptime(old_time_stamp, "%Y-%m-%d %H:%M:%S")
    old_time_stamp_uid = 0

    if sender == chatbot_id and recipient == user_id:
        analysis[day_counter].append((0, 0))
    else:
        analysis[day_counter].append((1, 0))

    for i in range(1, len(conversation_file)):
        time_stamp = conversation_file[i][TIME_STAMP_INDEX]
        time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")

        if (time_stamp.year, time_stamp.month, time_stamp.day) != (old_time_stamp.year, old_time_stamp.month, old_time_stamp.day):
            analysis.append([])
            day_counter += 1
            sub_time_report.append(
                (old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60))
            total_usage_time = 0
            new_time_stamp_uid = conversation_file[i][UID_INDEX]
            sub_practice_report.append([int(x[QID_INDEX]) for x in user_history_file \
                                       if (x[END_UID_INDEX] != "" and x[BEGIN_UID_INDEX] >= old_time_stamp_uid and x[BEGIN_UID_INDEX] <= new_time_stamp_uid)])
            old_time_stamp_uid = new_time_stamp_uid

        if (time_stamp - old_time_stamp).total_seconds() <= BREAK_TIME:
            total_usage_time += (time_stamp - old_time_stamp).total_seconds()
        old_time_stamp = time_stamp

    sub_time_report.append((old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60))
    sub_practice_report.append([int(x[QID_INDEX]) for x in user_history_file \
                                       if (x[END_UID_INDEX] != "" and x[BEGIN_UID_INDEX] >= old_time_stamp_uid)])
    time_report[user] = sub_time_report
    practice_report[user] = sub_practice_report

    events = [int(x[QID_INDEX]) for x in user_history_file if x[END_UID_INDEX] != ""]
    print("\n------------")
    print(user)
    events.sort()
    print(events)

    events_correct = [int(x[QID_INDEX]) for x in user_history_file if x[END_UID_INDEX] != "" and int(x[SCORE_INDEX]) > 8]

    qid_in_postquiz_seen = set(events) & postquiz_qid
    qualtricsID_in_postquiz_seen = [qid_2_qualtricsID_dict[qid] for qid in qid_in_postquiz_seen]
    most_counts_qid, num_most_counts = Counter(events).most_common(1)[0]  # get question with most counts and the counts
    question_report[user] = (len(events), len(set(events)), len(qid_in_postquiz_seen), qualtricsID_in_postquiz_seen, num_most_counts)

    # for q in quizbot_qid:
    #     practice_question_count[user][q] = events.count(q)
    # for q in quizbot_qid:
    #     if float(events.count(q)) == 0:
    #         question_correctness_rate[user][q] = ''
    #     else:
    #         question_correctness_rate[user][q] = round(float(events_correct.count(q)) / float(events.count(q)), 2)

    if user == 'Zilin_Ma':
        qid_in_postquiz_seen = set(events) & postquiz_qid_A
        qualtricsID_in_postquiz_seen = [qid_2_qualtricsID_dict_A[qid] for qid in qid_in_postquiz_seen]
        print(qualtricsID_in_postquiz_seen)
        question_report[user] = (len(events), len(set(events)), len(qid_in_postquiz_seen), qualtricsID_in_postquiz_seen)

        # for q in quizbot_qid:
        #     practice_question_count[user][q] = events.count(q)
        # for q in quizbot_qid:
        #     if float(events.count(q)) == 0:
        #         question_correctness_rate[user][q] = ''
        #     else:
        #         question_correctness_rate[user][q] = round(float(events_correct.count(q)) / float(events.count(q)), 2)

output_string = "\n"
for user in time_report:
    total_time = 0
    output_string += "----- "
    output_string += user
    output_string += " -----\n"

    for j, day_report in enumerate(time_report[user]):
        output_string += str(day_report[0])
        output_string += "."
        output_string += str(day_report[1])
        output_string += "."
        output_string += '{:02}'.format(day_report[2])
        output_string += ": "
        output_string += "{:.2f}".format(day_report[3])
        output_string += " min"
        output_string += " "*19
        output_string += str(len(practice_report[user][j])) + " -- "
        output_string += str(practice_report[user][j])
        output_string += "\n"
        total_time += day_report[3]
    output_string += "\n"

    output_string += "Number of questions practiced       : "
    output_string += str(question_report[user][0])
    output_string += "\n"
    output_string += "Number of unique questions practiced: "
    output_string += str(question_report[user][1])
    output_string += "\n"
    # output_string += "Number of post-quiz questions seen  : "
    # output_string += str(question_report[user][2])
    # output_string += "\n"
    # output_string += '['+', '.join(str(e) for e in question_report[user][3]) + ']\n'
    output_string += "Max count                           : "
    output_string += str(question_report[user][4])
    output_string += "\n"
    output_string += "Total APP Usage Time                : "
    output_string += str(round(total_time, 2))
    output_string += " min"
    output_string += "\n\n"

f = open(result_filename, 'w')
f.write(output_string)
f.close()
print(output_string)

all_practice_question_count = [['qid'] + all_appeared_question_qid]

for user in practice_question_count.keys():
    user_practice_question_count = [user] + practice_question_count[user].values()
    all_practice_question_count.append(user_practice_question_count)

with open(practice_question_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_practice_question_count)

all_question_correctness_rate = [['qid'] + all_appeared_question_qid]

for user in question_correctness_rate.keys():
    user_correctness_rate = [user] + question_correctness_rate[user].values()
    all_question_correctness_rate.append(user_correctness_rate)

# all_question_correctness_rate = list(map(list, zip(*all_question_correctness_rate)))
with open(correctness_rate_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_question_correctness_rate)

