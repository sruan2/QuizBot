'''Flash application for quizbot'''
import os
import yaml
import json
from random import randint
from flask import Flask, request, send_from_directory
import requests
import time
from datetime import datetime
import logging
from flask_mysqldb import MySQL

import sys
sys.path.append('./question_sequencing')

import message
import database
import chatbot
import speech
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
            if sender_id == os.environ["CHATBOT_ID"]: # return if this message is sent from the chatbot
                return "Chatbot ID", 200
            # the recipient's ID, which should be your page's facebook ID
            recipient_id = messaging_event["recipient"]["id"]

            # Get user data
            data = _get_user_profile(sender_id)
            sender_firstname = data['first_name']
            sender_lastname = data['last_name']

            if 'gender' in data:
                sender_gender = data['gender']
            else:
                sender_gender = 'unknown'

            # first-time user
            if not int(sender_id) in database.show_user_id_list(mysql):
                pretty_print('This is a new user!', mode='QuizBot')
                database.insert_user(mysql, sender_id, sender_firstname, sender_lastname, sender_gender, 1)
                database.insert_score(mysql, sender_id, -1, "new_user", 0)
                message.choose_mode_quick_reply(sender_id)

            # Liwei: update the user's name
            # database.update_user_name(mysql, sender_id, sender_firstname, sender_lastname)

            # User clicked/tapped "postback" button in Persistent menu
            if messaging_event.get("postback"):
                payload = messaging_event["postback"]["payload"] # the button's payload
                message_text = messaging_event["postback"]["title"]  # the button's text
                pretty_print("Received a Postback from Persistent Menu", mode='QuizBot')
                pretty_print("Payload is \""+payload+"\"")
                pretty_print("Message Text is \""+message_text+"\"")
                chatbot.respond_to_payload(payload, sender_id, sender_firstname, qa_model, chatbot_text, template_conversation, mysql)

            elif messaging_event.get("message"):
                # user clicked/tapped "postback" button in earlier message
                if "quick_reply" in messaging_event.get("message"):
                    payload = messaging_event["message"]["quick_reply"]["payload"] # the button's payload
                    message_text = messaging_event["message"]["text"]  # the button's text
                    pretty_print("Received a quick reply from an earlier message", mode="QuizBot")
                    pretty_print("Payload is \""+payload+"\"")
                    pretty_print("Message Text is \""+message_text+"\"")
                    chatbot.respond_to_payload(payload, sender_id, sender_firstname, qa_model, chatbot_text, template_conversation, mysql)

                # someone sent us a message
                elif not "text" in messaging_event["message"]:
                    return "key error", 200

                else:
                    message_text = messaging_event["message"]["text"]  # the message's text
                    pretty_print("Received a Message", mode="QuizBot")
                    pretty_print("Message Text is \""+message_text+"\"")
                    chatbot.respond_to_messagetext(message_text, sender_id, qa_model, chatbot_text, template_conversation, mysql)
    return "ok", 200


def get_offset_time(hour, minute, second):
    FMT = "%Y-%m-%d %H:%M:%S"
    cur_time = time.localtime()

    _year = cur_time.tm_year
    _mon = cur_time.tm_mon
    _mday = cur_time.tm_mday
    _hour = hour
    _min = minute
    _sec = second
    _wday = cur_time.tm_wday
    _yday = cur_time.tm_yday
    _isdst = cur_time.tm_isdst

    cur_time = time.strftime(FMT, cur_time)
    offset_time = time.strftime(FMT, (_year, _mon, _mday, _hour, _min, _sec, _wday, _yday, _isdst))
    tdelta = datetime.strptime(offset_time, FMT) - datetime.strptime(cur_time, FMT)

    return tdelta.seconds


with app.app_context():
    reminder_object = message.Reminder()
    tdelta = get_offset_time(20, 0, 0)
    active_list = database.show_users_newly_added(mysql) + [(1850388251650155, 'Liwei'), (1139924072777403, 'Sherry'), (1805880356153906, 'Nathan')]
    reminder.RepeatedTimer(tdelta, 86400, reminder_object.send_reminder, active_list)


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
    with open(chatbot_text_file_name + ".json") as data_file:
        chatbot_text = json.load(data_file)
    with open(template_conversation_file_name + ".json") as data_file:
        template_conversation = json.load(data_file)

    return chatbot_text, template_conversation


def setup(chatbot_text):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    pretty_print("============ Start the app ============", mode='App')
    message.init_payload(template_conversation)
    pretty_print("Initiaize the payloads", mode="Initialization")
    message.persistent_menu(template_conversation)
    pretty_print("Persistent menu loaded", mode="Initialization")


if __name__ == '__main__':
    # Load conversation source text file
    chatbot_text, template_conversation = load_source("text/chatbot_text", "text/template_conversation")
    # Set up Flask app and MySQL

    setup(chatbot_text)
    # Read QA json data and construct the QA knowledge base
    json_file = 'QAdataset/questions_filtered_150_quizbot.json'
    qa_kb = QAKnowlegeBase(json_file)

    model = os.environ["MODEL"]
    if model == "TFIDF":
        qa_model = QAModel.TFIDFModel(qa_kb)
    elif model == "SIF":
        qa_model = QAModel.SIFModel(qa_kb)
    elif model == "SIF2":
        qa_model = QAModel.SIF2Model(qa_kb)
    elif model == "DOC2VEC":
        qa_model = QAModel.Doc2VecModel(qa_kb)

    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem',
               '/etc/letsencrypt/live/smartprimer.org/privkey.pem')

    pretty_print('run app', mode='App')
    app.run(host='0.0.0.0', threaded=True, debug=True, use_reloader=False, ssl_context=context, port=int(os.environ["PORT"]))
