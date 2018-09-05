import sys
sys.path.append("../")
sys.path.append("../question_sequencing")
import os
import json
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask_mysqldb import MySQL
import database as db
from random_model import RandomSequencingModel
from dash_model import DASHSequencingModel
from sequential_model import SequentialModel
from QAKnowledgebase import QAKnowlegeBase
from time import strftime, localtime, sleep
from utils import SubjectEnoughQuestions, EnoughForToday, FinishFixQuestionsStudy

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# ================== MySQL Setup ==================
mysql = MySQL()
app.config['MYSQL_HOST'] = os.environ["DB_HOST"]
app.config['MYSQL_USER'] = os.environ["DB_USER"]
app.config['MYSQL_PASSWORD'] = os.environ["DB_PASSWORD"]
app.config['MYSQL_DB'] = os.environ["DB"]
mysql.init_app(app)

# ================== 96 question pool ==================
# qid_to_index = {0: 15, 1: 135, 2: 55, 3: 51, 4: 56, 5: 141, 6: 128, 7: 106, 8: 111, 9: 114, 10: 59, 11: 9, 12: 131, 13: 145, 14: 18, 15: 102, 16: 11, 17: 133, 18: 130, 19: 83, 20: 41, 21: 148, 22: 75, 23: 90, 24: 99, 25: 113, 26: 104, 27: 46, 28: 37, 29: 44, 30: 49, 31: 58, 32: 24, 33: 52, 34: 73, 35: 6, 36: 29, 37: 88, 38: 17, 39: 76, 40: 77, 41: 89, 42: 144, 43: 142, 44: 92, 45: 10, 46: 3, 47: 40, 48: 147, 49: 100, 50: 138, 51: 118, 52: 112, 53: 64, 54: 32, 55: 50, 56: 136, 57: 143, 58: 121, 59: 132, 60: 120, 61: 8, 62: 5, 63: 30, 64: 117, 65: 125, 66: 14, 67: 103, 68: 19, 69: 27, 70: 84, 71: 93, 72: 79, 73: 72, 74: 2, 75: 31, 76: 42, 77: 35, 78: 65, 79: 25, 80: 1, 81: 21, 82: 38, 83: 97, 84: 94, 85: 53, 86: 45, 87: 82, 88: 87, 89: 127, 90: 146, 91: 68, 92: 139, 93: 85, 94: 74, 95: 70}
# qid_to_index = {v:k for (k,v) in qid_to_index.items()}

# # ================== quizbot 48 question pool ==================
# qid_to_index = {1: 32, 2: 26, 132: 11, 5: 14, 136: 8, 138: 2, 139: 44, 14: 18, 143: 9, 146: 42, 19: 20, 21: 33, 25: 31, 27: 21, 30: 15, 31: 27, 32: 6, 35: 29, 38: 34, 42: 28, 45: 38, 8: 13, 50: 7, 53: 37, 64: 5, 65: 30, 68: 43, 70: 47, 72: 25, 74: 46, 79: 24, 82: 39, 84: 22, 85: 45, 87: 40, 93: 23, 94: 36, 97: 35, 100: 1, 103: 19, 112: 4, 147: 0, 117: 16, 118: 3, 120: 12, 121: 10, 125: 17, 127: 41}

# ================== flashcard 48 question pool ==================
qid_to_index = {128: 6, 130: 18, 131: 12, 133: 17, 6: 35, 135: 1, 9: 11, 10: 45, 11: 16, 141: 5, 142: 43, 15: 0, 144: 42, 145: 13, 18: 14, 3: 46, 148: 21, 24: 32, 29: 36, 37: 28, 40: 47, 41: 20, 44: 29, 46: 27, 49: 30, 51: 3, 52: 33, 55: 2, 56: 4, 58: 31, 59: 10, 73: 34, 75: 22, 76: 39, 77: 40, 83: 19, 88: 37, 89: 41, 90: 23, 92: 44, 99: 24, 102: 15, 17: 38, 104: 26, 106: 7, 111: 8, 113: 25, 114: 9}

# ================== Batch 1+2 ==================
batch12_qa_kb = QAKnowlegeBase("../QAdataset/questions_filtered_150.json")
batch12_model = RandomSequencingModel(batch12_qa_kb)
batch12_user = {"871927094": "Yufeng Yin", "1085427761": "Jorge Nam", "1632": "3 3"}

