import os
import sys
import json
sys.path.append("/home/venv/quizbot/QuizBot/")

import QAKnowledgebase
import QAModel
#import sqlite3 as sql
from flask_mysqldb import MySQL
from random import randint
from time import gmtime, strftime
#from similarity_model.princeton_sif import sif_sentence_similarity
from similarity_model import tfidf

import requests
from flask import Flask, request


#tfidf_ins = tfidf.tfidfTransform('model_pre_trained/model_d2v_v1')


#conn = sqlite3.connect('QUIZBOT.db')
#c = conn.cursor()

# print "Opened database successfully";


# conn.execute('CREATE TABLE score (user_id INTEGER, score DECIMAL')
# print "Table created successfully";
# conn.close()



app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ubuntu'
app.config['MYSQL_PASSWORD'] = 'smartprimer'
app.config['MYSQL_DB'] = 'QUIZBOT'
mysql.init_app(app)

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

                    if sender_id == "1805880356153906": #chatbot
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
                            #update_status(sender_id, 0)
                            #time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            #insert_question(sender_id,QID,time)

                            #app.session[sender_id] = {"QID": QID, "total_score": 0}
                            #data_entry(sender_id, "Sherry Ruan", 0)
                            send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

                        elif message_text == "physics":
                            question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                            update_status(sender_id, 0)
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            insert_question(sender_id,QID,time)
                            #app.session[sender_id] = {"QID": QID}
                            send_message(sender_id, "Question."+str(QID)+": "+question)

                        elif message_text == "chemistry":
                            question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                            update_status(sender_id, 0)
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            insert_question(sender_id,QID,time)
                            #app.session[sender_id] = {"QID": QID}
                            send_message(sender_id, "Question."+str(QID)+": "+question)

                        elif message_text == "biology":
                            question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                            update_status(sender_id, 0)
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            insert_question(sender_id,QID,time)
                            #app.session[sender_id] = {"QID": QID}
                            send_message(sender_id, "Question."+str(QID)+": "+question)

                        elif message_text == "geology":
                            question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                            update_status(sender_id, 0)
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            insert_question(sender_id,QID,time)
                            #app.session[sender_id] = {"QID": QID}
                            send_message(sender_id, "Question."+str(QID)+": "+question)

                        elif message_text == "random":
                            question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                            update_status(sender_id, 0)
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            insert_question(sender_id,QID,time)
                            #app.session[sender_id] = {"QID": QID}
                            send_message(sender_id, "Question."+str(QID)+": "+question)

                        elif message_text == 'switch subject' or message_text[:4] == 'sure':
                            send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')


                        # look for next similar question based off the pre-trained model
                        elif message_text == "next question":
                            #sender_id]["answering"] = False
                            if show_status(sender_id):
                                last_subject = show_last_qid_subject(sender_id)[1]
                                if last_subject == 'random' or last_subject == 'no record':
                                    question, QID = qa_md.pickRandomQuestion()
                                else:
                                    question, QID = qa_md.pickSubjectRandomQuestion(last_subject)
                                update_status(sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,last_subject,time)
                            else: 
                                QID = show_last_qid_subject(sender_id)[0]
                                question = qa_md.pickLastQuestion(QID)
                            #app.session[sender_id] = {"QID": QID}
                            send_message(sender_id, "Question."+str(QID)+": "+question)

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
                            QID,SUBJECT = show_last_qid_subject(sender_id)

                            if message_text == "Quiz Mode "+u'\u270F':
                                #app.session[sender_id]["answering"] = False
                                    # question, QID = qa_md.pickRandomQuestion()
                                    # update_status(sender_id, 0)
                                send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47') 
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,'-11','SWITCH_SUBJUECT',time)
                                print("\n-4- QID is: "+str(QID)+"\n")                                 

                            elif message_text == "Next Question" or message_text == "Got it, next!" or message_text[:4] == "Sure":
                                #app.session[sender_id]["answering"] = False

                                if show_status(sender_id):
                                    last_subject = show_last_qid_subject(sender_id)[1]
                                    if last_subject == 'random' or last_subject == 'no record':
                                        question, QID = qa_md.pickRandomQuestion()
                                    else:
                                        question, QID = qa_md.pickSubjectRandomQuestion(last_subject)
                                    update_status(sender_id, 0)
                                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    insert_question(sender_id,QID,last_subject,time)
                                else: 
                                    QID = show_last_qid_subject(sender_id)[0]
                                    question = qa_md.pickLastQuestion(QID)
                                #app.session[sender_id] = {"QID": QID}
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            # I comment out this part as there is bug here
                            # elif app.session[sender_id]["answering"] == True:
                            #     answer = tfidf.Featurize(message_text)
                            #     send_message(sender_id, answer)    

                            elif message_text[:4] == "Why?":
                                support_sentence = qa_md.getSupport(QID)[:600]
                                #send_gotit_quickreply(sender_id, "Here's an explanation: "+ support_sentence)
                                send_why2_quickreply(sender_id, "Here's an explanation: " + support_sentence)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_score(sender_id,QID,"why",0,time)

                            elif message_text == "Check Total Score":
                                print ("&"*50)
                                print (str(show_score(sender_id)))
                                send_gotit_quickreply(sender_id, "Your accumulated score is "+str(show_score(sender_id)))


                            elif message_text == "Physics":
                                question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                                update_status(sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,message_text.lower(),time)
                                #app.session[sender_id] = {"QID": QID}
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            elif message_text == "Chemistry":
                                question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                                update_status(sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,message_text.lower(),time)
                                #app.session[sender_id] = {"QID": QID}
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            elif message_text == "Biology":
                                question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                                update_status(sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,message_text.lower(),time)
                                #app.session[sender_id] = {"QID": QID}
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            elif message_text == "Geology":
                                question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                                update_status(sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,message_text.lower(),time)
                                #app.session[sender_id] = {"QID": QID}
                                send_message(sender_id, "Question."+str(QID)+": "+question)
                            
                            elif message_text == "Random":
                                question, QID = qa_md.pickRandomQuestion()
                                update_status(sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(sender_id,QID,message_text.lower(),time)
                                #app.session[sender_id] = {"QID": QID}
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            elif message_text.lower() == 'switch subject':
                                send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

                            else: # user's respons in natural language    
                                if not show_status(sender_id):
                                    print("not first time"+"="*50)
                                    #standard_answer, score = tfidf_ins.computeScore(message_text, QID)
                                    standard_answer = qa_md.getAnswer(QID)
                                    #score = qa_sif.compute_score(message_text, QID)
                                    # score = qa_tfidf.compute_score(message_text, QID)
                                    score = qa_sif2.compute_score(message_text, QID)
                                    send_message(sender_id, "Your score this round is "+str(score))
                                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    #total_score = show_score(sender_id) + score
                                    insert_score(sender_id,QID,message_text,score,time)
                                    #update_db(sender_id, score)
                                    send_why_quickreply(sender_id, QID, standard_answer)    
                                    update_status(sender_id, 1) 
                                else:
                                    update_status(sender_id, 1)
                                    send_interesting(sender_id, "Thans sounds interesting. Would you want more quiz questions to practice? I'm here to help")
                                    
                                    #send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')


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
                    "payload": "yup ready"
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
                    "title": "Physics",
                    "payload": "Physics"
                },
                {
                    "content_type": "text",
                    "title": "Chemistry",
                    "payload": "Chemistry"
                },
                {
                    "content_type": "text",
                    "title": "Biology",
                    "payload": "Biology"
                },
                {
                    "content_type": "text",
                    "title": "Geology",
                    "payload": "Geology"
                },
                {
                    "content_type": "text",
                    "title": "Random",
                    "payload": "Random"                
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
                    "title": "Why?",
                    "payload": "WHY_"
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
    print (str(message))
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
            cur = mysql.connection.cursor()           
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
            cur = mysql.connection.cursor()             
            cur.execute("update users set user_status = ? where user_id = ?",(status, user_id,))           
            con.commit()
            print ("update status successfully added")
        except:
            con.rollback()
            print ("error in updating user status operation")
        finally:
            con.close()      

def show_status(user_id):
    con = mysql.connect()
    con.row_factory = mysql.Row

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
            cur = mysql.connection.cursor()              
            cur.execute("INSERT INTO scores (user_id,qid,answer,score,r_time) VALUES (?,?,?,?,?)",(user_id,qid,answer,score,time,))           
            con.commit()
            print ("Score record successfully added")
        except:
            con.rollback()
            print ("error in inserting score operation")
        finally:
            con.close()

# insert asked questions
def insert_question(user_id,qid,subject,time):
    if request.method == 'POST':
        try:
            cur = mysql.connection.cursor()            
            cur.execute("INSERT INTO questions (user_id,qid,subject,r_time) VALUES (?,?,?,?)",(user_id,qid,subject,time,))           
            con.commit()
            print ("Questions record successfully added")
        except:
            con.rollback()
            print ("error in inserting question operation")
        finally:
            con.close()

def show_user_id_list():
    con = mysql.connect()
    con.row_factory = mysql.Row

    cur = con.cursor()
    cur.execute("select user_id from users")

    rows = cur.fetchall()
    return [x[0] for x in rows]   


# retrieve score based on user_id 
def show_score(user_id):
    con = mysql.connect()
    con.row_factory = mysql.Row

    cur = con.cursor()
    cur.execute("select sum(score) from scores group by user_id having user_id = ?", (user_id,))

    rows = cur.fetchall();
    return rows[0][0] if len(rows) > 0 else 0

# retrieve score based on user_id 
def show_last_qid_subject(user_id):
    con = mysql.connect()
    con.row_factory = mysql.Row

    cur = con.cursor()
    cur.execute("select qid,subject from questions where user_id = ? order by id desc limit 1", (user_id,))

    rows = cur.fetchall();
    return (rows[0][0] if len(rows) > 0 else -1, rows[0][1] if len(rows) > 0 else 'no record')

# show top 10 in leaderboard
def show_top_10():
    con = mysql.connect()
    con.row_factory = mysql.Row

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
    # tfidf_ins.appendQuestionKB('SciQdataset-23/question_file_2.txt')
    # tfidf_ins.appendSupportKB('SciQdataset-23/support_file_2.txt')
    # tfidf_ins.appendCorrectAnswerKB('SciQdataset-23/correct_answer_file_2.txt')
    # doc2vec = 'model_pre_trained/model_d2v_v1'
    # question_file = 'SciQdataset-23/question_file_2.txt'
    # support_file = 'SciQdataset-23/support_file_2.txt'
    # answer_file = 'SciQdataset-23/correct_answer_file_2.txt'

    # qa_kb = QAKnowledgebase.QATransform(question_file, support_file, answer_file)
    # qa_md = QAModel.QAModel(qa_kb)
    # qa_doc2vec = QAModel.Doc2VecModel(qa_kb, doc2vec)
    # qa_sif = QAModel.SIFModel(qa_kb)

    #tfidf_ins = tfidf.tfidfTransform(qa_kb, qa_md)
    #app.session = {}
    # create_table()
    greeting()
    print("\nafter greeting\n")
    persistent_menu()

    

setup_app(app)

if __name__ == '__main__':
    # model
    doc2vec = 'model_pre_trained/model_d2v_v1'
    pkl_file = 'model_pre_trained/glove/glove.6B.100d.pkl'
    # qa data
    question_file = 'SciQdataset-23/question_file_2.txt'
    subject_file = 'SciQdataset-23/question_file_2_subject.txt'
    support_file = 'SciQdataset-23/support_file_2.txt'
    answer_file = 'SciQdataset-23/correct_answer_file_2.txt'
    
    qa_kb = QAKnowledgebase.QATransform(question_file, support_file, answer_file, subject_file)
    qa_md = QAModel.QAModel(qa_kb)
    qa_doc2vec = QAModel.Doc2VecModel(qa_kb, doc2vec)
    # qa_sif = QAModel.SIFModel(qa_kb)
    qa_sif2 = QAModel.SIF2Model(qa_kb, pkl_file)
    # qa_tfidf = QAModel.TFIDFModel(qa_kb)



    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem', '/etc/letsencrypt/live/smartprimer.org/privkey.pem')
    app.run(host='0.0.0.0', threaded=True, debug=True, port=8443, ssl_context=context)
    #app.run(port=80,debug=True)
    # send_message(sender_id, str("Received. I'm here!"))
    # print(predict(raw_input("Enter something")))
    
