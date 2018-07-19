import os
import json
import requests
import random
from time import *
import template
from utils import pretty_print
from utils import log
from database import *
from flask_mysqldb import MySQL

PRAMS = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
HEADERS = {"Content-Type": "application/json"}

DELAY_TIME = 1

# MySQL Setup
mysql = MySQL()
app.config['MYSQL_HOST'] = os.environ["DB_HOST"]
app.config['MYSQL_USER'] = os.environ["DB_USER"]
app.config['MYSQL_PASSWORD'] = os.environ["DB_PASSWORD"]
app.config['MYSQL_DB'] = os.environ["DB"]
mysql.init_app(app)

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


def send_image(recipient_id, image_data):
    '''
        This function sends an image to the specified recipient.
    '''
    send_typing_action(recipient_id)
    data = template.create_image_template_json(recipient_id, image_data)
    send_data(data)

    if image_data["template_type"] == "generic":
        insert_score(mysql, recipient_id, -1, data["recipient"]["message"]["attachment"]["payload"]["elements"]["image_url"], "chatbot_image", 0)
    else:
        insert_score(mysql, recipient_id, -1, data["recipient"]["message"]["attachment"]["payload"]["url"], "chatbot_image", 0)


def send_message(recipient_id, template_conversation, message_data):
    '''
        This function sends a text message, with a short delay and typing action at the beginning, to the specified recipient.
    '''
    send_typing_action(recipient_id)
    data = template.create_message_template_json(recipient_id, template_conversation, message_data)
    send_data(data)

    insert_score(mysql, recipient_id, -1, data["message"]["text"], "chatbot_text", 0)    


def send_quick_reply(recipient_id, template_conversation, quick_reply_data, message_data = ""):
    '''
        This function sends a set of quick reply buttons along with one message to the specified recipient.
    '''
    send_typing_action(recipient_id)
    data = template.create_quick_reply_template_json(recipient_id, template_conversation, quick_reply_data, message_data)
    send_data(data)


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
