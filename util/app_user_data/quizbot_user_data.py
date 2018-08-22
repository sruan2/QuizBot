'''
    quizbot_time.py
    Author: Liwei Jiang
    Date: 02/08/2018
    Usage: Calculate the usage time of the QuizBot app for a user.
    	   The code can be modified to compute the user reaction time by only considering the action that user sends message to the chatbot.
'''
import csv
import sys
import os
from datetime import datetime

dirname = os.path.dirname(__file__)
result_filename = "quizbot_data_analysis.txt"

# Past Pilot Users: "Alex_Nguyen", "Maika_Isogawa", "Michael_Cooper", "Jordan_Cho", "Laura_Davey"

# users = ["Veronica_Cruz", "Jackie_Fortin", "Eleni_Aneziris", "Zilin_Ma", "Jongho_Kim", \
#          "Nina_Tai", "Yi_Feng", "Dae_hyun_Kim", "Pingyu_Wang", "Lantao_Mei", \
#          "Michael_Silvernagel", "Bianca_Yu"]

# within-subject users
users = ["Noah Yinuo_Yao", "Dee Dee_Thao", "Zhenqi_Hu", "Jingyi_Li", "Joy_Yuzuriha", "Tyler_Yep", \
         "Andrew_Ying", "Henry_Qin", "Nina_Horowitz"]

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
TYPE_INDEX = 6
END_QID_INDEX = 8

if len(sys.argv) == 3:
    users = [sys.argv[1] + "_" + sys.argv[2]]

time_report = {}  # a disctionary of dates and corresponding daily usage time
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
    # list of tuples of (0 if chatbot to user / 1 if user to chatbot <which is not used for now> , time breaks in second)
    analysis = [[]]
    day_counter = 0  # counter of total usage days
    total_usage_time = 0  # counter of total usage time

    sender = conversation_file[0][SENDER_INDEX]
    recipient = conversation_file[0][RECIPIENT_INDEX]
    old_time_stamp = conversation_file[0][TIME_STAMP_INDEX]
    old_time_stamp = datetime.strptime(old_time_stamp, "%Y-%m-%d %H:%M:%S")

    if sender == chatbot_id and recipient == user_id:
        analysis[day_counter].append((0, 0))
    else:
        analysis[day_counter].append((1, 0))

    for i in range(1, len(conversation_file)):
        sender = conversation_file[i][SENDER_INDEX]
        recipient = conversation_file[i][RECIPIENT_INDEX]
        try:
            time_stamp = conversation_file[i][TIME_STAMP_INDEX]
            time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
        except:
            time_stamp = conversation_file[i][TIME_STAMP_INDEX + 1]
            time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")

        if (time_stamp.year, time_stamp.month, time_stamp.day) != (old_time_stamp.year, old_time_stamp.month, old_time_stamp.day):
            analysis.append([])
            day_counter += 1
            sub_time_report.append(
                (old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60))
            total_usage_time = 0

        if sender == chatbot_id and recipient == user_id:
            analysis[day_counter].append(
                (0, (time_stamp - old_time_stamp).total_seconds()))
        else:
            analysis[day_counter].append(
                (1, (time_stamp - old_time_stamp).total_seconds()))

        if (time_stamp - old_time_stamp).total_seconds() <= BREAK_TIME:
            total_usage_time += (time_stamp - old_time_stamp).total_seconds()
        old_time_stamp = time_stamp

    sub_time_report.append(
        (old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60))
    time_report[user] = sub_time_report

    events = [int(x[QID_INDEX]) for x in user_history_file if x[END_QID_INDEX] != ""]
    qid_in_postquiz_seen = set(events) & postquiz_qid
    qualtricsID_in_postquiz_seen = [qid_2_qualtricsID_dict[qid] for qid in qid_in_postquiz_seen]
    question_report[user] = (len(events), len(set(events)), len(qid_in_postquiz_seen), qualtricsID_in_postquiz_seen)

    if user == 'Zilin_Ma':
        qid_in_postquiz_seen = set(events) & postquiz_qid_A
        qualtricsID_in_postquiz_seen = [qid_2_qualtricsID_dict_A[qid] for qid in qid_in_postquiz_seen]
        print(qualtricsID_in_postquiz_seen)
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