# ================== Batch 4 ==================
json_file = '../QAdataset/questions_between_subjects_flashcard.json'  # sherry: typo here, should be within-subject
qa_kb = QAKnowlegeBase(json_file)
model = SequentialModel(qa_kb)

# ================== Batch 3 ==================
# json_file_within_subject = '../QAdataset/questions_between_subjects_flashcard.json'  # sherry: typo here, should be within-subject
# qa_kb_within_subject = QAKnowlegeBase(json_file_within_subject)
# model_within_subject = RandomSequencingModel(qa_kb_within_subject)


user_within_subject = { }
# "902902333": "Liwei Jiang"

user_finished_study = { #"379832172": "Anonymous Tester",
                        "239435253": "Giovanni Campagna", "1407190745": "Jean Coquet",
                        "50608053": "Philip Zhuang", "719675501": "Yue Hui",
                        "772553696": "Kylie Jue", "747757516": "De-An Huang",
                        "672579434": "Dee Dee Thao", "725315344": "Tyler Yep",
                        "1844410129": "Yinuo Yao", "1852193290": "Andrew Ying",
                        "2000946117": "jingyi li", "2079749432": "Jenn Hu",
                        "732119323": "Joy Yuzurih", "664942274": "Henry Qin",
                        "2137982794": "Nina Horowitz", "1689820842": "Daniel Do",
                        "1394174277": "Claire Yang",
                        "1515117469": "Olivia Yang", "1295547909": "Helen Wang",
                        "1237870507": 'Wangjianzhe Shao', "1732584014": "Francis Yan",
                        "361848411": "Flora Wang",
                        "1492552826": "Nathaniel Ramos",
                        "370456441": "Paul Walter", "434751492": "Clayton Ellington",
                        "994772346": "Maisam Pyarali", "1964037557": "Christine Liu",
                        "450648678": "Nathan Dalal", "466714361": "Sorathan Chaturapruek",
                        "1477638740": "Owen Wang",
                        "1163140404": "Richard Xu", "368141180": "Yang Wang",
                        "490809501": "Hongsheng Fang",
                        "102151122": "Michael Solorio", "678532179": "Nina Wei",
                        "798628431": "Jessica de la Paz",
                        "821967244": "Janice Zang",
                        "454995128": "Grace Hong", "420158298": "Daniel Choe"}
user_id_within_subject = list(user_within_subject.keys())


# ================== Messages sent to users ==================
enough_for_today_info = {'distractor': [], 'question': 'You already praciced enough questions today. Please wait until tomorrow to practice another session. Thank you!', 'support': 'NA', 'correct_answer': 'NA', 'qid': [-1, -1]}
enough_questions_info = {'distractor': [], 'question': 'You already practiced enough questions in this subject. Please try other two subjects.', 'support': 'NA', 'correct_answer': 'NA', 'qid': [-1, -1]}
finish_info = {'distractor': [], 'question': 'Thank you very much for using our app! You study is finished now and please proceed to the post-study surveys. Thank you!', 'support': 'NA', 'correct_answer': 'NA', 'qid': [-1, -1]}


with app.app_context():
    user_list = db.show_user_id_list_flashcard(mysql)
    for user_id in user_list:
        model.loadUserData(user_id, db.show_user_history_flashcard(mysql, user_id), qid_to_index)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/question_data", methods=['GET'])
def fetch_question():
    user_id = request.args.get('user_id')
    if user_id in user_within_subject:
        data = model_within_subject.pickNextQuestion(int(user_id), subject='random')
    elif user_id in user_finished_study:
        data = finish_info
    elif user_id in batch12_user.keys():
        print(batch12_user[user_id])
        data = batch12_model.pickNextQuestion(int(user_id), subject='random')
    else:
        try:
            data = model.pickNextQuestion(int(user_id), subject='random')
        except EnoughForToday:
            print("~~~~~ Enough for Today ~~~~~")
            data = enough_for_today_info
        except SubjectEnoughQuestions:
            print("~~~~~ Enough Questions ~~~~~")
            data = enough_questions_info
        except FinishFixQuestionsStudy:
            print("~~~~~ Finish Fix Question Study ~~~~~")
            data = finish_info
    return jsonify(data)


