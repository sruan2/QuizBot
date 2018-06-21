import os
import json
import requests
import sys
import random
from time import gmtime, strftime
from utils import pretty_print


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
                    "payload": "BUTTON_I_NEED_A_HINT"
                },
                {
                    "content_type": "text",
                    "title": "I don’t know 😓",
                    "payload": "BUTTON_I_DONT_KNOW"
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
                    "payload": "BUTTON_I_NEED_A_HINT"
                },
                {
                    "content_type": "text",
                    "title": "I don’t know 😓",
                    "payload": "BUTTON_I_DONT_KNOW"
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
    
    # send text message
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
   
    # display sender actions
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": "typing_on"
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
                    "payload": "BUTTON_SURE"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_hint(recipient_id, main_text, qa_model, qid):
    message_text = ""
    options = []
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
        message_text += "<"
        message_text += str(i+1) 
        message_text += "> "
        message_text += str(options[i]["title"])
        message_text += "\n"
    
    options.append({
                    "content_type": "text",
                    "title": "I don’t know 😓",
                    "payload": "BUTTON_I_DONT_KNOW"
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
            "text" : main_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text" : message_text,
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
                    "payload": "BUTTON_GIVEUP_YES"
                },
                {
                    "content_type": "text",
                    "title": "No, I'll try again!",
                    "payload": "BUTTON_GIVEUP_NO"
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
                    "payload": "BUTTON_YUP_IM_READY"
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
            # "text": "Okay, what would you like to do?",
            "text": "Let’s get started 🚀",    
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Quiz me 🤓",
                    "payload": "BUTTON_PRACTICE_MODE"
                }
                # {
                #     "content_type": "text",
                #     "title": "I have a question❓",
                #     "payload": "BUTTON_CHALLENGE_MODE"
                # }
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
                # {
                #     "content_type": "text",
                #     "title": "Physics🚗",
                #     "payload": "BUTTON_PHYSICS"
                # },
                # {
                #     "content_type": "text",
                #     "title": "Chemistry⚗️",
                #     "payload": "BUTTON_CHEMISTRY"
                # },
                # {
                #     "content_type": "text",
                #     "title": "Biology🔬",
                #     "payload": "BUTTON_BIOLOGY"
                # },
                # {
                #     "content_type": "text",
                #     "title": "Geology⛰",
                #     "payload": "BUTTON_GEOLOGY"
                # },
                {
                    "content_type": "text",
                    "title": "Science🔬",
                    "payload": "BUTTON_SCIENCE"
                },
                {
                    "content_type": "text",
                    "title": "GRE🔠",
                    "payload": "BUTTON_GRE"
                },
                {
                    "content_type": "text",
                    "title": "Safety🛠",
                    "payload": "BUTTON_SAFETY"
                },
                {
                    "content_type": "text",
                    "title": "Random🎲",
                    "payload": "BUTTON_RANDOM"
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
                    "payload": "BUTTON_WHY"
                },
                {
                    "content_type": "text",
                    "title": "Next question 💪",
                    "payload": "BUTTON_NEXT_QUESTION"
                },
                {
                    "content_type": "text",
                    "title":"Switch Subject!",
                    "payload":"BUTTON_SWITCH_SUBJECT"
                },
                {
                    "content_type": "text",
                    "title": "Wait, I'm right 😡",
                    "payload": "BUTTON_REPORT_BUG"
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_reminder(list):

    for recipient_id, user_name in list:
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
                        "payload": "BUTTON_CONTINUE"
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


def send_gotit_quickreply(recipient_id, sentence, flag):
    # if flag is True, that's leaderboard view, otherwise is general
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    result = {
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

    }
    if flag:
        result["message"]["quick_replies"][0]["title"] = "Got it, quiz me more!"
    data = json.dumps(result)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)



############ persistent menu ############
def persistent_menu(access_token):
    params = {
        "access_token": access_token
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

                # Liwei: Remove this functionality for user study
                # {
                #     "title":"Change Mode",
                #     "type":"nested",
                #     "call_to_actions":[
                #         {
                #             "title":"Practice Mode "+u'\u270F',
                #             "type":"postback",
                #             "payload":"MENU_PRACTICE_MODE"
                #         },
                #         {
                #             "title":"Challenge Mode "+u'\uD83D\uDE3A',
                #             "type":"postback",
                #             "payload":"MENU_CHALLENGE_MODE"
                #         }
                #         ]
                # },
                {
                    "title":"Change Subject",
                    "type":"nested",
                    "call_to_actions":[
                        {
                            "title":"Science🔬",
                            "type":"postback",
                            "payload":"BUTTON_SCIENCE"
                        },
                        {
                            "title":"GRE🔠",
                            "type":"postback",
                            "payload":"BUTTON_GRE"
                        },
                        {
                            "title":"Safety🛠",
                            "type":"postback",
                            "payload":"BUTTON_SAFETY"
                        },
                        {
                            "title":"Random🎲",
                            "type":"postback",
                            "payload":"BUTTON_RANDOM"
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
                    }
                    # Liwei: Remove this functionality for user study
                    # {
                    #     "title":"Check Leaderboard",
                    #     "type":"postback",
                    #     "payload":"MENU_LEADERBOARD"
                    # }
                    ]
                }
                # Liwei: Remove this functionality for user study
                # {
                #     "type":"web_url",
                #     "title":"Invite Friends! "+u'\U0001F604',
                #     "url":"https://www.facebook.com/sharer/sharer.php?u=https%3A//www.facebook.com/quizzzbot/",
                #     "webview_height_ratio":"full"
                # }
            ]
          }
        ]
    })
    pretty_print("Persistent menu loaded", mode="Message")
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


############ greeting ############
def send_greeting(access_token):
    params = {
        "access_token":access_token
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
                "text":"Hi, we are a group of researchers from Stanford University Computer Science Department. Thank you for trying out the QuizBot!"
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
    print(str(message))
    sys.stdout.flush()
