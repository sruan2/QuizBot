import os
import json
import requests
import sys
import random
from time import gmtime, strftime


def send_picture(user_id, imageUrl, title="", subtitle=""):
    print("sending pictures")
    if title != "":
        data = {"recipient": {"id": user_id},
                  "message":{
                      "attachment": {
                          "type": "template",
                          "payload": {
                              "template_type": "generic",
                              "elements": [{
                                  "title": title,
                                  "subtitle": subtitle,
                                  "image_url": imageUrl
                              }]
                          }
                      }
                    }
              }
    else:
        data = { "recipient": {"id": user_id},
                "message":{
                  "attachment": {
                      "type": "image",
                      "payload": {
                          "url": imageUrl
                      }
                  }
                }
            }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": os.environ["PAGE_ACCESS_TOKEN"]},
                      data=json.dumps(data),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)    

def send_starting_question(recipient_id):
    starting_part = ["Here's a question for you:",
                     "Let's try this one:",
                     "Could you answer this one for me?",
                     "Let's see if you can get this one:"]  
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
            "text": random.choice(starting_part),
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "I need a hint 🤔",
                    "payload": "I_NEED_A_HINT"
                },
                {
                    "content_type": "text",
                    "title": "I don’t know 😓",
                    "payload": "I_DONT_KNOW"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_a_question(recipient_id, question):
    #ending_part = "\nPlease note that you will earn at most 3 points if you ask for a hint!"
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
            "text": question,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "I need a hint 🤔",
                    "payload": "I_NEED_A_HINT"
                },
                {
                    "content_type": "text",
                    "title": "I don’t know 😓",
                    "payload": "I_DONT_KNOW"
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

def send_hint(recipient_id, main_text, qa_model, qid):
    options = [
                {
                    "content_type": "text",
                    "title": str(qa_model.D1KB[qid]),
                    "payload": "D1KB"
                },
                {
                    "content_type": "text",
                    "title": str(qa_model.D2KB[qid]),
                    "payload": "D2KB"
                },
                {
                    "content_type": "text",
                    "title": str(qa_model.D3KB[qid]),
                    "payload": "D3KB"
                },
                {
                    "content_type": "text",
                    "title": str(qa_model.AKB[qid][0]),
                    "payload": "AKB"
                },
            ]
    random.shuffle(options)
    options.append({
                    "content_type": "text",
                    "title": "I don’t know 😓",
                    "payload": "I_DONT_KNOW"
                })
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
            "text" : main_text,
            "quick_replies": options
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_giveup(recipient_id):

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
            "text": "Are you sure you want to give up?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Yes, answer please.",
                    "payload": "GIVEUP_YES"
                },
                {
                    "content_type": "text",
                    "title": "No, I'll try again!",
                    "payload": "GIVEUP_NO"
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
            "text": "Okay, what would you like to do?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Quiz me 🤓",
                    "payload": "PRACTICE_MODE"
                },
                {
                    "content_type": "text",
                    "title": "I have a question❓",
                    "payload": "CHALLENGE_MODE"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)        


# new added subject selection
def choose_subject_quick_reply(recipient_id, main_text):

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
                    "title": "Physics 🚗",
                    "payload": "PHYSICS"
                },
                {
                    "content_type": "text",
                    "title": "Chemistry ⚗️",
                    "payload": "CHEMISTRY"
                },
                {
                    "content_type": "text",
                    "title": "Biology 🔬",
                    "payload": "BIOLOGY"
                },
                {
                    "content_type": "text",
                    "title": "Geology ⛰",
                    "payload": "GEOLOGY"
                },
                {
                    "content_type": "text",
                    "title": "Random 🎲",
                    "payload": "RANDOM"                
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)  

def send_correct_answer(recipient_id, QID, standard_answer):

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
            "text": "The correct answer is " + "\""+standard_answer+"\"",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Why?",
                    "payload": "WHY"
                },
                {
                    "content_type": "text",
                    "title": "Next question 💪",
                    "payload": "NEXT_QUESTION"
                },
                {
                    "content_type": "text",
                    "title":"Switch Subject!",
                    "payload":"SWITCH_SUBJECT"
                },
                {
                    "content_type": "text",
                    "title": "Wait, I'm right 😡",
                    "payload": "REPORT_BUG"
                },                 
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_explanation(recipient_id, explanation):
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
            "text": explanation,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Next question 💪",
                    "payload": "NEXT_QUESTION"
                },
                {
                    "content_type": "text",
                    "title": "Switch Subject!",
                    "payload": "SWITCH_SUBJECT"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_bugreport(recipient_id, text):
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
            "text": text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Next question 💪",
                    "payload": "NEXT_QUESTION"
                },
                {
                    "content_type": "text",
                    "title": "Switch Subject!",
                    "payload": "SWITCH_SUBJECT"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)        

def send_reminder(list):
    for recipient_id, user_name in [('1805880356153906', 'Nathan')]:
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
                "text": user_name + ", you haven't talked to me for more than a day, would you like to continue the conversation with me now?",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Continue 💪",
                        "payload": "CONTINUE"
                    }
                ]
            }
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)    
        else:
            print("[QUIZBOT] PID " + str(os.getpid())+": Sent Reminder To " + str(user_name) + " With ID " + str(recipient_id) + " At " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

def send_why2_quickreply(recipient_id, support_sentence):
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
                            "title":"Practice Mode "+u'\u270F',
                            "type":"postback",
                            "payload":"PRACTICE_MODE"
                        },
                        {
                            "title":"Challenge Mode "+u'\uD83D\uDE3A',
                            "type":"postback",
                            "payload":"CHALLENGE_MODE"
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
                "text":"Welcome to QuizBot created by Stanford!"
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