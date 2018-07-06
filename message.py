import os
import json
import yaml
import requests
import sys
import random
import time
import messaging_API
from utils import pretty_print
from utils import log

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
    '''   
    messaging_API.send_persistent_menu(json.dumps(template_conversation["STATE"]["PERSISTENT_MENU"]))


def send_image(recipient_id, payload, chatbot_text, image_id):
    '''
        This function sends an image to the specified recipient.
    '''
    messaging_API.send_typing_action(recipient_id)
    image_data = chatbot_text[payload]["image"][image_id]
    messaging_API.send_image(recipient_id, image_data)


def send_sentence(recipient_id, payload, chatbot_text, template_conversation, sentence_id):
    '''
        This function sends a single sentence to the specified recipient.
    '''
    message_data = chatbot_text[payload]["sentence"][sentence_id]
    messaging_API.send_message(recipient_id, template_conversation, message_data)


def send_paragraph(recipient_id, payload, chatbot_text, template_conversation, paragraph_id):
    '''
        This function sends a set of sentences to the specified recipient.
    '''
    paragraph_data = chatbot_text[payload]["paragraph"][paragraph_id]
    num_paragraph = len(paragraph_data)

    for i in range(num_paragraph):
        message_data = paragraph_data[i]
        messaging_API.send_message(recipient_id, template_conversation, message_data)


def send_conversation(recipient_id, payload, chatbot_text, template_conversation, conversation_id):
    '''
        This function sends a list of texts, with a short delay and typing action in between scentences, 
        along with a set of quick reply button to continue the conversation, to the specified recipient.

    '''
    conversation_data = chatbot_text[payload]["conversation"][conversation_id]
    message_data = conversation_data["message"]
    quick_reply_data = conversation_data["quick_reply"]

    for msg in message_data[:-1]:
        messaging_API.send_message(recipient_id, template_conversation, msg)

    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data, message_data[-1])


def send_question(recipient_id, template_conversation, question):
    '''
        This function sends a question to the specified recipient.
    '''
    question_data = template_conversation["STATE"]["QUESTION"]
    message_data = question_data["message"]
    quick_reply_data = question_data["quick_reply"]

    messaging_API.send_message(recipient_id, template_conversation, message_data)
    
    question_format = quick_reply_data["message"]["text"]
    quick_reply_data["message"]["text"] = quick_reply_data["message"]["text"].format(question)
    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data)
    quick_reply_data["message"]["text"] = question_format


def send_say_hi(recipient_id, template_conversation, recipient_firstname):
    '''
        This function sends a hi message to the specified recipient.
    '''
    quick_reply_data = template_conversation["STATE"]["SAY_HI"]["quick_reply"]
    
    say_hi_format = quick_reply_data["message"]["text"]
    quick_reply_data["message"]["text"] = quick_reply_data["message"]["text"].format(recipient_firstname)
    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data)
    quick_reply_data["message"]["text"] = say_hi_format


def send_correct_answer(recipient_id, template_conversation, standard_answer):
    '''
        This function sends the correct answer of a question to the specified recipient.
    '''
    correct_answer_data = template_conversation["STATE"]["CORRECT_ANSWER"]
    quick_reply_data = correct_answer_data["quick_reply"]
    
    correct_answer_format = quick_reply_data["message"]["text"]
    quick_reply_data["message"]["text"] = quick_reply_data["message"]["text"].format(standard_answer)
    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data)
    quick_reply_data["message"]["text"] = correct_answer_format


def send_choose_subject(recipient_id, template_conversation):
    '''
        This function asks the specified recipient to choose a subject.
    '''
    quick_reply_data = template_conversation["STATE"]["CHOOSE_SUBJECT"]["quick_reply"]
    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data)


def send_explanation(recipient_id, template_conversation, explanation):
    '''
        This function sends the explanation of a question to the specified recipient.
    '''
    explanation_data = template_conversation["STATE"]["EXPLANATION"]
    message_data = explanation_data["message"]
    quick_reply_data = explanation_data["quick_reply"]

    messaging_API.send_message(recipient_id, template_conversation, message_data)
    
    explanation_format = quick_reply_data["message"]["text"]
    quick_reply_data["message"]["text"] = quick_reply_data["message"]["text"].format(explanation)
    messaging_API.send_quick_reply(recipient_id, template_conversation, quick_reply_data)
    quick_reply_data["message"]["text"] = explanation_format


def send_hint(recipient_id, main_text, qa_model, qid):
    '''
        This function sends a list of hints to the specified recipient.

        recipient_id: recipient id of where the messages are sent
        main_text: a message string
        qa_model: QA model used for look up for answers and distractors
        qid: ID of the question
    '''
    message_text = ""
    options = []
    index = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for x in qa_model.DKB[qid]:
        options.append({
                    "content_type": "text",
                    "title": str(x),
                    "payload": "BUTTON_DKB_"+str(x)
                })
    for x in qa_model.AKB[qid]:
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
                    "payload": "BUTTON_I_DONT_KNOW"
                })

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text" : main_text
        }
    })
    send_data(data)

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














def send_bugreport(recipient_id, text):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Next question 💪",
                    "payload": "BUTTON_NEXT_QUESTION"
                },
                {
                    "content_type": "text",
                    "title": "Switch Subject!",
                    "payload": "BUTTON_SWITCH_SUBJECT"
                }
            ]
        }
    })
    send_data(data)

def send_reminder(list):
    count_sent = {}
    for recipient_id, user_name in list:

        if recipient_id not in count_sent:
            count_sent[recipient_id] = 0

        if count_sent[recipient_id] < 7:
            count_sent[recipient_id] += 1
            data = json.dumps({
                "recipient": {
                    "id": recipient_id
                },
                "message": {
                    "text": user_name + ", you haven't talked to me for more than a day, would you like to continue the conversation with me now?",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "Continue 💪",
                            "payload": "BUTTON_CONTINUE"
                        }
                    ]
                }
            })
            r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=PRAMS, headers=HEADERS, data=data)
            if r.status_code != 200:
                log(r.status_code)
                log(r.text)
            else:
                print("[QUIZBOT] PID " + str(os.getpid())+": Sent Reminder To " + str(user_name) + " With ID " + str(recipient_id) + " At " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

def send_gotit_quickreply(recipient_id, sentence):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": sentence,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Got it, next!",
                    "payload": "BUTTON_GOT_IT_NEXT"
                }
            ]
        }

    })
    send_data(data)



def send_greeting():
    data = json.dumps({
        "get_started":{
        "payload":"GET_INTRO_1"
        }
    })
    send_data(data, "messenger_profile")

def log(message):
    print(str(message))
    sys.stdout.flush()

def send_message(sender_id, msg_subject):
    pass


