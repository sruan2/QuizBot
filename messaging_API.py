'''
    messaging_API.py
    Author: Liwei Jiang
    Date: 24/07/2018
    Usage: Internal messaging API sending data to Facebook Messenger.
'''

import os
import json
import requests
import random
from time import strftime, localtime, sleep
from flask_mysqldb import MySQL

import template
from utils import pretty_print, log
import database as db
from constants import CHATBOT_ID


PRAMS = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
HEADERS = {"Content-Type": "application/json"}
# time to sleep in send_typing_action
DELAY_TIME = 1


def send_data(data, data_type="messages"):
    '''
        Base function that sends data to Facebook API. 
        All other messaging_API functions call this one.
    '''
    r = requests.post("https://graph.facebook.com/v2.6/me/" +
                      data_type, params=PRAMS, headers=HEADERS, data=data)
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
        And saves the image_url to the conversation database.
    '''
    send_typing_action(recipient_id)
    data = template.create_image_template_json(recipient_id, image_data)
    send_data(data)

    dialogue = image_data["image_url"][0]
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    db.insert_conversation(mysql, CHATBOT_ID, recipient_id,
                           dialogue, "BOT: image", timestamp)


def send_message(mysql, recipient_id, template_conversation, message_data):
    '''
        This function sends a text message, with a short delay and typing action at the beginning, to the specified recipient.
        And saves the message text to the conversation database
    '''
    send_typing_action(recipient_id)
    data = template.create_message_template_json(
        recipient_id, template_conversation, message_data)
    send_data(data)

    dialogue = json.loads(data)["message"]["text"]
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    db.insert_conversation(mysql, CHATBOT_ID, recipient_id,
                           dialogue, "BOT: message", timestamp)


def send_quick_reply(mysql, recipient_id, template_conversation, quick_reply_data, message_data=""):
    '''
        This function sends a set of quick reply buttons along with one message to the specified recipient.
        TODO:
            - Use None if needed. Don't use ""
            - what is message_data? Add some documentation here.
    '''
    send_typing_action(recipient_id)

    data = template.create_quick_reply_template_json(recipient_id, template_conversation, quick_reply_data, message_data)
    send_data(data)

    dialogue = json.loads(data)["message"]["text"]
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    uid = db.insert_conversation(mysql, CHATBOT_ID, recipient_id, dialogue, "BOT: quick reply", timestamp)
    # return timestamp and uid so that we can log the information in the [user_history] dataset when the bot sends a question
    return uid


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
