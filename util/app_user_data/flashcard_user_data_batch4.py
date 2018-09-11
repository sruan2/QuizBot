'''
    flashcard_user_data_batch4.py
    Author: Liwei Jiang
    Date: 02/08/2018
    Usage: Calculate the usage time of the QuizBot app for a user.
'''
import csv
import sys
import os
from datetime import datetime
from collections import Counter

dirname = os.path.dirname(__file__)
result_filename = "flashcard_data_analysis_batch4.txt"

users = ["Jeongeun_Park","shuo_han", "Harry_Liu",
         "Yunan_Xu", "Jackie_Yang", "xuebing_leng", "Zhiyuan_Lin", "Jerry_Hong", "Kebing_Li", "Yun_Zhang",
         "Xiaoou_Wang", "Yue_Lian", "Jackie_Hang", "Heidi_He", "Anna_Yu", "Irene_Lai",
         "Qiwen_Zhang", "Ran_Gong", "Tianshi_Li", "wenjing_yan", "Yin_Li",
         "Harry_Liu", "Wendy_Li", 
         "Wenming_Zhang", "Miao_Zhang", "Fangjie_Cao", "Meng_Tang", "Elaine_Yin",
         "Yiran_Shen", 
         "Ziang_Zhu", 
         "Hao_Chen", "Akemi_Wijayabahu", "Yifan_He", 
         "Hongyu_Zhai", "Yibing_Du",
         "Mkhanyisi_Gamedze", "Haihong_L", "Wenxiao_Huang",
         "Mingchen_Li", 
         "Ramon_Tuason",
         "Hanke_Gu",
         "Huiying_Chen"
         ]

if len(sys.argv) == 3:
    users = [sys.argv[1] + "_" + sys.argv[2]]

# 54 questions in post-study quiz (quiz B)
postquiz_qid = set([1, 2, 6, 8, 9, 11, 17, 19, 21, 24, 25, 29, 30, 37, 38, 41, 42, 44, 50, 53, 56, \
                    58, 59, 68, 72, 73, 75, 77, 79, 83, 84, 87, 89, 90, 93, 97, 102, 106, 111, 112, \
                    114, 117, 118, 120, 121, 127, 130, 133, 141, 143, 145, 146, 147, 148])

qualtricsID_2_qid = {0: 146, 1: 72, 2: 25, 3: 145, 4: 79, 6: 90, 7: 118, 8: 84, 9: 24, 10: 1, \
                    11: 58, 12: 130, 13: 148, 14: 19, 15: 117, 16: 83, 17: 21, 18: 59, 19: 127, \
                    22: 111, 23: 50, 24: 44, 25: 17, 26: 30, 27: 56, 28: 120, 29: 141, 30: 73, 31: 38, \
                    32: 143, 33: 6, 34: 147, 35: 8, 36: 114, 37: 93, 38: 2, 39: 11, 41: 121, 42: 68, \
                    43: 53, 44: 37, 45: 9, 46: 77, 49: 75, 50: 106, 51: 97, 52: 102, 53: 112, 54: 41, \
                    55: 89, 56: 29, 57: 42, 58: 133, 59: 87}

flashcard_index_2_qid_dict = {0: 15, 1: 135, 2: 55, 3: 51, 4: 56, 5: 141, 6: 128, 7: 106, 8: 111, \
                              9: 114, 10: 59, 11: 9, 12: 131, 13: 145, 14: 18, 15: 102, 16: 11, \
                              17: 133, 18: 130, 19: 83, 20: 41, 21: 148, 22: 75, 23: 90, 24: 99, \
                              25: 113, 26: 104, 27: 46, 28: 37, 29: 44, 30: 49, 31: 58, 32: 24, 33: 52, \
                              34: 73, 35: 6, 36: 29, 37: 88, 38: 17, 39: 76, 40: 77, 41: 89, 42: 144, \
                              43: 142, 44: 92, 45: 10, 46: 3, 47: 40}

flashcard_qid = [15, 135, 55, 51, 56, 141, 128, 106, 111, 114, 59, 9, 131, 145, 18, 102, 11, 133, \
                 130, 83, 41, 148, 75, 90, 99, 113, 104, 46, 37, 44, 49, 58, 24, 52, 73, 6, 29, \
                 88, 17, 76, 77, 89, 144, 142, 92, 10, 3, 40]

