'''
    quizbot batch 4 user data.py
    Author: Sherry Ruan, Liwei Jiang
    Date: 02/08/2018
    Usage: Calculate the usage time of the QuizBot app for a user.
'''
import csv
import sys
import os
import numpy
from datetime import datetime
#from pytz import timezone
from dateutil import tz
from collections import Counter
import math

dirname = os.path.dirname(__file__)
result_filename = "quizbot_data_analysis.txt"
practice_question_file = "practice_question.csv"
correctness_rate_file = "correctness_rate.csv"
check_answer_count_file = "check_answer_count.csv"

users = ["Sherry_Ruan", "Jeongeun_Park", "Shuo_Han",
         "Jackie_Yang", "Yunan_Xu", "Xuebing_Leng", "Zhiyuan_Lin", "Jerry_Hong",
         "Emma_Chen", "Iris_Lian", "Alice_Wang", "Irene_Lai", "Wenjing_Yan",
         "Jackie_Hang", "Yun_Zhang", "Kebing_Li", "Heidi_He", "Anna_Yu",
         "Yin_Li", "Ran_Gong", "Qiwen_Zhang", "Tianshi_Li",
         "Yiran_Shen", "Wendy_Li", "Wenming_Zhang",
         "Mkhanyisi_Gamedze", "Meng_Tang", "Miao_Zhang", "Fangjie_Cao",
         "Harry_Liu", "Tenaer_Yin", "Hao_Chen", "Ziang_Zhu",
         "Akemi_Wijayabahu", "Hongyu_Zhai", "Wenxiao_Huang",
         "Yibing_Du", "Haihong_Li", "Yifan_He", "Mingchen_Li",
         "Ramon_Tuason", "Hanke_Gu"]

# a dictionary of the number of times user studied each question
practice_question_count = {}

# a dictionary of the correctness rate of each question
question_correctness_rate = {}

# qid of all 96 questions appeared in either quiz a or quiz b
all_appeared_question_qid = [1, 2, 3, 5, 6, 8, 9, 10, 11, 14, 15, 17, 18, 19, 21, 24, 25, 27, 29, 30, 31, 32, 35, 37, 38, 40, 41, 42, 44, 45, 46, 49, 50, 51, 52, 53, 55, 56, 58, 59, 64, 65, 68, 70, 72, 73, 74, 75, 76, 77, 79, 82, 83, 84, 85, 87, 88, 89, 90, 92, 93, 94, 97, 99, 100, 102, 103, 104, 106, 111, 112, 113, 114, 117, 118, 120, 121, 125, 127, 128, 130, 131, 132, 133, 135, 136, 138, 139, 141, 142, 143, 144, 145, 146, 147, 148]

qid_96 = [148, 49, 18, 111, 6, 51, 93, 94, 102, 21, 128, 82, 135, 114, 146, 113, 131, 41, 55, 37, 52, 58, 11, 64, 14, 88, 84, 103, 90, 32, 117, 136, 31, 44, 132, 45, 42, 76, 104, 53, 72, 5, 15, 100, 27, 65, 35, 138, 125, 127, 99, 46, 75, 79, 25, 145, 118, 24, 1, 130, 19, 83, 59, 50, 17, 30, 56, 120, 141, 73, 38, 143, 147, 8, 2, 121, 68, 9, 77, 106, 97, 112, 89, 29, 133, 87, 3, 10, 40, 70, 74, 85, 92, 139, 142, 144]
qualtrics_id_96 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97]

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

