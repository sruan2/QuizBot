import os
import json
import requests
import sys

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

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
                    "payload": "<POSTBACK_PAYLOAD>"
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
                    "type":"postback",
                    "content_type": "text",
                    "title": "Sure!",
                    "payload": "<POSTBACK_PAYLOAD>"
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
                    "type":"postback",
                    "content_type": "text",
                    "title": "Yup! I'm ready! "+u'\u270A',
                    "payload": "<POSTBACK_PAYLOAD>"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_mode_quick_reply(recipient_id, main_text):

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
                    "type":"postback",
                    "title": "Quiz Mode "+u'\u270F',
                    "payload": "none"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Answering Mode"+u'\uD83D\uDE3A',
                    "payload": "none"
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
                    "type":"postback",
                    "title": "Physics",
                    "payload": "<POSTBACK_PAYLOAD>"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Chemistry",
                    "payload": "<POSTBACK_PAYLOAD>"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Biology",
                    "payload": "<POSTBACK_PAYLOAD>"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Geology",
                    "payload": "<POSTBACK_PAYLOAD>"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Random",
                    "payload": "<POSTBACK_PAYLOAD>"                
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)  

def send_why_quickreply(recipient_id, QID, standard_answer):

    log("sending WHY button to {recipient}: {text}".format(recipient=recipient_id, text=str(QID)))

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
            "text": "Standard answer is " +standard_answer,
            "quick_replies": [
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Why",
                    "payload": "Why"+str(QID)
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Next Question",
                    "payload": "<POSTBACK_PAYLOAD>"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title":"Switch Subject",
                    "payload":"<POSTBACK_PAYLOAD>"
                },                 
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Check Total Score",
                    "payload": "<POSTBACK_PAYLOAD>"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Report Bug",
                    "payload": "<POSTBACK_PAYLOAD>"
                }
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
                    "type":"postback",
                    "title": "Why",
                    "payload": "<POSTBACK_PAYLOAD>"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Next Question",
                    "payload": "<POSTBACK_PAYLOAD>"
                },
                {
                    "content_type": "text",
                    "type":"postback",
                    "title":"Switch Subject",
                    "payload":"<POSTBACK_PAYLOAD>"
                },                 
                {
                    "content_type": "text",
                    "type":"postback",
                    "title": "Check Total Score",
                    "payload": "<POSTBACK_PAYLOAD>"
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
                    "type":"postback",
                    "title": "Got it, next!",
                    "payload": "<POSTBACK_PAYLOAD>"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text) 

def log(message):  # simple wrapper for logging to stdout on heroku
    print (str(message))
    sys.stdout.flush()





############ thread_setting ############
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data)
    print("*"*100)
    print("PERSISTENT MENU")
    if r.status_code != 200:
        log(r.status_code)
        log(r.text) 

def greeting():
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        #"access_token": "EAATy6mWWYHwBAMtHKuxZAj77n9NZCnXzLUctSwmpDzcjJARDPXALUZAQIpgmJg8ZAKjJB2pjOFeGSlecpWZCje5pEzACZCINnxW5NMJSTLffdL8eJbS3aMWLZBS4Hl9carC2qd1c5EX3r3HA0utkaqEfrt0mNte6ygT8oEEqjm2TAZDZD"
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
        "payload":"<GET_STARTED_PAYLOAD>"
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data2)
    print("*"*100)
    print("GET STARTED")
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data1)
    print("*"*100)
    print("GREETING")
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)