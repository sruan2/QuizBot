import os
import sys
import json
import predict_reply
import visualize_sherry
import sqlite3
from random import randint
#from thread_settings import PersistentMenu, PersistentMenuItem, MessengerProfile

import requests
from flask import Flask, request


tfidf = visualize_sherry.tfidfTransform()

conn = sqlite3.connect('tutorial.db')
c = conn.cursor()
app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test():
    return "test", 200

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    print("\nwebhook\n")

    # endpoint for processing incoming messaging events

    data = request.get_json()
    #log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            print("\n\entry\n")

            
            if entry.get("messaging"):
                for messaging_event in entry["messaging"]:
                    print("\n\messaging_event\n")

                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        print("sender ID is: "+sender_id)
                        print("recipient ID is: "+recipient_id)
                        
                        if sender_id == "1497174250389598": #chatbot
                            return "irrelavant ID", 200
                        
                        #send_message(sender_id, "Your sender ID is: "+sender_id)
                        if not "text" in messaging_event["message"]:
                            return "key error", 200
                            
                        message_text = messaging_event["message"]["text"]  # the message's text
 
                        # create an entry in app.session and give the first random question
                        if not sender_id in app.session:
                            print("first time user"+"="*50)
                            question, QID = tfidf.pickRandomQuestion()
                            app.session[sender_id] = {"QID": QID, "total_score": 0}
                            data_entry(sender_id, "Sherry Ruan", 0)
                            send_message(sender_id, "Question."+str(QID)+": "+question)

                        else:
                            QID = app.session[sender_id]["QID"]
                            # print("\n-2- QID is: "+str(tfidf.QID)+"\n")
                            if message_text == "Next Question" or message_text == "Got it, next!":
                                question, QID = tfidf.pickRandomQuestion()
                                app.session[sender_id]["QID"] = QID
                                send_message(sender_id, "Question."+str(QID)+": "+question)
                                print("\n-3- QID is: "+str(QID)+"\n")

                            elif message_text[:4] == "Why?":
                                send_gotit_quickreply(sender_id, QID)

                            elif message_text == "Check Total Score":
                                send_message(sender_id, "Your accumulated score is "+str(app.session[sender_id]["total_score"]))

                            elif message_text == "Leaderboard":
                                print("*"*100)
                                print("LEADERBOARD")
                                read_from_db()


                            else: # user's respons in natural language    
                                print("not first time"+"="*50)
                                standard_answer, score = tfidf.computeScore(message_text, QID)
                                send_message(sender_id, "Your score is: "+str(score))
                                app.session[sender_id]["total_score"] += score
                                update_db(sender_id, score)
                                
                                # Add a why button to show the supporting sentence
                                # you can use a dict instead of a Button class
                                #
                                send_why_quickreply(sender_id, QID, standard_answer)

                            

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        sender_id = messaging_event["sender"]["id"]        
                        recipient_id = messaging_event["recipient"]["id"]  
                        
                        if sender_id == "1497174250389598": #chatbot
                            return "irrelavant ID", 200
                        message_text = messaging_event["postback"]["title"] # the button's payload
                         
                        log("Inside postback")
                        message_text = message_text.lower()
                        print(message_text)
                        print("#"*100)


                        if message_text == "get started":
                            send_ready_go(sender_id, "Hi! Welcome! I'm your personal tutor Mr.Q and I'm here to help you master science! Ready? Go!")
                            
                            

                        elif message_text == "check total score":
                            score = app.session[sender_id]["total_score"]
                            send_message(sender_id, "Your total score is "+str(score)+". Keep moving!") 

                        elif message_text == "check leaderboard":
                            score = app.session[sender_id]["total_score"]
                            send_message(sender_id, "Your total score is "+str(score)+". Keep moving!") 

                        elif message_text == "yup ready":
                            send_mode_quick_reply(sender_id, "Now tell me which mode you would like to choose:"+u'\uD83D\uDC47')

                        elif message_text == "quiz mode":
                            # create an entry in app.session and give the first random question
                            print("first time user"+"="*50)
                            question, QID = tfidf.pickRandomQuestion()
                            app.session[sender_id] = {"QID": QID, "total_score": 0}
                            data_entry(sender_id, "Sherry Ruan", 0)
                            send_message(sender_id, "Question."+str(QID)+": "+question)

                        

    return "ok", 200



def send_message(recipient_id, message_text):

    # print("="*100)
    # print("sent a message!")

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

# why button
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
                    "payload": "yup ready"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

# why button
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
                    "title": "Quiz Mode "+u'\u270F',
                    "payload": "none"
                },
                {
                    "content_type": "text",
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

# why button
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
            "text": "Answer." +str(QID) + ": "+standard_answer,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Why?",
                    "payload": "WHY_"+str(QID)
                },
                {
                    "content_type": "text",
                    "title": "Next Question",
                    "payload": "NEXT_QUESTION"
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

def send_gotit_quickreply(recipient_id, QID):

    log("sending GOTIT button to {recipient}: {text}".format(recipient=recipient_id, text=str(QID)))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    support_sentence = tfidf.get_support(QID)[:600]
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": "Support." +str(QID) + ": "+support_sentence,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Got it, next!",
                    "payload": "WHY_"+str(QID)
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text) 

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

def predict(incoming_msg):
    return predict_reply.classify(incoming_msg);

# SQLite
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(id TEXT, username TEXT, score REAL)')
    print('*'*50)
    print("SQLite: table created")

def data_entry(uid, username, score):
    c.execute("INSERT INTO stuffToPlot (id, username, score) VALUES (?, ?, ?)", (uid, username, score))
    conn.commit()
    print('*'*50)
    print("SQLite: data entered")
    # c.close()
    # conn.close()

def update_db(uid, current_score):
    c.execute('SELECT score FROM stuffToPlot WHERE id = ?', (uid,))
    score = c.fetchall()[0][0]
    print("*"*100)
    print("score is " + str(score))
    print("uid is" + str(uid))
    score += current_score
    c.execute('UPDATE stuffToPlot SET score = ? WHERE id = ?', (score, uid))
    conn.commit()

def read_from_db():
    c.execute('SELECT username, score FROM stuffToPlot')
    for row in c.fetchall():
        print row

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
                  },
                ]
              },
              {
                "type":"web_url",
                "title":"Invite Friends! "+u'\U0001F604',
                "url":"https://www.facebook.com/sharer/sharer.php?u=https%3A//www.facebook.com/quizzzbot/",
                "webview_height_ratio":"full"
              },
              {
                "title":"Check Total Score",
                "type":"postback",
                "payload":"MENU_SCORE"
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
    }
    headers = {
        "Content-Type": "application/json"
    }
    data1 = json.dumps({
        "greeting":[
          {
            "locale":"default",
            "text":"Hello!"
          }, {
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



############ SET UP ############
def setup_app(app):
    tfidf.appendQuestionKB('SciQdataset-23/question_file.txt')
    tfidf.appendSupportKB('SciQdataset-23/support_file.txt')
    tfidf.appendCorrectAnswerKB('SciQdataset-23/correct_answer_file.txt')
    app.session = {}
    create_table()
    greeting()
    persistent_menu()
    

setup_app(app)

if __name__ == '__main__':
    app.run(debug=True)

    # send_message(sender_id, str("Received. I'm here!"))
    # print(predict(raw_input("Enter something")))
    



    
