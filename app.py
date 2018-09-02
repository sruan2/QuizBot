'''Flash application for quizbot'''
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
import pinyin

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

# qid_to_index = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20, 21: 21, 22: 22, 23: 23, 24: 24, 25: 25, 26: 26, 27: 27, 28: 28, 29: 29, 30: 30, 31: 31, 32: 32, 33: 33, 34: 34, 35: 35, 36: 36, 37: 37, 38: 38, 39: 39, 40: 40, 41: 41, 42: 42, 43: 43, 44: 44, 45: 45, 46: 46, 47: 47, 48: 48, 49: 49, 50: 50, 51: 51, 52: 52, 53: 53, 54: 54, 55: 55, 56: 56, 57: 57, 58: 58, 59: 59, 60: 60, 61: 61, 62: 62, 63: 63, 64: 64, 65: 65, 66: 66, 67: 67, 68: 68, 69: 69, 70: 70, 71: 71, 72: 72, 73: 73, 74: 74, 75: 75, 76: 76, 77: 77, 78: 78, 79: 79, 80: 80, 81: 81, 82: 82, 83: 83, 84: 84, 85: 85, 86: 86, 87: 87, 88: 88, 89: 89, 90: 90, 91: 91, 92: 92, 93: 93, 94: 94, 95: 95, 96: 96, 97: 97, 98: 98, 99: 99, 100: 100, 101: 101, 102: 102, 103: 103, 104: 104, 105: 105, 106: 106, 107: 107, 108: 108, 109: 109, 110: 110, 111: 111, 112: 112, 113: 113, 114: 114, 115: 115, 116: 116, 117: 117, 118: 118, 119: 119, 120: 120, 121: 121, 122: 122, 123: 123, 124: 124, 125: 125, 126: 126, 127: 127, 128: 128, 129: 129, 130: 130, 131: 131, 132: 132, 133: 133, 134: 134, 135: 135, 136: 136, 137: 137, 138: 138, 139: 139, 140: 140, 141: 141, 142: 142, 143: 143, 144: 144, 145: 145, 146: 146, 147: 147, 148: 148, 149: 149}
qid_to_index = {0: 15, 1: 135, 2: 55, 3: 51, 4: 56, 5: 141, 6: 128, 7: 106, 8: 111, 9: 114, 10: 59, 11: 9, 12: 131, 13: 145, 14: 18, 15: 102, 16: 11, 17: 133, 18: 130, 19: 83, 20: 41, 21: 148, 22: 75, 23: 90, 24: 99, 25: 113, 26: 104, 27: 46, 28: 37, 29: 44, 30: 49, 31: 58, 32: 24, 33: 52, 34: 73, 35: 6, 36: 29, 37: 88, 38: 17, 39: 76, 40: 77, 41: 89, 42: 144, 43: 142, 44: 92, 45: 10, 46: 3, 47: 40, 48: 147, 49: 100, 50: 138, 51: 118, 52: 112, 53: 64, 54: 32, 55: 50, 56: 136, 57: 143, 58: 121, 59: 132, 60: 120, 61: 8, 62: 5, 63: 30, 64: 117, 65: 125, 66: 14, 67: 103, 68: 19, 69: 27, 70: 84, 71: 93, 72: 79, 73: 72, 74: 2, 75: 31, 76: 42, 77: 35, 78: 65, 79: 25, 80: 1, 81: 21, 82: 38, 83: 97, 84: 94, 85: 53, 86: 45, 87: 82, 88: 87, 89: 127, 90: 146, 91: 68, 92: 139, 93: 85, 94: 74, 95: 70}
effective_qids = {v:k for (k,v) in qid_to_index.items()}

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
@app.route('/pictures/<path:path>')
def send_lb_pictures(path):
    return send_from_directory('../pictures', path)


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

            # # Get user data
            # if sender_id == "1931189830271244":
            #     sender_firstname = "Bianca"
            #     sender_lastname = "Yu"

            # else:
            data = _get_user_profile(sender_id)
            sender_firstname = data['first_name']
            sender_lastname = data['last_name']

            # Check if the user is in cache already
            if not sender_id in cache:
                # Check if the user is in database
                if int(sender_id) in db.show_user_id_list(mysql):
                    subject = db.show_current_subject(mysql, sender_id)
                    qid = db.show_current_qid(mysql, sender_id)
                    qid = [qid_to_index[qid], qid]
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
                    qa_model.loadUserData(sender_id, user_history_data, effective_qids)
                    pretty_print('Pass the user history to the QAModel', mode='QAModel')
                # Insert the user into database and cache if it doesn't exist yet.

                else:
                    sender_firstname = pinyin.get(sender_firstname, format="strip", delimiter="")
                    sender_lastname = pinyin.get(sender_lastname, format="strip", delimiter="")
                    sender_firstname = sender_firstname.capitalize()
                    sender_lastname = sender_lastname.capitalize()
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
    # [(1139924072777403, 'Sherry'), (1805880356153906, 'Nathan'), (1850388251650155, 'Liwei')]
    reminder.RepeatedTimer(86400, template_conversation, mysql)

if __name__ == '__main__':
    # Set up Flask app and MySQL
    setup(chatbot_text)

    # Read QA json data and construct the QA knowledge base
    json_file = 'QAdataset/questions_96.json'
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

    context = ("/home/321yy/ssl_cert/smartprimer_ai.crt", "/home/321yy/ssl_cert/server.key")

    pretty_print('============ Run App ============', mode='App')
    app.run(host='0.0.0.0', threaded=True, debug=True, use_reloader=False, ssl_context=context, port=int(os.environ["PORT"]))