question_check_answer_count = {
                             'Jeongeun_Park': {128: 5, 130: 4, 131: 4, 133: 4, 6: 4, 135: 4, 9: 4, 10: 4, 11: 5, 141: 4, 142: 5, 15: 5, 144: 5, 145: 4, 18: 4, 3: 4, 148: 4, 24: 5, 29: 6, 37: 6, 40: 4, 41: 2, 44: 5, 46: 5, 49: 6, 51: 10, 52: 5, 55: 8, 56: 6, 58: 8, 59: 9, 73: 5, 75: 4, 76: 4, 77: 4, 83: 7, 88: 4, 89: 4, 90: 4, 92: 2, 99: 7, 102: 4, 17: 3, 104: 4, 106: 4, 111: 4, 113: 4, 114: 5},
                             'Shuo_Han': {128: 5, 130: 4, 131: 4, 133: 4, 6: 6, 135: 9, 9: 4, 10: 4, 11: 4, 141: 7, 142: 4, 15: 6, 144: 4, 145: 3, 18: 4, 3: 4, 148: 4, 24: 4, 29: 7, 37: 3, 40: 6, 41: 4, 44: 4, 46: 4, 49: 4, 51: 8, 52: 7, 55: 11, 56: 6, 58: 5, 59: 4, 73: 4, 75: 4, 76: 4, 77: 4, 83: 4, 88: 9, 89: 4, 90: 5, 92: 4, 99: 5, 102: 4, 17: 4, 104: 4, 106: 8, 111: 6, 113: 4, 114: 4},
                             'Harry_Liu': {128: 5, 130: 2, 131: 4, 133: 7, 6: 4, 135: 4, 9: 5, 10: 6, 11: 5, 141: 2, 142: 3, 15: 2, 144: 5, 145: 4, 18: 3, 3: 3, 148: 5, 24: 2, 29: 3, 37: 4, 40: 5, 41: 4, 44: 3, 46: 3, 49: 3, 51: 1, 52: 2, 55: 1, 56: 7, 58: 11, 59: 5, 73: 3, 75: 3, 76: 1, 77: 2, 83: 3, 88: 3, 89: 4, 90: 2, 92: 3, 99: 2, 102: 5, 17: 2, 104: 4, 106: 8, 111: 4, 113: 4, 114: 3},
                             'Yunan_Xu': {128: 4, 130: 4, 131: 7, 133: 5, 6: 5, 135: 7, 9: 3, 10: 4, 11: 3, 141: 3, 142: 4, 15: 4, 144: 7, 145: 3, 18: 3, 3: 3, 148: 4, 24: 3, 29: 3, 37: 3, 40: 3, 41: 3, 44: 4, 46: 3, 49: 3, 51: 2, 52: 4, 55: 4, 56: 4, 58: 4, 59: 5, 73: 5, 75: 4, 76: 4, 77: 4, 83: 9, 88: 3, 89: 4, 90: 5, 92: 3, 99: 4, 102: 4, 17: 4, 104: 4, 106: 5, 111: 4, 113: 3, 114: 4},
                             'Jackie_Yang': {128: 6, 130: 5, 131: 6, 133: 6, 6: 5, 135: 6, 9: 8, 10: 5, 11: 4, 141: 4, 142: 4, 15: 3, 144: 8, 145: 5, 18: 3, 3: 3, 148: 9, 24: 8, 29: 4, 37: 3, 40: 5, 41: 7, 44: 4, 46: 6, 49: 6, 51: 6, 52: 5, 55: 9, 56: 4, 58: 7, 59: 6, 73: 5, 75: 3, 76: 3, 77: 3, 83: 8, 88: 7, 89: 3, 90: 8, 92: 4, 99: 5, 102: 4, 17: 4, 104: 3, 106: 9, 111: 5, 113: 9, 114: 6},
                             'Xuebing_Leng': {128: 4, 130: 3, 131: 4, 133: 4, 6: 3, 135: 3, 9: 5, 10: 4, 11: 4, 141: 3, 142: 3, 15: 5, 144: 4, 145: 4, 18: 3, 3: 4, 148: 4, 24: 3, 29: 4, 37: 4, 40: 3, 41: 4, 44: 4, 46: 4, 49: 4, 51: 4, 52: 2, 55: 4, 56: 4, 58: 2, 59: 3, 73: 4, 75: 4, 76: 3, 77: 4, 83: 4, 88: 4, 89: 11, 90: 4, 92: 4, 99: 2, 102: 3, 17: 3, 104: 4, 106: 3, 111: 3, 113: 4, 114: 4},
                             'Zhiyuan_Lin': {128: 5, 130: 3, 131: 5, 133: 7, 6: 4, 135: 6, 9: 2, 10: 5, 11: 4, 141: 5, 142: 5, 15: 5, 144: 6, 145: 9, 18: 3, 3: 4, 148: 7, 24: 4, 29: 5, 37: 4, 40: 9, 41: 3, 44: 5, 46: 4, 49: 4, 51: 4, 52: 2, 55: 12, 56: 4, 58: 4, 59: 5, 73: 4, 75: 4, 76: 5, 77: 3, 83: 6, 88: 3, 89: 5, 90: 5, 92: 7, 99: 4, 102: 4, 17: 3, 104: 7, 106: 3, 111: 3, 113: 6, 114: 5},
                             'Jerry_Hong': {128: 4, 130: 3, 131: 4, 133: 3, 6: 2, 135: 3, 9: 7, 10: 4, 11: 4, 141: 4, 142: 4, 15: 3, 144: 4, 145: 3, 18: 4, 3: 4, 148: 4, 24: 2, 29: 6, 37: 4, 40: 3, 41: 4, 44: 2, 46: 4, 49: 3, 51: 2, 52: 3, 55: 3, 56: 3, 58: 3, 59: 5, 73: 4, 75: 4, 76: 3, 77: 3, 83: 4, 88: 4, 89: 5, 90: 3, 92: 4, 99: 3, 102: 4, 17: 2, 104: 4, 106: 4, 111: 3, 113: 5, 114: 3},
                             'Kebing_Li': {128: 5, 130: 5, 131: 3, 133: 4, 6: 6, 135: 6, 9: 4, 10: 6, 11: 3, 141: 4, 142: 5, 15: 6, 144: 3, 145: 4, 18: 4, 3: 5, 148: 4, 24: 5, 29: 4, 37: 4, 40: 6, 41: 3, 44: 4, 46: 7, 49: 4, 51: 2, 52: 4, 55: 6, 56: 3, 58: 2, 59: 5, 73: 4, 75: 4, 76: 4, 77: 6, 83: 4, 88: 3, 89: 4, 90: 4, 92: 6, 99: 1, 102: 4, 17: 4, 104: 6, 106: 5, 111: 3, 113: 4, 114: 4},
                             'Yun_Zhang': {128: 4, 130: 4, 131: 4, 133: 4, 6: 3, 135: 4, 9: 4, 10: 3, 11: 4, 141: 4, 142: 4, 15: 2, 144: 3, 145: 4, 18: 3, 3: 5, 148: 4, 24: 3, 29: 4, 37: 8, 40: 3, 41: 6, 44: 4, 46: 7, 49: 4, 51: 4, 52: 4, 55: 3, 56: 4, 58: 2, 59: 6, 73: 4, 75: 2, 76: 4, 77: 4, 83: 2, 88: 4, 89: 4, 90: 2, 92: 4, 99: 2, 102: 4, 17: 5, 104: 4, 106: 5, 111: 3, 113: 4, 114: 5},
                             'Alice_Wang': {128: 3, 130: 5, 131: 9, 133: 4, 6: 3, 135: 7, 9: 4, 10: 3, 11: 5, 141: 4, 142: 4, 15: 2, 144: 5, 145: 4, 18: 3, 3: 4, 148: 5, 24: 3, 29: 5, 37: 3, 40: 4, 41: 6, 44: 4, 46: 7, 49: 4, 51: 5, 52: 3, 55: 6, 56: 4, 58: 6, 59: 6, 73: 4, 75: 4, 76: 3, 77: 3, 83: 5, 88: 4, 89: 2, 90: 4, 92: 4, 99: 3, 102: 3, 17: 4, 104: 4, 106: 4, 111: 7, 113: 6, 114: 4},
                             'Iris_Lian': {128: 2, 130: 4, 131: 5, 133: 5, 6: 4, 135: 5, 9: 5, 10: 4, 11: 5, 141: 7, 142: 4, 15: 14, 144: 5, 145: 5, 18: 4, 3: 4, 148: 4, 24: 7, 29: 4, 37: 6, 40: 4, 41: 2, 44: 3, 46: 4, 49: 3, 51: 4, 52: 4, 55: 5, 56: 5, 58: 6, 59: 4, 73: 5, 75: 4, 76: 4, 77: 4, 83: 4, 88: 4, 89: 4, 90: 4, 92: 6, 99: 4, 102: 4, 17: 4, 104: 4, 106: 5, 111: 4, 113: 4, 114: 4},
                             'Jackie_Hang': {128: 4, 130: 4, 131: 4, 133: 3, 6: 3, 135: 3, 9: 5, 10: 4, 11: 3, 141: 3, 142: 4, 15: 9, 144: 4, 145: 4, 18: 4, 3: 3, 148: 5, 24: 3, 29: 4, 37: 4, 40: 4, 41: 4, 44: 5, 46: 4, 49: 3, 51: 8, 52: 4, 55: 5, 56: 4, 58: 5, 59: 3, 73: 4, 75: 4, 76: 4, 77: 4, 83: 5, 88: 4, 89: 3, 90: 4, 92: 4, 99: 6, 102: 4, 17: 4, 104: 4, 106: 4, 111: 4, 113: 6, 114: 7},
                             'Heidi_He': {128: 5, 130: 3, 131: 9, 133: 4, 6: 3, 135: 4, 9: 18, 10: 4, 11: 4, 141: 4, 142: 4, 15: 6, 144: 3, 145: 5, 18: 3, 3: 4, 148: 4, 24: 5, 29: 5, 37: 4, 40: 3, 41: 4, 44: 5, 46: 4, 49: 5, 51: 10, 52: 4, 55: 14, 56: 4, 58: 1, 59: 8, 73: 5, 75: 4, 76: 5, 77: 3, 83: 6, 88: 4, 89: 5, 90: 5, 92: 7, 99: 7, 102: 4, 17: 5, 104: 5, 106: 6, 111: 4, 113: 7, 114: 4},
                             'Anna_Yu': {128: 6, 130: 4, 131: 4, 133: 3, 6: 5, 135: 3, 9: 7, 10: 5, 11: 5, 141: 4, 142: 4, 15: 6, 144: 4, 145: 4, 18: 4, 3: 4, 148: 3, 24: 15, 29: 5, 37: 5, 40: 6, 41: 4, 44: 4, 46: 3, 49: 4, 51: 6, 52: 5, 55: 4, 56: 4, 58: 5, 59: 5, 73: 4, 75: 4, 76: 4, 77: 4, 83: 4, 88: 4, 89: 4, 90: 4, 92: 4, 99: 4, 102: 5, 17: 5, 104: 3, 106: 2, 111: 3, 113: 5, 114: 5},
                             'Irene_Lai': {128: 4, 130: 5, 131: 4, 133: 2, 6: 4, 135: 3, 9: 4, 10: 4, 11: 4, 141: 4, 142: 4, 15: 5, 144: 4, 145: 4, 18: 2, 3: 4, 148: 4, 24: 4, 29: 4, 37: 4, 40: 4, 41: 4, 44: 4, 46: 4, 49: 4, 51: 3, 52: 3, 55: 4, 56: 4, 58: 2, 59: 4, 73: 4, 75: 4, 76: 0, 77: 4, 83: 4, 88: 3, 89: 4, 90: 4, 92: 4, 99: 2, 102: 3, 17: 4, 104: 4, 106: 3, 111: 5, 113: 2, 114: 4},
                             'Qiwen_Zhang': {128: 5, 130: 3, 131: 6, 133: 8, 6: 4, 135: 3, 9: 5, 10: 4, 11: 4, 141: 7, 142: 4, 15: 3, 144: 4, 145: 4, 18: 3, 3: 3, 148: 4, 24: 3, 29: 4, 37: 3, 40: 4, 41: 4, 44: 3, 46: 4, 49: 4, 51: 3, 52: 4, 55: 6, 56: 4, 58: 5, 59: 3, 73: 5, 75: 4, 76: 4, 77: 2, 83: 6, 88: 4, 89: 4, 90: 4, 92: 5, 99: 3, 102: 4, 17: 5, 104: 5, 106: 4, 111: 4, 113: 3, 114: 5},
                             'Ran_Gong': {128: 4, 130: 4, 131: 9, 133: 5, 6: 7, 135: 7, 9: 7, 10: 4, 11: 5, 141: 6, 142: 4, 15: 6, 144: 4, 145: 5, 18: 3, 3: 4, 148: 5, 24: 6, 29: 5, 37: 4, 40: 7, 41: 4, 44: 5, 46: 7, 49: 5, 51: 13, 52: 4, 55: 10, 56: 12, 58: 4, 59: 5, 73: 3, 75: 4, 76: 4, 77: 5, 83: 11, 88: 8, 89: 5, 90: 5, 92: 5, 99: 5, 102: 6, 17: 4, 104: 8, 106: 6, 111: 6, 113: 6, 114: 6},
                             'Tianshi_Li': {128: 7, 130: 6, 131: 7, 133: 4, 6: 3, 135: 3, 9: 3, 10: 8, 11: 6, 141: 4, 142: 4, 15: 4, 144: 6, 145: 7, 18: 4, 3: 6, 148: 7, 24: 6, 29: 7, 37: 6, 40: 4, 41: 6, 44: 4, 46: 7, 49: 5, 51: 5, 52: 2, 55: 11, 56: 6, 58: 8, 59: 11, 73: 7, 75: 6, 76: 5, 77: 5, 83: 6, 88: 6, 89: 5, 90: 6, 92: 5, 99: 6, 102: 4, 17: 5, 104: 5, 106: 5, 111: 7, 113: 6, 114: 4},
                             'Wenjing_Yan': {128: 4, 130: 4, 131: 6, 133: 4, 6: 6, 135: 4, 9: 4, 10: 4, 11: 5, 141: 5, 142: 3, 15: 11, 144: 4, 145: 4, 18: 4, 3: 6, 148: 6, 24: 6, 29: 5, 37: 7, 40: 10, 41: 4, 44: 4, 46: 7, 49: 6, 51: 5, 52: 6, 55: 5, 56: 5, 58: 0, 59: 3, 73: 3, 75: 4, 76: 5, 77: 4, 83: 5, 88: 4, 89: 3, 90: 4, 92: 4, 99: 5, 102: 5, 17: 5, 104: 5, 106: 4, 111: 4, 113: 4, 114: 6},
                             'Yin_Li': {128: 2, 130: 1, 131: 2, 133: 1, 6: 3, 135: 3, 9: 4, 10: 2, 11: 3, 141: 2, 142: 2, 15: 1, 144: 2, 145: 2, 18: 5, 3: 4, 148: 0, 24: 5, 29: 9, 37: 2, 40: 2, 41: 2, 44: 2, 46: 2, 49: 5, 51: 5, 52: 4, 55: 6, 56: 5, 58: 3, 59: 1, 73: 3, 75: 3, 76: 3, 77: 3, 83: 3, 88: 5, 89: 3, 90: 5, 92: 3, 99: 2, 102: 2, 17: 3, 104: 0, 106: 2, 111: 2, 113: 0, 114: 2},
                             'Harry_Liu': {128: 5, 130: 2, 131: 4, 133: 7, 6: 4, 135: 4, 9: 5, 10: 6, 11: 5, 141: 2, 142: 3, 15: 2, 144: 5, 145: 4, 18: 3, 3: 3, 148: 5, 24: 2, 29: 3, 37: 4, 40: 5, 41: 4, 44: 3, 46: 3, 49: 3, 51: 1, 52: 2, 55: 1, 56: 7, 58: 11, 59: 5, 73: 3, 75: 3, 76: 1, 77: 2, 83: 3, 88: 3, 89: 4, 90: 2, 92: 3, 99: 2, 102: 5, 17: 2, 104: 4, 106: 8, 111: 4, 113: 4, 114: 3},
                             'Wendy_Li': {128: 4, 130: 4, 131: 4, 133: 4, 6: 4, 135: 3, 9: 4, 10: 5, 11: 4, 141: 4, 142: 4, 15: 4, 144: 4, 145: 5, 18: 4, 3: 4, 148: 4, 24: 3, 29: 4, 37: 4, 40: 4, 41: 4, 44: 3, 46: 5, 49: 4, 51: 6, 52: 0, 55: 4, 56: 5, 58: 5, 59: 4, 73: 4, 75: 3, 76: 4, 77: 2, 83: 2, 88: 4, 89: 3, 90: 4, 92: 5, 99: 3, 102: 4, 17: 3, 104: 4, 106: 3, 111: 4, 113: 6, 114: 5},
                             'Wenming_Zhang': {128: 5, 130: 4, 131: 5, 133: 7, 6: 3, 135: 4, 9: 4, 10: 3, 11: 4, 141: 7, 142: 7, 15: 3, 144: 5, 145: 6, 18: 4, 3: 3, 148: 3, 24: 6, 29: 3, 37: 3, 40: 3, 41: 3, 44: 4, 46: 6, 49: 5, 51: 5, 52: 5, 55: 11, 56: 4, 58: 4, 59: 4, 73: 4, 75: 3, 76: 5, 77: 2, 83: 4, 88: 5, 89: 4, 90: 4, 92: 4, 99: 4, 102: 3, 17: 4, 104: 7, 106: 10, 111: 3, 113: 6, 114: 10},
                             'Miao_Zhang': {128: 4, 130: 4, 131: 4, 133: 4, 6: 3, 135: 7, 9: 5, 10: 3, 11: 4, 141: 4, 142: 3, 15: 3, 144: 3, 145: 4, 18: 7, 3: 5, 148: 4, 24: 4, 29: 6, 37: 4, 40: 4, 41: 3, 44: 4, 46: 4, 49: 4, 51: 8, 52: 3, 55: 8, 56: 5, 58: 3, 59: 4, 73: 5, 75: 2, 76: 3, 77: 7, 83: 1, 88: 7, 89: 3, 90: 3, 92: 8, 99: 2, 102: 4, 17: 4, 104: 4, 106: 4, 111: 4, 113: 4, 114: 4},
                             'Fangjie_Cao': {128: 4, 130: 3, 131: 5, 133: 5, 6: 3, 135: 3, 9: 4, 10: 4, 11: 4, 141: 6, 142: 4, 15: 2, 144: 5, 145: 3, 18: 3, 3: 6, 148: 4, 24: 2, 29: 6, 37: 3, 40: 4, 41: 3, 44: 4, 46: 4, 49: 4, 51: 5, 52: 2, 55: 6, 56: 4, 58: 4, 59: 7, 73: 3, 75: 3, 76: 4, 77: 4, 83: 3, 88: 3, 89: 3, 90: 4, 92: 6, 99: 4, 102: 3, 17: 2, 104: 4, 106: 4, 111: 4, 113: 4, 114: 4},
                             'Meng_Tang': {128: 5, 130: 5, 131: 5, 133: 5, 6: 4, 135: 6, 9: 3, 10: 9, 11: 4, 141: 5, 142: 5, 15: 4, 144: 5, 145: 5, 18: 4, 3: 4, 148: 5, 24: 5, 29: 4, 37: 4, 40: 4, 41: 4, 44: 4, 46: 5, 49: 6, 51: 10, 52: 7, 55: 14, 56: 5, 58: 3, 59: 3, 73: 4, 75: 4, 76: 3, 77: 2, 83: 5, 88: 4, 89: 4, 90: 4, 92: 5, 99: 3, 102: 4, 17: 5, 104: 4, 106: 3, 111: 5, 113: 4, 114: 4},
                             'Tenaer_Yin': {128: 4, 130: 4, 131: 4, 133: 4, 6: 4, 135: 3, 9: 3, 10: 5, 11: 4, 141: 4, 142: 4, 15: 5, 144: 4, 145: 5, 18: 4, 3: 4, 148: 4, 24: 3, 29: 3, 37: 4, 40: 4, 41: 5, 44: 4, 46: 4, 49: 4, 51: 3, 52: 3, 55: 3, 56: 6, 58: 4, 59: 4, 73: 4, 75: 4, 76: 5, 77: 4, 83: 4, 88: 4, 89: 4, 90: 4, 92: 4, 99: 4, 102: 4, 17: 4, 104: 2, 106: 5, 111: 4, 113: 4, 114: 4},
                             'Yiran_Shen': {128: 4, 130: 5, 131: 4, 133: 3, 6: 5, 135: 3, 9: 4, 10: 3, 11: 3, 141: 4, 142: 3, 15: 3, 144: 4, 145: 4, 18: 3, 3: 3, 148: 3, 24: 4, 29: 4, 37: 3, 40: 2, 41: 3, 44: 3, 46: 3, 49: 3, 51: 5, 52: 4, 55: 5, 56: 4, 58: 4, 59: 3, 73: 3, 75: 3, 76: 4, 77: 4, 83: 3, 88: 4, 89: 4, 90: 3, 92: 3, 99: 4, 102: 5, 17: 4, 104: 4, 106: 5, 111: 4, 113: 4, 114: 4},
                             'Ziang_Zhu': {128: 5, 130: 4, 131: 5, 133: 5, 6: 4, 135: 4, 9: 4, 10: 3, 11: 4, 141: 4, 142: 8, 15: 3, 144: 3, 145: 4, 18: 3, 3: 3, 148: 3, 24: 6, 29: 3, 37: 3, 40: 3, 41: 4, 44: 3, 46: 4, 49: 3, 51: 2, 52: 2, 55: 2, 56: 2, 58: 1, 59: 2, 73: 2, 75: 2, 76: 2, 77: 2, 83: 2, 88: 2, 89: 2, 90: 2, 92: 2, 99: 2, 102: 5, 17: 3, 104: 2, 106: 4, 111: 4, 113: 4, 114: 4},
                             'Hao_Chen': {128: 2, 130: 4, 131: 2, 133: 3, 6: 4, 135: 4, 9: 3, 10: 3, 11: 4, 141: 4, 142: 4, 15: 2, 144: 3, 145: 4, 18: 4, 3: 6, 148: 4, 24: 2, 29: 3, 37: 4, 40: 2, 41: 6, 44: 3, 46: 3, 49: 4, 51: 3, 52: 4, 55: 9, 56: 3, 58: 2, 59: 2, 73: 4, 75: 3, 76: 4, 77: 4, 83: 4, 88: 4, 89: 4, 90: 4, 92: 3, 99: 5, 102: 5, 17: 1, 104: 4, 106: 6, 111: 2, 113: 4, 114: 4},
                             'Akemi_Wijayabahu': {128: 6, 130: 4, 131: 4, 133: 4, 6: 4, 135: 3, 9: 5, 10: 4, 11: 3, 141: 5, 142: 6, 15: 4, 144: 4, 145: 4, 18: 4, 3: 4, 148: 5, 24: 3, 29: 5, 37: 4, 40: 2, 41: 3, 44: 4, 46: 4, 49: 6, 51: 4, 52: 3, 55: 3, 56: 3, 58: 4, 59: 4, 73: 4, 75: 4, 76: 4, 77: 4, 83: 4, 88: 5, 89: 5, 90: 5, 92: 5, 99: 4, 102: 4, 17: 4, 104: 4, 106: 5, 111: 5, 113: 5, 114: 5},
                             'Yifan_He': {128: 2, 130: 2, 131: 2, 133: 2, 6: 4, 135: 4, 9: 4, 10: 1, 11: 3, 141: 2, 142: 2, 15: 2, 144: 2, 145: 2, 18: 3, 3: 2, 148: 2, 24: 3, 29: 4, 37: 3, 40: 3, 41: 3, 44: 3, 46: 3, 49: 3, 51: 5, 52: 2, 55: 2, 56: 5, 58: 2, 59: 3, 73: 2, 75: 2, 76: 2, 77: 3, 83: 2, 88: 4, 89: 2, 90: 2, 92: 3, 99: 2, 102: 2, 17: 4, 104: 2, 106: 2, 111: 2, 113: 2, 114: 2},
                             'Hongyu_Zhai': {128: 5, 130: 9, 131: 5, 133: 9, 6: 5, 135: 5, 9: 7, 10: 5, 11: 4, 141: 7, 142: 8, 15: 4, 144: 3, 145: 7, 18: 6, 3: 7, 148: 7, 24: 8, 29: 6, 37: 4, 40: 12, 41: 7, 44: 5, 46: 9, 49: 7, 51: 10, 52: 8, 55: 7, 56: 7, 58: 2, 59: 6, 73: 18, 75: 6, 76: 8, 77: 5, 83: 17, 88: 8, 89: 5, 90: 12, 92: 11, 99: 8, 102: 5, 17: 5, 104: 10, 106: 7, 111: 5, 113: 8, 114: 8},
                             'Yibing_Du': {128: 4, 130: 4, 131: 2, 133: 4, 6: 5, 135: 3, 9: 4, 10: 3, 11: 3, 141: 4, 142: 3, 15: 4, 144: 3, 145: 5, 18: 3, 3: 3, 148: 4, 24: 4, 29: 4, 37: 3, 40: 4, 41: 3, 44: 3, 46: 4, 49: 3, 51: 4, 52: 3, 55: 6, 56: 3, 58: 4, 59: 5, 73: 4, 75: 4, 76: 4, 77: 3, 83: 3, 88: 4, 89: 3, 90: 4, 92: 5, 99: 4, 102: 4, 17: 3, 104: 2, 106: 4, 111: 3, 113: 7, 114: 3},
                             'Mkhanyisi_Gamedze': {128: 4, 130: 4, 131: 3, 133: 1, 6: 5, 135: 3, 9: 3, 10: 3, 11: 4, 141: 4, 142: 5, 15: 5, 144: 3, 145: 3, 18: 3, 3: 4, 148: 6, 24: 5, 29: 6, 37: 3, 40: 5, 41: 4, 44: 5, 46: 3, 49: 3, 51: 4, 52: 4, 55: 6, 56: 3, 58: 4, 59: 5, 73: 4, 75: 2, 76: 5, 77: 4, 83: 4, 88: 4, 89: 4, 90: 5, 92: 2, 99: 4, 102: 4, 17: 3, 104: 4, 106: 5, 111: 4, 113: 4, 114: 5},
                             'Haihong_Li': {128: 5, 130: 3, 131: 0, 133: 3, 6: 3, 135: 2, 9: 3, 10: 4, 11: 4, 141: 3, 142: 3, 15: 3, 144: 3, 145: 3, 18: 4, 3: 4, 148: 3, 24: 8, 29: 4, 37: 5, 40: 4, 41: 5, 44: 4, 46: 6, 49: 3, 51: 6, 52: 5, 55: 2, 56: 4, 58: 3, 59: 5, 73: 4, 75: 4, 76: 3, 77: 3, 83: 10, 88: 2, 89: 3, 90: 3, 92: 5, 99: 3, 102: 1, 17: 3, 104: 3, 106: 4, 111: 4, 113: 4, 114: 4},
                             'Wenxiao_Huang': {128: 5, 130: 4, 131: 3, 133: 7, 6: 4, 135: 5, 9: 4, 10: 4, 11: 4, 141: 4, 142: 5, 15: 3, 144: 4, 145: 7, 18: 4, 3: 4, 148: 4, 24: 4, 29: 4, 37: 5, 40: 5, 41: 5, 44: 5, 46: 5, 49: 3, 51: 4, 52: 4, 55: 8, 56: 4, 58: 4, 59: 4, 73: 4, 75: 4, 76: 4, 77: 4, 83: 5, 88: 4, 89: 4, 90: 4, 92: 5, 99: 5, 102: 4, 17: 4, 104: 6, 106: 4, 111: 4, 113: 3, 114: 4},
                             'Mingchen_Li': {128: 4, 130: 4, 131: 4, 133: 4, 6: 3, 135: 3, 9: 4, 10: 4, 11: 4, 141: 4, 142: 4, 15: 2, 144: 4, 145: 3, 18: 6, 3: 2, 148: 4, 24: 4, 29: 2, 37: 3, 40: 4, 41: 4, 44: 5, 46: 4, 49: 4, 51: 6, 52: 5, 55: 7, 56: 4, 58: 4, 59: 4, 73: 4, 75: 5, 76: 4, 77: 4, 83: 2, 88: 4, 89: 5, 90: 5, 92: 4, 99: 3, 102: 4, 17: 4, 104: 4, 106: 4, 111: 2, 113: 6, 114: 4},
                             'Ramon_Tuason': {128: 4, 130: 3, 131: 4, 133: 4, 6: 3, 135: 4, 9: 4, 10: 4, 11: 4, 141: 4, 142: 5, 15: 4, 144: 3, 145: 4, 18: 4, 3: 4, 148: 4, 24: 3, 29: 3, 37: 3, 40: 3, 41: 4, 44: 5, 46: 4, 49: 4, 51: 5, 52: 4, 55: 4, 56: 4, 58: 4, 59: 4, 73: 4, 75: 5, 76: 4, 77: 4, 83: 4, 88: 4, 89: 4, 90: 5, 92: 5, 99: 5, 102: 4, 17: 3, 104: 4, 106: 4, 111: 4, 113: 5, 114: 4},
                             'Hanke_Gu': {128: 3, 130: 3, 131: 8, 133: 6, 6: 4, 135: 1, 9: 4, 10: 4, 11: 4, 141: 4, 142: 5, 15: 3, 144: 4, 145: 3, 18: 3, 3: 3, 148: 4, 24: 3, 29: 3, 37: 4, 40: 4, 41: 4, 44: 5, 46: 4, 49: 5, 51: 5, 52: 3, 55: 4, 56: 4, 58: 4, 59: 4, 73: 4, 75: 5, 76: 5, 77: 3, 83: 6, 88: 4, 89: 3, 90: 4, 92: 4, 99: 2, 102: 5, 17: 3, 104: 2, 106: 3, 111: 3, 113: 7, 114: 5},
                             'Emma_Chen': {128: 6, 130: 5, 131: 6, 133: 5, 6: 4, 135: 4, 9: 2, 10: 5, 11: 4, 141: 4, 142: 5, 15: 2, 144: 4, 145: 4, 18: 4, 3: 5, 148: 6, 24: 5, 29: 4, 37: 5, 40: 3, 41: 4, 44: 5, 46: 4, 49: 4, 51: 4, 52: 3, 55: 6, 56: 4, 58: 3, 59: 6, 73: 4, 75: 4, 76: 2, 77: 4, 83: 4, 88: 4, 89: 4, 90: 4, 92: 5, 99: 5, 102: 4, 17: 4, 104: 7, 106: 5, 111: 4, 113: 5, 114: 5}}


