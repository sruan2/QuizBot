'''
    app.py
    Author: Liwei Jiang, Sherry Ruan, Zhengneng Qiu
    Last Modified Date: 09/08/2018
    Usage: Flask application for QuizBot.
'''

import os
import yaml
import json
from random import randint
from flask import Flask, request, send_from_directory
import requests
from time import localtime, strftime
from datetime import datetime
import logging
from flask_mysqldb import MySQL

import sys
sys.path.append('./question_sequencing')

from constants import CHATBOT_ID
import message
import database as db
import chatbot
import reminder
from QAKnowledgebase import QAKnowlegeBase
import QAModel
from utils import pretty_print


# ================== Global Varaibles ==================
#  Flash App Setup
app = Flask(__name__, static_url_path='')

# MySQL Setup
mysql = MySQL()
app.config['MYSQL_HOST'] = os.environ["DB_HOST"]
app.config['MYSQL_USER'] = os.environ["DB_USER"]
app.config['MYSQL_PASSWORD'] = os.environ["DB_PASSWORD"]
app.config['MYSQL_DB'] = os.environ["DB"]
mysql.init_app(app)

# access_token for facebook messenger
access_token = os.environ["PAGE_ACCESS_TOKEN"]

# set up cache to store user data such as current_subject and current_qid
cache = {}

# For static pictures such as owl
@app.route('/pictures/<path:path>')
def send_pictures(path):
    return send_from_directory('pictures', path)


# For tmp picture files such as dynamically generated leaderboard
@app.route('/tmp/pictures/<path:path>')
def send_lb_pictures(path):
    return send_from_directory('../tmp/pictures', path)


# go to https://smartprimer.org:8443/test
@app.route('/test', methods=['GET'])
def test():
    return "test", 200