@app.route("/question_data_gre", methods=['GET'])
def fetch_question_gre():
    user_id = request.args.get('user_id')
    if user_id in user_within_subject:
        data = model_within_subject.pickNextQuestion(subject='gre')
    elif user_id in user_finished_study:
        data = finish_info
    elif user_id in batch12_user.keys():
        print(batch12_user[user_id])
        data = batch12_model.pickNextQuestion(int(user_id), subject='gre')
    else:
        try:
            data = model.pickNextQuestion(int(user_id), subject='gre')
        except EnoughForToday:
            print("~~~~~ Enough for Today ~~~~~")
            data = enough_for_today_info
        except SubjectEnoughQuestions:
            print("~~~~~ Enough Questions ~~~~~")
            data = enough_questions_info
        except FinishFixQuestionsStudy:
            print("~~~~~ Finish Fix Question Study ~~~~~")
            data = finish_info
    return jsonify(data)


@app.route("/question_data_science", methods=['GET'])
def fetch_question_science():
    user_id = request.args.get('user_id')
    if user_id in user_within_subject:
        data = model_within_subject.pickNextQuestion(subject='science')
    elif user_id in user_finished_study:
        data = finish_info
    elif user_id in batch12_user.keys():
        print(batch12_user[user_id])
        data = batch12_model.pickNextQuestion(int(user_id), subject='science')
    else:
        try:
            data = model.pickNextQuestion(int(user_id), subject='science')
        except EnoughForToday:
            print("~~~~~ Enough for Today ~~~~~")
            data = enough_for_today_info
        except SubjectEnoughQuestions:
            print("~~~~~ Enough Questions ~~~~~")
            data = enough_questions_info
        except FinishFixQuestionsStudy:
            print("~~~~~ Finish Fix Question Study ~~~~~")
            data = finish_info
    return jsonify(data)


@app.route("/question_data_safety", methods=['GET'])
def fetch_question_safety():
    user_id = request.args.get('user_id')
    if user_id in user_within_subject:
        data = model_within_subject.pickNextQuestion(subject='safety')
    elif user_id in user_finished_study:
        data = finish_info
    elif user_id in batch12_user.keys():
        print(batch12_user[user_id])
        data = batch12_model.pickNextQuestion(int(user_id), subject='safety')
    else:
        try:
            data = model.pickNextQuestion(int(user_id), subject='safety')
        except EnoughForToday:
            print("~~~~~ Enough for Today ~~~~~")
            data = enough_for_today_info
        except SubjectEnoughQuestions:
            print("~~~~~ Enough Questions ~~~~~")
            data = enough_questions_info
        except FinishFixQuestionsStudy:
            print("~~~~~ Finish Fix Question Study ~~~~~")
            data = finish_info
    return jsonify(data)


@app.route('/test', methods=['GET'])
def verify():
    print("received")
    return "test", 200


@app.route('/logdata', methods=['POST'])
def webhook():
    data=json.loads(request.data.decode("utf-8"))

    sender_id = data['user_id']
    qid = data['qid']
    user_action = data['event']

    if not int(sender_id) in db.show_user_id_list_flashcard(mysql):
        sender_firstname = data['firstname']
        sender_lastname = data['lastname']
        print("[FLASHCARD] PID " + str(os.getpid())+": This is a new user!")
        db.insert_user_flashcard(mysql, sender_id, sender_firstname, sender_lastname)

    db.insert_user_action_flashcard(mysql, sender_id, qid, user_action)

    # send user feedback to the question sequencing model
    if user_action == 'got it':
        print("got it")
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        # model.updateHistory(sender_id, (qid, 1, timestamp), qid_to_index)  # sherry: seems not working
    elif user_action == "I don't know":
        print("I don't know")
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        # model.updateHistory(sender_id, (qid, 0, timestamp), qid_to_index)  # sherry: seems not working

    #print("[FLASHCARD] PID " + str(os.getpid())+": Record FLASHCARD user action successfully")
    return "ok", 200


if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem', '/etc/letsencrypt/live/smartprimer.org/privkey.pem')
    app.run(debug=True, host='0.0.0.0', use_reloader=False, port=5000, ssl_context=context)
    # app.run(debug=True, host='0.0.0.0', use_reloader=False, port=5000)
