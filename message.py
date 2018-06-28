import os
import json
import requests
import sys
import random
import time
from time import gmtime, strftime
from utils import pretty_print

def send_get_it(recipient_id, main_text, sleep_time, payload):
    time.sleep(sleep_time)
    for msg in main_text[:-1]:
        send_message(recipient_id, msg)
        time.sleep(sleep_time)

    content = ["Got it💡", "Got it 👊🏼", "Got it 📍", "Sure ✅", "Tap me👇🏼", "Yes, continue 👉🏼", "Next 💪🏼", "Continue 👉🏼", "Continue ▶️", "Next ➡️"]
    random.shuffle(content)

    send_typing_action(recipient_id)

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
            "text": main_text[-1],
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": content[0],
                    "payload": payload
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)



def send_if_new(recipient_id, main_text):
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
                    "title": "I'm a new user.",
                    "payload": "GET_READY"
                },
                {
                    "content_type": "text",
                    "title": "Resume Learning",
                    "payload": "BUTTON_GOT_IT_NEXT"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)



def send_typing_action(recipient_id):
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
        "sender_action": "typing_on"
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)   
   
def send_if_user_manual(recipient_id):
    send_message(recipient_id, "Do you want me to guide you through how this works? 🦉")

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
            "text": main_text[-1],
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Yes, user manual!",
                    "payload": "BUTTON_USER_MANUAL_1"
                },
                {
                    "content_type": "text",
                    "title": "Skip user manual.",
                    "payload": "GET_STARTED_PAYLOAD_5"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)



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
                {
                    "content_type": "text",
                    "title": "Science🔬",
                    "payload": "BUTTON_SCIENCE"
                },
                {
                    "content_type": "text",
                    "title": "GRE 🔠",
                    "payload": "BUTTON_GRE"
                },
                {
                    "content_type": "text",
                    "title": "Safety🛠",
                    "payload": "BUTTON_SAFETY"
                },
                {
                    "content_type": "text",
                    "title": "Random 🎲",
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
                }
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
                {
                    "title":"Change Subject 🔀",
                    "type":"nested",
                    "call_to_actions":[
                        {
                            "title":"Science🔬",
                            "type":"postback",
                            "payload":"BUTTON_SCIENCE"
                        },
                        {
                            "title":"GRE 🔠",
                            "type":"postback",
                            "payload":"BUTTON_GRE"
                        },
                        {
                            "title":"Safety🛠",
                            "type":"postback",
                            "payload":"BUTTON_SAFETY"
                        },
                        {
                            "title":"Random 🎲",
                            "type":"postback",
                            "payload":"BUTTON_RANDOM"
                        }
                    ]
                },
                {
                    "title":"Check Total Score 📝",
                    "type":"postback",
                    "payload":"MENU_SCORE"
                },
                {
                    "title":"More📍",
                    "type":"nested",
                    "call_to_actions":[
                        {
                            "title":"Report Bug 🔧",
                            "type":"postback",
                            "payload":"BUTTON_REPORT_BUG"
                        },
                        {
                            "title":"User Manual 👩🏻‍💻👨🏻‍💻",
                            "type":"postback",
                            "payload":"BUTTON_USER_MANUAL_1"
                        },
                        {
                            "title":"About QuizBot 🔖",
                            "type":"postback",
                            "payload":"BUTTON_ABOUT_QUIZBOT"
                        },
                        {
                            "title":"Contact ☎️",
                            "type":"postback",
                            "payload":"BUTTON_CONTACT"
                        }               
                    ]
                }
                # {
                #     "title":"Report Bug 🔧",
                #     "type":"postback",
                #     "payload":"BUTTON_REPORT_BUG"
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
    # data1 = json.dumps({
    #     "greeting":[
    #         {
    #             "locale":"default",
    #             "text":"Hello!"
    #         },
    #         {
    #             "locale":"en_US",
    #             "text":"Hi, we are a group of researchers from Stanford University Computer Science Department. Thank you for trying out the QuizBot!"
    #         }
    #     ]
    # })
    data2 = json.dumps({
        "get_started":{
        "payload":"GET_INTRO_1"
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data2)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

    # r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data1)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()
