import os
import json
import yaml
import requests
import sys
import random
import time
import messaging_API
from database import *
from utils import *

PRAMS = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
HEADERS = {"Content-Type": "application/json"}

def send_data(data, data_type = "messages"):
    r = requests.post("https://graph.facebook.com/v2.6/me/" + data_type, params=PRAMS, headers=HEADERS, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)  


def persistent_menu(template_conversation):
    '''
        This function sets up the persistence menu.

        Args:
            template_conversation: the json structure containing the conversation and state templates 

        Returns:
    '''   
    messaging_API.send_persistent_menu(json.dumps(template_conversation["STATE"]["PERSISTENT_MENU"]))


def init_payload(template_conversation):
    '''
        This function initializes the payloads.

        Args:
            template_conversation: the json structure containing the conversation and state templates 

        Returns:
    '''
    messaging_API.send_get_started(json.dumps(template_conversation["STATE"]["GET_STARTED"]))


def send_image(recipient_id, payload, chatbot_text, image_id):
    '''
        This function sends an image to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            image_id: the name/id of the image being sent, specified in chatbot_text

        Returns:
    '''
    image_data = chatbot_text[payload]["image"][image_id]
    image_data["image_url"] = image_data["image_url"].format(os.environ["PORT"])
    messaging_API.send_image(recipient_id, image_data)


def send_sentence(recipient_id, payload, chatbot_text, template_conversation, sentence_id):
    '''
        This function sends a single sentence to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates 
            sentence_id: the name/id of the sentence being sent, specified in chatbot_text
       
        Returns:
    '''
    message_data = chatbot_text[payload]["sentence"][sentence_id]
    messaging_API.send_message(recipient_id, template_conversation, message_data) 


def send_paragraph(recipient_id, payload, chatbot_text, template_conversation, paragraph_id):
    '''
        This function sends a set of sentences to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates 
            paragraph_id: the name/id of the paragraph being sent, specified in chatbot_text
       
        Returns:
    '''
    paragraph_data = chatbot_text[payload]["paragraph"][paragraph_id]
    num_sentence = len(paragraph_data)

    for i in range(num_sentence):
        message_data = paragraph_data[i]
        messaging_API.send_message(recipient_id, template_conversation, message_data)


def send_conversation(recipient_id, payload, chatbot_text, template_conversation, conversation_id):
    '''
        This function sends a list of texts, with a short delay and typing action in between scentences, 
        along with a set of quick reply button to continue the conversation, to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates 
            conversation_id: the name/id of the conversation being sent, specified in chatbot_text
       
        Returns:
    '''
    conversation_data = chatbot_text[payload]["conversation"][conversation_id]

    message_data = conversation_data["message"]
    for msg in message_data[:-1]:
        messaging_API.send_message(recipient_id, template_conversation, msg)

    quick_reply_data = conversation_data["quick_reply"]
    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data, message_data[-1])


def send_format_quick_reply_text(recipient_id, template_conversation, state, format_fill_text):
    '''
        This function sends a quick reply with formatted text message.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates 
            state: the state's name, specified in template_conversation
            format_fill_text: the text to be filled into the placeholder of the message text

        Returns:
    '''
    quick_reply_data = template_conversation["STATE"][state]["quick_reply"]
    text_format = quick_reply_data["message"]["text"]
    quick_reply_data["message"]["text"] = quick_reply_data["message"]["text"].format(format_fill_text)
    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data)
    quick_reply_data["message"]["text"] = text_format   


def send_choose_subject(recipient_id, template_conversation):
    '''
        This function asks the specified recipient to choose a subject.
        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates 
       
        Returns:
    '''
    quick_reply_data = template_conversation["STATE"]["CHOOSE_SUBJECT"]["quick_reply"]
    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data)


def send_question(recipient_id, template_conversation, payload = "", qa_model = "", mysql = "", subject = "", question = ""):
    '''
        This function sends a question to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates 
            payload: chatbot's payload state
            qa_model: the question answering model containing information about the question dataset
            mysql: database
            subject: the subject name: (science, safety, gre, random)
            question: the question string
       
        Returns:
    '''    
    if question == "":
        question, QID = qa_model.pickQuestion(subject)
        update_status(mysql, recipient_id, 0)
        insert_question(mysql, recipient_id, QID, payload)

    message_data = template_conversation["STATE"]["QUESTION"]["message"]
    messaging_API.send_message(recipient_id, template_conversation, message_data)

    send_format_quick_reply_text(recipient_id, template_conversation, "QUESTION", question)


