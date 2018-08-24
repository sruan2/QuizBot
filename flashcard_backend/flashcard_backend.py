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
from QAKnowledgebase import QAKnowlegeBase
from time import strftime, localtime, sleep

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# ================== MySQL Setup ==================
mysql = MySQL()
app.config['MYSQL_HOST'] = os.environ["DB_HOST"]
app.config['MYSQL_USER'] = os.environ["DB_USER"]
app.config['MYSQL_PASSWORD'] = os.environ["DB_PASSWORD"]
app.config['MYSQL_DB'] = os.environ["DB"]
mysql.init_app(app)

# ================== Load Sequencing Model ==================
json_file = '../QAdataset/questions_filtered_150_quizbot.json'
qa_kb = QAKnowlegeBase(json_file)
model = RandomSequencingModel(qa_kb)

json_file_between_subject = '../QAdataset/questions_between_subjects_flashcard.json'
qa_kb_between_subject = QAKnowlegeBase(json_file_between_subject)
model_between_subject = RandomSequencingModel(qa_kb_between_subject)

user_between_subject = {"672579434": "Dee Dee Thao", "725315344": "Tyler Yep",  \
                        "1844410129": "Yinuo Yao", "1852193290": "Andrew Ying", \
                        "2000946117": "jingyi li", "2079749432": "Jenn Hu",     \
                        "732119323": "Joy Yuzurih", "664942274": "Henry Qin", \
                        "902902333": "Liwei Jiang", "2137982794": "Nina Horowitz", \
                        "1689820842": "Daniel Do", "1394174277": "Claire Yang", \
                        "1515117469": "Olivia Yang", "1295547909": "Helen Wang", \
                        "1237870507": 'Wangjianzhe Shao', "772553696": "Kylie Jue", \
                        "747757516": "De-An Huang"}
                        
user_id_between_subject = list(user_between_subject.keys())

with app.app_context():
    user_list = db.show_user_id_list_flashcard(mysql)
    for user_id in user_list:
        model.loadUserData(user_id, db.show_user_history_flashcard(mysql, user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/question_data", methods=['GET'])
def fetch_question():
    user_id = request.args.get('user_id')
    if user_id in user_id_between_subject:
        print("--------------------")
        print(user_between_subject[user_id])
        data = model_between_subject.pickNextQuestion(subject='random')
    else:
        data = model.pickNextQuestion(subject='random')
    return jsonify(data)


@app.route("/question_data_gre", methods=['GET'])
def fetch_question_gre():
    user_id = request.args.get('user_id')
    if user_id in user_id_between_subject:
        print("--------------------")
        print(user_between_subject[user_id])
        data = model_between_subject.pickNextQuestion(subject='gre')
    else:
        data = model.pickNextQuestion(subject='gre')
    return jsonify(data)


@app.route("/question_data_science", methods=['GET'])
def fetch_question_science():
    user_id = request.args.get('user_id')
    if user_id in user_id_between_subject:
        print("--------------------")
        print(user_between_subject[user_id])
        data = model_between_subject.pickNextQuestion(subject='science')
    else:
        data = model.pickNextQuestion(subject='science')
    return jsonify(data)


@app.route("/question_data_safety", methods=['GET'])
def fetch_question_safety():
    user_id = request.args.get('user_id')
    
    if user_id in user_id_between_subject:
        print("--------------------")
        print(user_between_subject[user_id])
        data = model_between_subject.pickNextQuestion(subject='safety')
    else:
        data = model.pickNextQuestion(subject='safety')
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
        model.updateHistory(sender_id, (qid, 1, timestamp))
    elif user_action == "I don't know":
        print("I don't know")
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        model.updateHistory(sender_id, (qid, 0, timestamp))

    print("[FLASHCARD] PID " + str(os.getpid())+": Record FLASHCARD user action successfully")
    return "ok", 200


if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem', '/etc/letsencrypt/live/smartprimer.org/privkey.pem')
    app.run(debug=True, host='0.0.0.0', use_reloader=False, port=5000, ssl_context=context)
    # app.run(debug=True, host='0.0.0.0', use_reloader=False, port=5000)