qid_2_qualtricsID_dict = {value: key for key, value in qualtricsID_2_qid.items()}

BREAK_TIME = 30 # time break considered to be a leave
# indices of useful data entry
TIME_STAMP_INDEX = 5
EVENT_INDEX = 4
QID_INDEX = 3

time_report = {} # a disctionary of dates and corresponding daily usage time
practice_report = {}
question_report = {} # a disctionary of studied question (total studies question, unique studies questions)
practice_question_count = {} # a dictionary of the number of times user studied each question
question_correctness_rate = {} # a dictionary of the correctness rate of each question

for user in users:
    flashcard_filename = os.path.join(dirname, "../../SQL_query/user_data/flashcard_" + user + ".csv")

    with open(flashcard_filename, 'rt') as csvfile:
        reader = list(csv.reader(csvfile))
        flashcard_file = reader[1:]

    sub_time_report = []
    sub_practice_report = []
    day_counter = 0
    total_usage_time = 0

    old_time_stamp = flashcard_file[0][TIME_STAMP_INDEX]
    old_time_stamp = datetime.strptime(old_time_stamp, "%Y-%m-%d %H:%M:%S")

    sub_practice_report.append([])
    if flashcard_file[0][EVENT_INDEX] in ("I don't know", "got it"):
	current_qid = int(flashcard_file[0][QID_INDEX])
	if current_qid != -1:
            sub_practice_report[day_counter].append(current_qid)

    for i in range(1,len(flashcard_file)):
        time_stamp = flashcard_file[i][TIME_STAMP_INDEX]
        time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")

        if (time_stamp.year, time_stamp.month, time_stamp.day) != (old_time_stamp.year, old_time_stamp.month, old_time_stamp.day):
            day_counter += 1
            sub_practice_report.append([])
            sub_time_report.append((old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60))
            total_usage_time = 0

        if (time_stamp - old_time_stamp).total_seconds() <= BREAK_TIME:
            total_usage_time += (time_stamp - old_time_stamp).total_seconds()
        old_time_stamp = time_stamp

        if flashcard_file[i][EVENT_INDEX] in ["I don't know", "got it", "change to safety", "change to random", "change to gre", "change to science"]:
            current_qid = int(flashcard_file[i][QID_INDEX])
	    if current_qid != -1:
		sub_practice_report[day_counter].append(current_qid)

    sub_time_report.append((old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60))
    time_report[user] = sub_time_report
    practice_report[user] = sub_practice_report
    practice_question_count[user] = {}
    question_correctness_rate[user] = {}

    events = [int(x[QID_INDEX]) for x in flashcard_file if (x[EVENT_INDEX] in ["I don't know", "got it", \
        "change to safety", "change to random", "change to gre", "change to science"] and int(x[QID_INDEX]) in flashcard_qid)]

    print("\n--------------------------------")
    print(user)
    events.sort()
    print(events)
    print('Count: '+str(len(events)))
    events_correct = [int(x[QID_INDEX]) for x in flashcard_file if x[EVENT_INDEX] == "got it" and int(x[QID_INDEX]) in flashcard_qid]
    qid_in_postquiz_seen = set(events)&postquiz_qid
    qualtricsID_in_postquiz_seen = [qid_2_qualtricsID_dict[qid] for qid in qid_in_postquiz_seen]
    most_counts_qid, num_most_counts = Counter(events).most_common(1)[0]  # get question with most counts and the counts
    question_report[user] = (len(events), len(set(events)), len(qid_in_postquiz_seen), qualtricsID_in_postquiz_seen, num_most_counts)

    for q in flashcard_qid:
        practice_question_count[user][q] = events.count(q)

    for q in flashcard_qid:
        if float(events.count(q)) == 0:
            question_correctness_rate[user][q] = ''
        else:
            question_correctness_rate[user][q] = round(float(events_correct.count(q)) / float(events.count(q)), 2)

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
        output_string += ":{:>5.2f}".format(day_report[3])
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

#print(practice_question_count)
#print(question_correctness_rate)



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