# go to https://smartprimer.org:8443
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    print('verify')
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            print('403')
            return "Verification token mismatch", 403
        print('200')
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    '''endpoint for processing incoming messaging events'''
    data = request.get_json()

    if data["object"] != "page":
        return "Object is not a page", 200

    for entry in data["entry"]:
        if not entry.get("messaging"):
            continue

        for messaging_event in entry["messaging"]:
            if messaging_event.get("delivery"):  # delivery confirmation
                continue
            if messaging_event.get("optin"):  # optin confirmation
                continue

            # the facebook ID of the person sending you the message
            sender_id = messaging_event["sender"]["id"]
            # Sherry: don't need this anymore because we can disable it in Facebook Developer Setting
            if sender_id == CHATBOT_ID:  # return if this message is sent from the chatbot
                return "Chatbot ID", 200
            # the recipient's ID, which should be your page's facebook ID
            recipient_id = messaging_event["recipient"]["id"]

            # Get user data
            data = _get_user_profile(sender_id)
            sender_firstname = data['first_name']
            sender_lastname = data['last_name']

            # db.insert_user_history(mysql, 1458878367545796, "1", "gre", "0")
            # db.insert_user_history(mysql, "1605863346117668", "1", "gre", 0)
            # db.insert_user_history(mysql, "1648221408640749", "1", "gre", 0)
            # db.insert_user_history(mysql, "1679729278802568", "1", "gre", 0)
            # db.insert_user_history(mysql, "1702211463234799", "1", "gre", 0)
            # db.insert_user_history(mysql, "1809787982474164", "1", "gre", 0)
            # db.insert_user_history(mysql, "1833809400020333", "1", "gre", 0)
            # db.insert_user_history(mysql, "1869513133135340", "1", "gre", 0)
            # db.insert_user_history(mysql, "1904897786199799", "1", "gre", 0)
            # db.insert_user_history(mysql, "1913473808676037", "1", "gre", 0)
            # db.insert_user_history(mysql, "2326685720705389", "1", "gre", 0)
            # db.insert_user_history(mysql, "2341119375928551", "1", "gre", 0)
            # db.insert_user_history(mysql, "2370522646291297", "1", "gre", 0)

            # if sender_id == "1850388251650155":
            #     sender_id = "1458878367545796"
            #     sender_firstname = "Julia"
            #     sender_lastname = "Thompson"

            # if sender_id == "1850388251650155":
            #     sender_id = "1605863346117668"
            #     sender_firstname = "Henry"
            #     sender_lastname = "Qin"

            # if sender_id == "1850388251650155":
            #     sender_id = "1648221408640749"
            #     sender_firstname = "Nina"
            #     sender_lastname = "Horowitz"

            # if sender_id == "1850388251650155":
            #     sender_id = "1679729278802568"
            #     sender_firstname = "Joy"
            #     sender_lastname = "Yuzuriha"

            # if sender_id == "1850388251650155":
            #     sender_id = "1702211463234799"
            #     sender_firstname = "Zhenqi"
            #     sender_lastname = "Hu"

            # if sender_id == "1605863346117668":
            #     sender_id = "1809787982474164"
            #     sender_firstname = "Tyler"
            #     sender_lastname = "Yep"

            # if sender_id == "1850388251650155":
            #     sender_id = "1833809400020333"
            #     sender_firstname = "Fangmingyu"
            #     sender_lastname = "Yang"

            # if sender_id == "1850388251650155":
            #     sender_id = "1869513133135340"
            #     sender_firstname = "Noah Yinuo"
            #     sender_lastname = "Yao"

            # if sender_id == "1605863346117668":
            #     sender_id = "1904897786199799"
            #     sender_firstname = "Francis"
            #     sender_lastname = "Yan"

            # if sender_id == "1850388251650155":
            #     sender_id = "1913473808676037"
            #     sender_firstname = "Dee Dee"
            #     sender_lastname = "Thao"

            # if sender_id == "1850388251650155":
            #     sender_id = "2326685720705389"
            #     sender_firstname = "Andrew"
            #     sender_lastname = "Ying"

            # if sender_id == "1850388251650155":
            #     sender_id = "2341119375928551"
            #     sender_firstname = "Daniel"
            #     sender_lastname = "Do"


            # if sender_id == "1850388251650155":
            #     sender_id = "2370522646291297"
            #     sender_firstname = "Jingyi"
            #     sender_lastname = "Li"



            # Check if the user is in cache already
            if not sender_id in cache:
                # Check if the user is in database
                if int(sender_id) in db.show_user_id_list(mysql):
                    subject = db.show_current_subject(mysql, sender_id)
                    qid = db.show_current_qid(mysql, sender_id)
                    begin_uid = db.show_last_begin_uid(mysql, sender_id)
                    pretty_print('Retrieve the user from [user]', mode='Database')
                    pretty_print('{} {}'.format(sender_firstname, sender_lastname))
                    cache[sender_id] = {'firstname': sender_firstname,
                                        'current_qid': qid,
                                        'current_subject': subject,
                                        'begin_uid': begin_uid,
                                        'waiting_for_answer': 0,
                                        'if_explanation_text': False,
                                        'last_payload': None}
                    pretty_print('Insert the user into cache', mode='Cache')
                    user_history_data = db.show_user_history(mysql, sender_id) # tuple of (qid, score, time_stamp)
                    pretty_print('Retrieve the user history from [user_history]', mode='Database')
                    print(user_history_data)

                    if sender_id == "1139924072777403":
                        user_history_data = list(user_history_data)[1:]

                    print(user_history_data)

                    qa_model.loadUserData(sender_id, user_history_data)
                    pretty_print('Pass the user history to the QAModel', mode='QAModel')
                # Insert the user into database and cache if it doesn't exist yet.
                else:
                    db.insert_user(mysql, sender_id, sender_firstname, sender_lastname)
                    pretty_print('Insert a user into [user]', mode='Database')
                    pretty_print('{} {}'.format(
                        sender_firstname, sender_lastname))
                    cache[sender_id] = {'firstname': sender_firstname,
                                        'current_qid': None,
                                        'current_subject': None,
                                        'begin_uid': None,
                                        'waiting_for_answer': 0,
                                        'if_explanation_text': False,
                                        'last_payload': None}
                    pretty_print('Insert a user into cache', mode='Cache')

                    pretty_print('firstname: '+str(cache[sender_id]['firstname']))
                    pretty_print('current_qid: '+str(cache[sender_id]['current_qid']))
                    pretty_print('current_subject: '+str(cache[sender_id]['current_subject']))
                    pretty_print('begin_uid: '+str(cache[sender_id]['begin_uid']))
                    pretty_print('waiting_for_answer: '+str(cache[sender_id]['waiting_for_answer']))
                    pretty_print('if_explanation_text: '+str(cache[sender_id]['if_explanation_text']))
                    pretty_print('last_payload: '+str(cache[sender_id]['last_payload']))

            # User clicked/tapped "postback" button in Persistent menu
            if messaging_event.get("postback"):
                # the button's payload
                payload = messaging_event["postback"]["payload"]
                # the button's text
                message_text = messaging_event["postback"]["title"]
                pretty_print(
                    "Received a Postback from Persistent Menu", mode='QuizBot')
                pretty_print("Payload is \""+payload+"\"")
                pretty_print("Message Text is \""+message_text+"\"")
                # save the user's quick reply to the conversation database
                timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
                uid = db.insert_conversation(mysql, sender_id, CHATBOT_ID, message_text, "persistent_menu: "+payload, timestamp)
                chatbot.respond_to_payload(payload, sender_id, qa_model, chatbot_text, template_conversation, mysql, cache, uid)

            elif messaging_event.get("message"):
                # user clicked/tapped "postback" button in earlier message
                if "quick_reply" in messaging_event.get("message"):
                    # the button's payload
                    payload = messaging_event["message"]["quick_reply"]["payload"]
                    # the button's text
                    message_text = messaging_event["message"]["text"]
                    pretty_print("Received a quick reply from an earlier message", mode="QuizBot")
                    pretty_print("Payload is \""+payload+"\"")
                    pretty_print("Message Text is \""+message_text+"\"")
                    # save the user's quick reply to the conversation database
                    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
                    uid = db.insert_conversation(mysql, sender_id, CHATBOT_ID, message_text, "user_quick_reply: "+payload, timestamp)

                    chatbot.respond_to_payload(payload, sender_id, qa_model, chatbot_text, template_conversation, mysql, cache, uid)

                # someone sent us a message
                elif not "text" in messaging_event["message"]:
                    return "key error", 200

                # user types their message
                else:
                    message_text = messaging_event["message"]["text"]
                    pretty_print("Received a Message", mode="QuizBot")
                    pretty_print("Message Text is \""+message_text+"\"")
                    # save the user's free reply to the conversation database
                    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
                    uid = db.insert_conversation(mysql, sender_id, CHATBOT_ID, message_text, "user_typing", timestamp)
                    chatbot.respond_to_messagetext(message_text, sender_id, qa_model, chatbot_text, template_conversation, mysql, cache, uid)
    return "ok", 200