users = question_check_answer_count.keys()

# time break considered to be a leave
BREAK_TIME = 30
QUESTION_BREAK_TIME = 200
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
    total_effective_usage_time = 0  # counter of total effective usage time
    joke_fun_fact_time = 0

    sender = conversation_file[0][SENDER_INDEX]
    recipient = conversation_file[0][RECIPIENT_INDEX]
    old_time_stamp = conversation_file[0][TIME_STAMP_INDEX]
    old_time_stamp = datetime.strptime(old_time_stamp, "%Y-%m-%d %H:%M:%S")
    old_time_stamp = old_time_stamp.replace(tzinfo=tz.gettz('UTC'))
    old_time_stamp = old_time_stamp.astimezone(tz.gettz('America/Los_Angeles'))
    old_time_stamp_uid = 0

    question_start_uid = -99999999
    if conversation_file[0][TYPE_INDEX] == "user_quick_reply: NEXT_QUESTION":
        question_start_uid = 0
        start_effective_time_stamp = conversation_file[0][TIME_STAMP_INDEX]
        start_effective_time_stamp = datetime.strptime(start_effective_time_stamp, "%Y-%m-%d %H:%M:%S")
        start_effective_time_stamp = start_effective_time_stamp.replace(tzinfo=tz.gettz('UTC'))
        start_effective_time_stamp = start_effective_time_stamp.astimezone(tz.gettz('America/Los_Angeles'))


    joke_fun_fact_start_uid = -99999999
    if conversation_file[0][TYPE_INDEX] == "user_quick_reply: JOKE" or conversation_file[0][TYPE_INDEX][0:26] == "user_quick_reply: FUN_FACT":
        joke_fun_fact_start_uid = 0
        start_joke_fun_fact_time_stamp = conversation_file[0][TIME_STAMP_INDEX]
        start_joke_fun_fact_time_stamp = datetime.strptime(start_joke_fun_fact_time_stamp, "%Y-%m-%d %H:%M:%S")
        start_joke_fun_fact_time_stamp = start_joke_fun_fact_time_stamp.replace(tzinfo=tz.gettz('UTC'))
        start_joke_fun_fact_time_stamp = start_joke_fun_fact_time_stamp.astimezone(tz.gettz('America/Los_Angeles'))

    for i in range(1, len(conversation_file)):
        time_stamp = conversation_file[i][TIME_STAMP_INDEX]
        time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
        time_stamp = time_stamp.replace(tzinfo=tz.gettz('UTC'))
        time_stamp = time_stamp.astimezone(tz.gettz('America/Los_Angeles'))

        if (time_stamp.year, time_stamp.month, time_stamp.day) != (old_time_stamp.year, old_time_stamp.month, old_time_stamp.day):
            analysis.append([])
            day_counter += 1
            sub_time_report.append((old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60, total_effective_usage_time/60, joke_fun_fact_time/60))
            total_usage_time = 0
            total_effective_usage_time = 0
            question_start_uid = -99999999
            joke_fun_fact_time = 0
            joke_fun_fact_start_uid = -99999999
            new_time_stamp_uid = int(conversation_file[i][UID_INDEX])
            #print(old_time_stamp_uid, new_time_stamp_uid)
            sub_practice_report.append([int(x[QID_INDEX]) for x in user_history_file \
                                       if (x[END_UID_INDEX] != "" and int(x[END_UID_INDEX]) >= old_time_stamp_uid and int(x[END_UID_INDEX]) < new_time_stamp_uid)])
            old_time_stamp_uid = new_time_stamp_uid

        if conversation_file[i][TYPE_INDEX] == "user_quick_reply: NEXT_QUESTION":
            if (i - question_start_uid) < 14:
                if (time_stamp - start_effective_time_stamp).total_seconds() <= QUESTION_BREAK_TIME:
                    total_effective_usage_time += (time_stamp - start_effective_time_stamp).total_seconds()
            question_start_uid = i
            start_effective_time_stamp = conversation_file[i][TIME_STAMP_INDEX]
            start_effective_time_stamp = datetime.strptime(start_effective_time_stamp, "%Y-%m-%d %H:%M:%S")
            start_effective_time_stamp = start_effective_time_stamp.replace(tzinfo=tz.gettz('UTC'))
            start_effective_time_stamp = start_effective_time_stamp.astimezone(tz.gettz('America/Los_Angeles'))

        if conversation_file[0][TYPE_INDEX] == "user_quick_reply: JOKE" or conversation_file[0][TYPE_INDEX][0:26] == "user_quick_reply: FUN_FACT":
            if (time_stamp - start_joke_fun_fact_time_stamp).total_seconds() <= QUESTION_BREAK_TIME:
                    start_joke_fun_fact_time_stamp += (time_stamp - start_joke_fun_fact_time_stamp).total_seconds()
            joke_fun_fact_start_uid = i
            start_joke_fun_fact_time_stamp = conversation_file[i][TIME_STAMP_INDEX]
            start_joke_fun_fact_time_stamp = datetime.strptime(start_joke_fun_fact_time_stamp, "%Y-%m-%d %H:%M:%S")
            start_joke_fun_fact_time_stamp = start_joke_fun_fact_time_stamp.replace(tzinfo=tz.gettz('UTC'))
            start_joke_fun_fact_time_stamp = start_joke_fun_fact_time_stamp.astimezone(tz.gettz('America/Los_Angeles'))

        if (time_stamp - old_time_stamp).total_seconds() <= BREAK_TIME:
            total_usage_time += (time_stamp - old_time_stamp).total_seconds()
        old_time_stamp = time_stamp

    sub_time_report.append((old_time_stamp.year, old_time_stamp.month, old_time_stamp.day, total_usage_time/60, total_effective_usage_time/60, joke_fun_fact_time/60))
    # print(old_time_stamp_uid, new_time_stamp_uid)
    sub_practice_report.append([int(x[QID_INDEX]) for x in user_history_file if (x[END_UID_INDEX] != "" and int(x[END_UID_INDEX]) >= old_time_stamp_uid)])
    time_report[user] = sub_time_report
    practice_report[user] = sub_practice_report

    events = [int(x[QID_INDEX]) for x in user_history_file if x[END_UID_INDEX] != ""]
    # events = [int(x[QID_INDEX]) for x in user_history_file]
    print("\n------------")
    print(user)
    events.sort()
    print(events)
    print('Count: %d ' %len(events))

    events_correct = [int(x[QID_INDEX]) for x in user_history_file if x[END_UID_INDEX] != "" and int(x[SCORE_INDEX]) > 8]

    qid_in_postquiz_seen = set(events) & postquiz_qid
    qualtricsID_in_postquiz_seen = [qid_2_qualtricsID_dict[qid] for qid in qid_in_postquiz_seen]
    if events:
    	most_counts_qid, num_most_counts = Counter(events).most_common(1)[0]  # get question with most counts and the counts
    else:
        num_most_counts = 0
    question_report[user] = (len(events), len(set(events)), len(qid_in_postquiz_seen), qualtricsID_in_postquiz_seen, num_most_counts)

    # for q in quizbot_qid:
    #     practice_question_count[user][q] = events.count(q)
    # for q in quizbot_qid:
    #     if float(events.count(q)) == 0:
    #         question_correctness_rate[user][q] = ''
    #     else:
    #         question_correctness_rate[user][q] = round(float(events_correct.count(q)) / float(events.count(q)), 2)

    for qid in quizbot_qid:
        question_check_answer_count[user][qid] = 0

    for i in range(1,len(user_history_file)):
        if user_history_file[i][6] == "fill_in_the_blank":
            question_check_answer_count[user][int(user_history_file[i][3])] += 1


