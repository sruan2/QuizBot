import os
import json
import requests
import random
from time import *
from flask_mysqldb import MySQL

import template
from utils import pretty_print, log
import database as db
from constants import CHATBOT_ID

PRAMS = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
HEADERS = {"Content-Type": "application/json"}

DELAY_TIME = 1


def send_data(data, data_type = "messages"):
    r = requests.post("https://graph.facebook.com/v2.6/me/" + data_type, params=PRAMS, headers=HEADERS, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_typing_action(recipient_id):
    '''
        This function delays the reply and sends a typing action to the specified recipient.
    '''
    sleep(DELAY_TIME)
    data = template.create_typing_action_template_json(recipient_id)
    send_data(data)


def send_image(mysql, recipient_id, image_data):
    '''
        This function sends an image to the specified recipient.
    '''
    send_typing_action(recipient_id)
    data = template.create_image_template_json(recipient_id, image_data)
    send_data(data)

    dialogue = json.loads(data)["image_url"]
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    record_id = db.insert_conversation(mysql, CHATBOT_ID, recipient_id, dialogue, "msg type", time_stamp=timestamp)

    # insert_score(mysql, recipient_id, -1, image_data["image_url"], 0)
    # insert_conversation(mysql, recipient_id, -1, "chatbot_image", "chatbot_image", image_data["image_url"], 0)


def send_message(mysql, recipient_id, template_conversation, message_data):
    '''
        This function sends a text message, with a short delay and typing action at the beginning, to the specified recipient.
    '''
    send_typing_action(recipient_id)
    data = template.create_message_template_json(recipient_id, template_conversation, message_data)
    send_data(data)

    dialogue = json.loads(data)["message"]["text"]
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    record_id = db.insert_conversation(mysql, CHATBOT_ID, recipient_id, dialogue, "msg type", time_stamp=timestamp)
    # insert the question to the user_history table
    #db.insert_user_history(mysql, int(recipient_id), QID, subject, timestamp, begin_record_id=record_id)

    # insert_score(mysql, recipient_id, -1, data["message"]["text"], 0)
    # insert_conversation(mysql, recipient_id, -1, "chatbot_message", "chatbot_message", data["message"]["text"], 0)


def send_quick_reply(mysql, recipient_id, template_conversation, quick_reply_data, message_data = ""):
    '''
        This function sends a set of quick reply buttons along with one message to the specified recipient.
    '''
    send_typing_action(recipient_id)
    data = template.create_quick_reply_template_json(recipient_id, template_conversation, quick_reply_data, message_data)
    send_data(data)

    dialogue = json.loads(data)["message"]["text"]
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    record_id = db.insert_conversation(mysql, CHATBOT_ID, recipient_id, dialogue, "msg type", time_stamp=timestamp)

    # data = json.loads(data)
    # insert_score(mysql, recipient_id, -1, data["message"]["text"], 0)
    # insert_conversation(mysql, recipient_id, -1, "chatbot_message", "chatbot_message", data["message"]["text"], 0)


def send_persistent_menu(persistent_menu_data):
    '''
        This function sets up the persistence menu.
    '''
    data = template.create_persistent_menu_json(persistent_menu_data)
    send_data(data, "messenger_profile")


def send_get_started(get_started_data):
    '''
        This function initializes the payloads.
    '''
    data = template.create_get_started_json(get_started_data)
    send_data(data, "messenger_profile")
