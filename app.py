import os
import sys
import json
import tfidf
import sqlite3 as sql
from random import randint
from time import gmtime, strftime

import requests
from flask import Flask, request


tfidf = tfidf.tfidfTransform('model_pre_trained/model_d2v_v1')


#conn = sqlite3.connect('QUIZBOT.db')
#c = conn.cursor()

# print "Opened database successfully";


# conn.execute('CREATE TABLE score (user_id INTEGER, score DECIMAL')
# print "Table created successfully";
# conn.close()



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

@app.route('/', methods=['GET'])
def get_user_profile(recipient_id):
    # based on user id retrive user name
    # could protentially retive more user profile, e.g. profile_pic, locale, timezone, gender, last_ad_referral, etc.
    log("getting user profile from user_id: {recipient}".format(recipient=recipient_id))

    r = requests.get("https://graph.facebook.com/v2.6/{psid}?fields=first_name,last_name,gender&access_token={token}".format(psid=recipient_id,token=os.environ["PAGE_ACCESS_TOKEN"]))
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        return
    data = json.loads(r.text)
    return data

@app.route('/', methods=['POST'])
def webhook():

    print("\nwebhook\n")

    # endpoint for processing incoming messaging events

    data = request.get_json()
    
    if data["object"] == "page":
        for entry in data["entry"]:
            print("\n\entry\n")

            if entry.get("messaging"):
                for messaging_event in entry["messaging"]:
                    print("\n\messaging_event\n")

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    sender_id = messaging_event["sender"]["id"]   
                    # sender_name = messaging_event["sender"]["name"]     
                    recipient_id = messaging_event["recipient"]["id"]  

                    if sender_id == "1497174250389598": #chatbot
                        return "irrelavant ID", 200

                    if show_status(sender_id) != -1 and messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        # sender_id = messaging_event["sender"]["id"]   
                        # # sender_name = messaging_event["sender"]["name"]     
                        # recipient_id = messaging_event["recipient"]["id"]  
                        
                        # if sender_id == "1497174250389598": #chatbot
                        #     return "irrelavant ID", 200

                        message_text = messaging_event["postback"]["title"] # the button's payload
                         
                        log("Inside postback")
                        message_text = message_text.lower()
                        #print(message_text)
                        print("#"*100)

                        if message_text == "get started":
                            send_ready_go(sender_id, "Hi! Welcome! I'm your personal tutor Mr.Q and I'm here to help you master science! Ready? Go!"+u'\uD83D\uDE0A')
                            
                        elif message_text == "check total score":
                            score = show_score(sender_id)
                            send_gotit_quickreply(sender_id, "Your total score is "+str(score)+". Keep moving!") 

                        elif message_text == "check leaderboard":
                            records = show_top_10()
                            sentence = ("\n").join(["No." + str(i + 1) + " " + str(records[i][0]+' '+records[i][1]) + ": " + str(records[i][2]) for i in range(len(records))])
                            send_gotit_quickreply(sender_id, "Leaderboard: \n" + sentence) 
                        elif message_text[0:9] == "quiz mode":
                            #app.session[sender_id]["answering"] = False
                            if show_status(sender_id):
                                question, QID = tfidf.pickRandomQuestion()
                                update_status(sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,time)
                            else: 
                                question = tfidf.pickLastQueston(QID)
                            #app.session[sender_id] = {"QID": QID, "total_score": 0}
                            #data_entry(sender_id, "Sherry Ruan", 0)
                            send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

                        elif message_text == "Mathematic":
                            question, QID = tfidf.pickRandomQuestion()    
                            send_message(sender_id, "Question."+str(QID)+": "+question)
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            insert_question(sender_id,QID,time)

                        # look for next similar question based off the pre-trained model
                        elif message_text == "next question":
                            #sender_id]["answering"] = False
                            if show_status(sender_id):
                                question, QID = tfidf.pickNextSimilarQuestion(show_last_qid(sender_id))
                                update_status(sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,time)
                            else: 
                                question = tfidf.pickLastQueston(QID)
                            #app.session[sender_id] = {"QID": QID}
                            send_message(sender_id, "Question."+str(QID)+": "+question)

                       
                        # switch subject means randomly pick another one
                        elif message_text == "switch subject":
                            #app.session[sender_id]["answering"] = False
                            question, QID = tfidf.pickRandomQuestion()
                            #app.session[sender_id] = {"QID": QID}
                            send_message(sender_id, "Question."+str(QID)+": "+question)   
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())  
                            insert_question(sender_id,QID,time)                      


                        elif message_text[0:9] == "answering":
                            #app.session[sender_id]["answering"] = True
                            #data_entry(sender_id, "Sherry Ruan", 0)
                            send_message(sender_id, "I'm here to answer your questions! Just type your question below :-) ")


                    elif messaging_event.get("message"):  # someone sent us a message
                        # sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        # recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        print("sender ID is: "+sender_id)
                        print("recipient ID is: "+recipient_id)
                        
                        # if sender_id == "1497174250389598": #chatbot
                        #     return "irrelavant ID", 200
                        
                        #send_message(sender_id, "Your sender ID is: "+sender_id)
                        if not "text" in messaging_event["message"]:
                            return "key error", 200
                            
                        message_text = messaging_event["message"]["text"]  # the message's text

                        data = get_user_profile(sender_id)
                        sender_firstname = data['first_name']
                        sender_lastname = data['last_name']
                        sender_gender = data['gender']

                        if not int(sender_id) in show_user_id_list():

                            print("first time user"+"="*50)
                            #app.session[sender_id] = {"QID": 0, "total_score": 0, "answering": False}
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            insert_user(sender_id,sender_firstname,sender_lastname,sender_gender,1)
                            insert_score(sender_id, -1,message_text,0,time)
                            send_mode_quick_reply(sender_id, "Now tell me which mode you would like to choose:"+u'\uD83D\uDC47') 

                        else:
                            QID = show_last_qid(sender_id)


                            if message_text == "Switch Subject" :
                                #app.session[sender_id]["answering"] = False
                                question, QID = tfidf.pickRandomQuestion()
                                #app.session[sender_id]["QID"] = QID
                                send_message(sender_id, "Here's a question from different subject: "+str(QID+". ")+question)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,time)
                                print("\n-3- QID is: "+str(QID)+"\n")

                            elif message_text == "Quiz Mode "+u'\u270F':
                                #app.session[sender_id]["answering"] = False
                                if show_status(sender_id):
                                    question, QID = tfidf.pickRandomQuestion()
                                    update_status(sender_id, 0)
                                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    insert_question(sender_id,QID,time)
                                else: 
                                    question = tfidf.pickLastQueston(QID)
                                #app.session[sender_id] = {"QID": QID, "total_score": 0}
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                                print("\n-4- QID is: "+str(QID)+"\n")                                 

                            elif message_text == "Next Question" or message_text == "Got it, next!" :
                                #app.session[sender_id]["answering"] = False

                                if show_status(sender_id):
                                    question, QID = tfidf.pickNextSimilarQuestion(show_last_qid(sender_id))
                                    update_status(sender_id, 0)
                                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    insert_question(sender_id,QID,time)
                                    #app.session[sender_id] = {"QID": QID}
                                else: 
                                    question = tfidf.pickLastQueston(QID)
                                send_message(sender_id, "Next Question "+str(QID)+": "+question)
                                print("\n-5- QID is: "+str(QID)+"\n") 

                            # I comment out this part as there is bug here
                            # elif app.session[sender_id]["answering"] == True:
                            #     answer = tfidf.Featurize(message_text)
                            #     send_message(sender_id, answer)    

                            elif message_text[:4] == "Why?":
                                support_sentence = tfidf.get_support(QID)[:600]
                                send_gotit_quickreply(sender_id, "Here's an explanation: "+ support_sentence)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_score(sender_id,QID,"why",0,time)

                            elif message_text == "Check Total Score":
                                print ("&"*50)
                                print (str(show_score(sender_id)))
                                send_gotit_quickreply(sender_id, "Your accumulated score is "+str(show_score(sender_id)))

                            else: # user's respons in natural language    
                                print("not first time"+"="*50)
                                standard_answer, score = tfidf.computeScore(message_text, QID)
                                send_message(sender_id, "Your score this round is "+str(score))
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                #total_score = show_score(sender_id) + score
                                insert_score(sender_id,QID,message_text,score,time)
                                #update_db(sender_id, score)
                                send_why_quickreply(sender_id, QID, standard_answer)    
                                update_status(sender_id, 1) 


    return "ok", 200



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
                    "title": "Mathematic",
                    "payload": "none"
                },
                {
                    "content_type": "text",
                    "title": "Physics",
                    "payload": "none"
                },
                {
                    "content_type": "text",
                    "title": "Chemistry",
                    "payload": "none"
                },
                {
                    "content_type": "text",
                    "title": "Biology",
                    "payload": "none"
                },
                {
                    "content_type": "text",
                    "title": "Geography",
                    "payload": "none"
                },
                {
                    "content_type": "text",
                    "title": "Hisotry",
                    "payload": "none"
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
                    "title":"Switch Subject",
                    "payload":"SWITCH_SUBJUECT"
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
                    "payload": "WHY"
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

# def predict(incoming_msg):
#     return predict_reply.classify(incoming_msg);

###################### SQLite ######################
# def create_table():
#     c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(id TEXT, username TEXT, score REAL)')
#     print('*'*50)
#     print("SQLite: table created")

# def data_entry(uid, username, score):
#     c.execute("INSERT INTO stuffToPlot (id, username, score) VALUES (?, ?, ?)", (uid, username, score))
#     conn.commit()
#     print('*'*50)
#     print("SQLite: data entered")
#     # c.close()
#     # conn.close()

# def update_db(uid, current_score):
#     c.execute('SELECT score FROM stuffToPlot WHERE id = ?', (uid,))
#     score = c.fetchall()[0][0]
#     print("*"*100)
#     print("score is " + str(score))
#     print("uid is" + str(uid))
#     score += current_score
#     c.execute('UPDATE stuffToPlot SET score = ? WHERE id = ?', (score, uid))
#     conn.commit()

# def read_from_db():
#     c.execute('SELECT username, score FROM stuffToPlot')
#     for row in c.fetchall():
#         print row


# insert user info
def insert_user(user_id,user_firstname,user_lastname,user_gender,user_status):
    if request.method == 'POST':
        try:
            with sql.connect("QUIZBOT.db") as con:
                cur = con.cursor()            
                cur.execute("INSERT INTO users (user_id,user_firstname,user_lastname,user_gender,user_status) VALUES (?,?,?,?,?)",(user_id,user_firstname,user_lastname,user_gender,user_status,))           
                con.commit()
                print ("User record successfully added")
        except:
            con.rollback()
            print ("error in inserting user reocrd operation")
        finally:
            con.close()    

# update user question-answer loop status
def update_status(user_id,status):
    if request.method == 'POST':
        try:
            with sql.connect("QUIZBOT.db") as con:
                cur = con.cursor()            
                cur.execute("update users set user_status = ? where user_id = ?",(status, user_id,))           
                con.commit()
                print ("update status successfully added")
        except:
            con.rollback()
            print ("error in updating user status operation")
        finally:
            con.close()      

def show_status(user_id):
    con = sql.connect("QUIZBOT.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select user_status from users where user_id = ?", (user_id,))

    rows = cur.fetchall()
    if len(rows) != 0:
        return rows[0][0] 
    else:
        return -1

# insert user score
def insert_score(user_id,qid,answer,score,time):
    if request.method == 'POST':
        try:
            with sql.connect("QUIZBOT.db") as con:
                cur = con.cursor()            
                cur.execute("INSERT INTO scores (user_id,qid,answer,score,r_time) VALUES (?,?,?,?,?)",(user_id,qid,answer,score,time,))           
                con.commit()
                print ("Score record successfully added")
        except:
            con.rollback()
            print ("error in inserting score operation")
        finally:
            con.close()

# insert asked questions
def insert_question(user_id,qid,time):
    if request.method == 'POST':
        try:
            with sql.connect("QUIZBOT.db") as con:
                cur = con.cursor()            
                cur.execute("INSERT INTO questions (user_id,qid,r_time) VALUES (?,?,?)",(user_id,qid,time,))           
                con.commit()
                print ("Questions record successfully added")
        except:
            con.rollback()
            print ("error in inserting question operation")
        finally:
            con.close()

def show_user_id_list():
    con = sql.connect("QUIZBOT.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select user_id from users")

    rows = cur.fetchall()
    return [x[0] for x in rows]   


# retrieve score based on user_id 
def show_score(user_id):
    con = sql.connect("QUIZBOT.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select sum(score) from scores group by user_id having user_id = ?", (user_id,))

    rows = cur.fetchall();
    return rows[0][0] if len(rows) > 0 else 0

# retrieve score based on user_id 
def show_last_qid(user_id):
    con = sql.connect("QUIZBOT.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select qid from questions where user_id = ? order by id desc limit 1", (user_id,))

    rows = cur.fetchall();
    return rows[0][0] if len(rows) > 0 else 0

# show top 10 in leaderboard
def show_top_10():
    con = sql.connect("QUIZBOT.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select t2.user_firstname,t2.user_lastname,t1.sc from \
        (select user_id, sum(score) as sc from scores group by user_id order by sc desc limit 10) t1 join users t2 on t2.user_id = t1.user_id")

    rows = cur.fetchall();
    return rows


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
    print("\nstart\n")
    tfidf.appendQuestionKB('SciQdataset-23/question_file_2.txt')
    tfidf.appendSupportKB('SciQdataset-23/support_file_2.txt')
    tfidf.appendCorrectAnswerKB('SciQdataset-23/correct_answer_file_2.txt')
    app.session = {}
    # create_table()
    greeting()
    print("\nafter greeting\n")
    persistent_menu()
    

setup_app(app)

if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem', '/etc/letsencrypt/live/smartprimer.org/privkey.pem')
    app.run(host='0.0.0.0', threaded=False, debug=True, port=443, ssl_context=context)

    # send_message(sender_id, str("Received. I'm here!"))
    # print(predict(raw_input("Enter something")))
    
