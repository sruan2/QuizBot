import os
import json
import sys
#sys.path.append("/home/venv/quizbot/QuizBot/")
import QAKnowledgebase
import QAModel
from flask_mysqldb import MySQL
from random import randint
from time import gmtime, strftime
from similarity_model import tfidf
from flask import Flask, request
from message import *


app = Flask(__name__)

# ================== MySQL Setup ==================
mysql = MySQL()
app.config['MYSQL_HOST'] = os.environ["DB_HOST"]
app.config['MYSQL_USER'] = os.environ["DB_USER"]
app.config['MYSQL_PASSWORD'] = os.environ["DB_PASSWORD"]
app.config['MYSQL_DB'] = os.environ["DB"]
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
    log("[QUIZBOT] Getting user profile from user_id: {recipient}".format(recipient=recipient_id))
    r = requests.get("https://graph.facebook.com/v2.6/{psid}?fields=first_name,last_name,gender&access_token={token}".format(psid=recipient_id,token=os.environ["PAGE_ACCESS_TOKEN"]))
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        return
    data = json.loads(r.text)
    return data


@app.route('/', methods=['POST'])
def webhook():

    log("[QUIZBOT] Enter webhook") # endpoint for processing incoming messaging events
    
    data = request.get_json()
    
    if data["object"] == "page":
        for entry in data["entry"]:
            if entry.get("messaging"):
                for messaging_event in entry["messaging"]:

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    sender_id = messaging_event["sender"]["id"]   
                    recipient_id = messaging_event["recipient"]["id"]  

                    if sender_id == os.environ["CHATBOT_ID"]: # return if this message is sent from the chatbot
                        return "Chatbot ID", 200

                    if show_status(sender_id) != -1 and messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message

                        message_text = messaging_event["postback"]["title"].lower() # the button's payload
                         
                        log("[QUIZBOT] Inside postback")

                        respond_to_postback(message_text, mysql)

########### sherry's refactor up here ################

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
                        print (data)
                        sender_firstname = data['first_name']
                        sender_lastname = data['last_name']
                        sender_gender = data['gender']

                        if not int(sender_id) in show_user_id_list():

                            print("first time user"+"="*50)
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            insert_user(mysql, sender_id,sender_firstname,sender_lastname,sender_gender,1)
                            insert_score(mysql, sender_id, -1,message_text,0,time)
                            send_mode_quick_reply(sender_id, "Now tell me which mode you would like to choose:"+u'\uD83D\uDC47') 

                        else:
                            QID,SUBJECT = show_last_qid_subject(sender_id)

                            print ("^"*100)
                            print (message_text)

                            if message_text == "Quiz Mode "+u'\u270F':
                                send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47') 
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(mysql, sender_id,'-11','SWITCH_SUBJUECT',time)
                                print("\n-4- QID is: "+str(QID)+"\n")                                 

                            elif message_text == "Next Question" or message_text == "Got it, next!" or message_text[:4] == "Sure":

                                if show_status(sender_id):
                                    last_subject = show_last_qid_subject(sender_id)[1]
                                    if last_subject == 'random' or last_subject == 'no record':
                                        question, QID = qa_md.pickRandomQuestion()
                                    else:
                                        question, QID = qa_md.pickSubjectRandomQuestion(last_subject)
                                    update_status(mysql, sender_id, 0)
                                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    insert_question(mysql, sender_id,QID,last_subject,time)
                                else: 
                                    QID = show_last_qid_subject(sender_id)[0]
                                    question = qa_md.pickLastQuestion(QID)
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            # I comment out this part as there is bug here
                            # elif app.session[sender_id]["answering"] == True:
                            #     answer = tfidf.Featurize(message_text)
                            #     send_message(sender_id, answer)    

                            elif "Yup! I'm ready!" in message_text:
                                update_status(mysql, sender_id, 1)
                                send_mode_quick_reply(sender_id, "Now tell me which mode you would like to choose:"+u'\uD83D\uDC47') 


                            elif message_text[:4] == "Why":
                                support_sentence = qa_md.getSupport(QID)[:600]
                                send_why2_quickreply(sender_id, "Here's an explanation: " + support_sentence)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_score(mysql, sender_id,QID,"why",0,time)

                            elif message_text == "Check Total Score":
                                print ("&"*50)
                                print (str(show_score(mysql, sender_id)))
                                send_gotit_quickreply(sender_id, "Your accumulated score is "+str(show_score(sender_id)))

                            elif message_text == "Report Bug":
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_score(sender_id,-1,message_text,-1,time)
                                send_interesting(sender_id, "Thanks for reporting! Would you want more questions to practice? :) ")

                            elif message_text == "Physics":
                                question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                                update_status(mysql, sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(mysql, sender_id,QID,message_text.lower(),time)
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            elif message_text == "Chemistry":
                                question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                                update_status(mysql, sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(mysql, sender_id,QID,message_text.lower(),time)
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            elif message_text == "Biology":
                                question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                                update_status(mysql, sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(mysql, sender_id,QID,message_text.lower(),time)
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            elif message_text == "Geology":
                                question, QID = qa_md.pickSubjectRandomQuestion(message_text)
                                update_status(mysql, sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(mysql, sender_id,QID,message_text.lower(),time)
                                send_message(sender_id, "Question."+str(QID)+": "+question)
                            
                            elif message_text == "Random":
                                question, QID = qa_md.pickRandomQuestion()
                                update_status(mysql, sender_id, 0)
                                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                insert_question(mysql, sender_id,QID,message_text.lower(),time)
                                send_message(sender_id, "Question."+str(QID)+": "+question)

                            elif message_text.lower() == 'switch subject':
                                send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

                            else: # user's respons in natural language    
                                if not show_status(sender_id):
                                    print("not first time"+"="*50)
                                    standard_answer = qa_md.getAnswer(QID)
                                    score = qa_model.compute_score(message_text, QID)
                                    send_message(sender_id, "Your score this round is "+str(score))
                                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    insert_score(mysql, sender_id,QID,message_text,score,time)
                                    send_why_quickreply(sender_id, QID, standard_answer)    
                                    update_status(mysql, sender_id, 1) 
                                else:
                                    update_status(mysql, sender_id, 1)
                                    send_interesting(sender_id, "That sounds interesting. Would you want more quiz questions to practice? I'm here to help :) ")
                                    
                                    #send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')
    return "ok", 200


    



############ SET UP ############
def setup_app(app):
    print("\nstart\n")
    greeting()
    print("\nafter greeting\n")
    persistent_menu()

setup_app(app)

if __name__ == '__main__':
    # model
    doc2vec = 'model_pre_trained/model_d2v_v1'
    pkl_file = 'model_pre_trained/glove/glove.6B.100d.pkl'
    # QA json data
    json_file = 'SciQdataset-23/200questions.json'
    
    qa_kb = QAKnowledgebase.ConstructQA(json_file)
    qa_md = QAModel.QAModel(qa_kb)
    qa_doc2vec = QAModel.Doc2VecModel(qa_kb, doc2vec)

    # select the right model to load based on environment variable "MODEL",
    # which is set in ./start_server.sh
    model = os.environ["MODEL"]
    if model == "TFIDF":
        qa_model = QAModel.TFIDFModel(qa_kb)
    elif model == "SIF":
        qa_model = QAModel.SIFModel(qa_kb)
    elif model == "SIF2":
        qa_model = QAModel.SIF2Model(qa_kb, pkl_file)

    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem', '/etc/letsencrypt/live/smartprimer.org/privkey.pem')

    app.run(host='0.0.0.0', threaded=True, debug=True, port=int(os.environ["PORT"]), ssl_context=context)
    
