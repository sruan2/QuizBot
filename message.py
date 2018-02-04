import os
import json
import requests
import sys
import random

def send_a_question(recipient_id, question):

    starting_part = ["Here's a question for you! ",
                     "Let's try this one: ",
                     "Could you tell the answer to this one: "]

    ending_part = " Please note that you will earn at most 3 points if you ask for a hint."

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": random.choice(starting_part) + question + ending_part,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "I need a hint ...",
                    "payload": "I_NEED_A_HINT"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_message(recipient_id, message_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_interesting(recipient_id, main_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": main_text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Sure!",
                    "payload": "SURE"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_hint(recipient_id, main_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": main_text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Sure!",
                    "payload": "SURE!"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_ready_go(recipient_id, main_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": main_text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Yup! I'm ready! "+u'\u270A',
                    "payload": "YUP_IM_READY"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def choose_mode_quick_reply(recipient_id):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": "Now tell me which mode you would like to choose:"+u'\uD83D\uDC47',
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Quiz Mode "+u'\u270F',
                    "payload": "QUIZ_MODE"
                },
                {
                    "content_type": "text",
                    "title": "Answering Mode"+u'\uD83D\uDE3A',
                    "payload": "ANSWERING_MODE"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)        


# new added subject selection
def send_subject_quick_reply(recipient_id, main_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": main_text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Physics",
                    "payload": "PHYSICS"
                },
                {
                    "content_type": "text",
                    "title": "Chemistry",
                    "payload": "CHEMISTRY"
                },
                {
                    "content_type": "text",
                    "title": "Biology",
                    "payload": "BIOLOGY"
                },
                {
                    "content_type": "text",
                    "title": "Geology",
                    "payload": "GEOLOGY"
                },
                {
                    "content_type": "text",
                    "title": "Random",
                    "payload": "RANDOM"                
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)  

def send_why_quickreply(recipient_id, QID, standard_answer):

    #log("sending WHY button to {recipient}: {text}".format(recipient=recipient_id, text=str(QID)))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": "Correct answer is " +standard_answer,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Why",
                    "payload": "WHY"
                },
                {
                    "content_type": "text",
                    "title": "Next Question",
                    "payload": "NEXT_QUESTION"
                },
                {
                    "content_type": "text",
                    "title":"Switch Subject",
                    "payload":"SWITCH_SUBJECT"
                },
                {
                    "content_type": "text",
                    "title": "Wait, I got it right...",
                    "payload": "REPORT"
                },                 
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_why2_quickreply(recipient_id, support_sentence):

    #log("sending WHY button to {recipient}: {text}".format(recipient=recipient_id, text=str(QID)))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": support_sentence,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Why",
                    "payload": "WHY"
                },
                {
                    "content_type": "text",
                    "title": "Next Question",
                    "payload": "NEXT_QUESTION"
                },
                {
                    "content_type": "text",
                    "title":"Switch Subject",
                    "payload":"SWITCH_SUBJECT"
                },                 
                {
                    "content_type": "text",
                    "title": "Check Total Score",
                    "payload": "CHECK_TOTAL_SCORE"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_gotit_quickreply(recipient_id, sentence):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    
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
                    "payload": "GOT_IT_NEXT"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text) 



############ persistent menu ############
def persistent_menu():
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "persistent_menu":[
            {
                "locale":"default",
                "composer_input_disabled": False,
                "call_to_actions":[
                {
                    "title":"Change Mode",
                    "type":"nested",
                    "call_to_actions":[
                        {
                            "title":"Quiz Mode "+u'\u270F',
                            "type":"postback",
                            "payload":"quiz mode"
                        },
                        {
                            "title":"Answering Mode"+u'\uD83D\uDE3A',
                            "type":"postback",
                            "payload":"question answering mode"
                        }              
                        ]
                },
                {
                    "title":"Progress Report",
                    "type":"nested",
                    "call_to_actions":[
                    {
                        "title":"Check Total Score",
                        "type":"postback",
                        "payload":"MENU_SCORE"
                    },
                    {
                        "title":"Check Leaderboard",
                        "type":"postback",
                        "payload":"MENU_LEADERBOARD"
                    }
                    ]
                },
                {
                    "type":"web_url",
                    "title":"Invite Friends! "+u'\U0001F604',
                    "url":"https://www.facebook.com/sharer/sharer.php?u=https%3A//www.facebook.com/quizzzbot/",
                    "webview_height_ratio":"full"
                }
            ]
          }
        ]        
    })
    print("[QUIZBOT] PID " + str(os.getpid())+": Persistent menu loaded")
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text) 


############ greeting ############
def greeting():
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data1 = json.dumps({
        "greeting":[
            {
                "locale":"default",
                "text":"Hello!"
            }, 
            {
                "locale":"en_US",
                "text":"Welcome to QuizBot made by Sherry!"
            }
        ]
    })
    data2 = json.dumps({
        "get_started":{
        "payload":"GET_STARTED_PAYLOAD"
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data2)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data1)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print (str(message))
    sys.stdout.flush()