def _get_user_profile(sender_id):
    r = requests.get("https://graph.facebook.com/v2.6/{psid}?fields=first_name,last_name"
                     "&access_token={token}".format(psid=sender_id, token=access_token))
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        return
    data = json.loads(r.text)
    return data


# ================== SET UP ==================
def yaml_to_json(chatbot_text_file_name, template_conversation_file_name):
    '''
        This function converts the chatbot conversation and source yaml files to json format.
    '''
    with open(chatbot_text_file_name + ".yml", 'r') as stream:
        try:
            data = yaml.load(stream)
            with open(chatbot_text_file_name + ".json", 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
        except yaml.YAMLError as exc:
            print(exc)

    with open(template_conversation_file_name + ".yml", 'r') as stream:
        try:
            data = yaml.load(stream)
            with open(template_conversation_file_name + ".json", 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
        except yaml.YAMLError as exc:
            print(exc)


def load_source(chatbot_text_file_name, template_conversation_file_name):
    '''
        This function loads the chatbot conversation and source yaml files.
    '''
    with open(chatbot_text_file_name + ".json") as data_file:
        chatbot_text = json.load(data_file)
    with open(template_conversation_file_name + ".json") as data_file:
        template_conversation = json.load(data_file)

    return chatbot_text, template_conversation


def setup(chatbot_text):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    pretty_print("============ Set up App ============", mode='App')
    message.init_payload(template_conversation)
    pretty_print("Initiaize the payloads", mode="Initialization")
    message.persistent_menu(template_conversation)
    pretty_print("Persistent menu loaded", mode="Initialization")


# Sherry: can we move this to main function?
with app.app_context():
    # Load conversation source text file
    chatbot_text, template_conversation = load_source(
        "text/chatbot_text", "text/template_conversation")
    reminder.RepeatedTimer(86400, template_conversation, mysql)

if __name__ == '__main__':
    # Set up Flask app and MySQL
    setup(chatbot_text)

    # Read QA json data and construct the QA knowledge base
    json_file = 'QAdataset/questions_between_subjects_quizbot.json'
    qa_kb = QAKnowlegeBase(json_file)
    model = os.environ["MODEL"]
    question_sequencing_model = os.environ["QUESTION_SEQUENCING_MODEL"]
    
    if model == "TFIDF":
        qa_model = QAModel.TFIDFModel(qa_kb, question_sequencing_model)
    elif model == "SIF":
        qa_model = QAModel.SIFModel(qa_kb, question_sequencing_model)
    elif model == "SIF2":
        qa_model = QAModel.SIF2Model(qa_kb, question_sequencing_model)
    elif model == "DOC2VEC":
        qa_model = QAModel.Doc2VecModel(qa_kb, question_sequencing_model)
    elif model == "SupervisedSIFModeL":
        qa_model = QAModel.SupervisedSIFModeL(qa_kb, question_sequencing_model)

    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem',
               '/etc/letsencrypt/live/smartprimer.org/privkey.pem')

    pretty_print('============ Run App ============', mode='App')
    app.run(host='0.0.0.0', threaded=True, debug=True, use_reloader=False,
            ssl_context=context, port=int(os.environ["PORT"]))