def send_say_hi(recipient_id, template_conversation, recipient_firstname):
    '''
        This function sends a hi message to the specified recipient.
    '''
    send_format_quick_reply_text(recipient_id, template_conversation, "SAY_HI", recipient_firstname)


def send_correct_answer(recipient_id, payload, template_conversation, qa_model, score, mysql):
    '''
        This function sends the correct answer of a question to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            template_conversation: the json structure containing the conversation and state templates 
            qa_model: the question answering model containing information about the question dataset
            score: the score to be logged into the database
            mysql: database
       
        Returns:
    '''
    QID, _ = show_last_qid_subject(mysql, recipient_id)
    standard_answer = qa_model.getAnswer(QID)
    insert_score(mysql, recipient_id, QID, payload, score)

    send_format_quick_reply_text(recipient_id, template_conversation, "CORRECT_ANSWER", standard_answer)

    update_status(mysql, recipient_id, 1)


def send_explanation(recipient_id, template_conversation, qa_model, mysql):
    '''
        This function sends the explanation of a question to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates 
            mysql: database
            explanation: the explanation of a question to be sent to the recipient
       
        Returns:
    '''
    QID, _ = show_last_qid_subject(mysql, recipient_id)
    explanation_sentence = qa_model.getSupport(QID)

    message_data = template_conversation["STATE"]["EXPLANATION"]["message"]
    messaging_API.send_message(recipient_id, template_conversation, message_data)
    
    send_format_quick_reply_text(recipient_id, template_conversation, "EXPLANATION", explanation_sentence)


def send_total_score(recipient_id, template_conversation, total_score):
    '''
        This function sends the total score of the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates 
            total score: the total score of the recipient, extracted from the database
       
        Returns:
    ''' 
    send_format_quick_reply_text(recipient_id, template_conversation, "TOTAL_SCORE", total_score)


def send_hint(recipient_id, qa_model, mysql):
    '''
        This function sends a list of hints(distractors) to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            qa_model: the question answering model containing information about the question dataset
            mysql: database
       
        Returns:
    '''
    QID, _ = show_last_qid_subject(mysql, recipient_id)

    message_text = ""
    options = []
    index = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for x in qa_model.DKB[QID]:
        options.append({
                    "content_type": "text",
                    "title": str(x),
                    "payload": "BUTTON_DKB_"+str(x)
                })
    for x in qa_model.AKB[QID]:
        options.append({
                    "content_type": "text",
                    "title": str(x),
                    "payload": "BUTTON_AKB_"+str(x)
                })
    random.shuffle(options)

    for i in range(len(options)):
        message_text += index[i%10]
        message_text += " "
        message_text += str(options[i]["title"])
        message_text += "\n"
        options[i]["title"] = index[i%10]

    options.append({
                    "content_type": "text",
                    "title": "I don’t know 😓",
                    "payload": "I_DONT_KNOW"
                })

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text" : message_text,
            "quick_replies": options
        }
    })
    send_data(data)


class Reminder():
    def __init__(self, template_conversation):
        self.users = {}
        self.template_conversation = template_conversation


    def send_reminder(self, list):
        '''
            This function sends a reminder to the specified recipient.
                Args:
                    list: a list of user ids to which the reminder is sent
               
                Returns:
        '''
        print(self.users)
        for recipient_id, user_name in list:
            if recipient_id not in self.users:
                self.users[recipient_id] = 0
            if self.users[recipient_id] < 7:
                self.users[recipient_id] += 1
                image_data = self.template_conversation["STATE"]["REMINDER"]["image"]
                image_data["image_url"] = image_data["image_url"].format(os.environ["PORT"])
                messaging_API.send_image(recipient_id, image_data)
                send_format_quick_reply_text(recipient_id, self.template_conversation, "REMINDER", user_name)
                print("[QUIZBOT] PID " + str(os.getpid())+": Sent Reminder To " + str(user_name) + " With ID " + str(recipient_id) + " At " + strftime("%Y-%m-%d %H:%M:%S", localtime()))