output_string = "\n"
for user in time_report:
    total_time = 0
    total_effective_time = 0
    joke_fun_fact_time = 0
    output_string += "----- "
    output_string += user
    output_string += " -----\n"

    for j, day_report in enumerate(time_report[user]):
        output_string += str(day_report[0])
        output_string += "."
        output_string += str(day_report[1])
        output_string += "."
        output_string += '{:02}'.format(day_report[2])
        output_string += ":{:>6.2f}".format(day_report[3])
        output_string += " min"
        output_string += " "*18
        output_string += str(len(practice_report[user][j])) + " -- "
        output_string += str(practice_report[user][j])
        output_string += "\n"
        total_time += day_report[3]
        total_effective_time += day_report[4]
        joke_fun_fact_time += day_report[5]
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
    output_string += "\n"
    output_string += "Total APP Effective Usage Time      : "
    output_string += str(round(total_effective_time, 2))
    output_string += " min"
    output_string += "\n"
    output_string += "Total APP Joke Fun Fact Time      : "
    output_string += str(round(joke_fun_fact_time, 2))
    output_string += " min"
    output_string += "\n\n"

f = open(result_filename, 'w')
f.write(output_string)
f.close()
print(output_string)

print(question_check_answer_count)

check_answer_count_file

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

all_question_correctness_rate = list(map(list, zip(*all_question_correctness_rate)))
with open(correctness_rate_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_question_correctness_rate)


all_question_check_answer_count = [['qid'] + qualtrics_id_96]

for user in question_check_answer_count.keys():
    check_answer_count = [question_check_answer_count[user][qid_96[i]] for i in range(len(qid_96))]
    check_answer_count.insert(0, user)
    all_question_check_answer_count.append(check_answer_count)

all_question_check_answer_count = list(map(list, zip(*all_question_check_answer_count)))
with open(check_answer_count_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_question_check_answer_count)

