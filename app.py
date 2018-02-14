import os
import json
import sys
#sys.path.append("/home/venv/quizbot/QuizBot/")
import QAKnowledgebase
import QAModel
from flask_mysqldb import MySQL
from random import randint
from similarity_model import tfidf
from flask import Flask, request, send_from_directory
import requests
import message
import database
import chatbot
import speech
import time
import reminder

# hide http print
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__, static_url_path='')

# ================== MySQL Setup ==================
mysql = MySQL()
app.config['MYSQL_HOST'] = os.environ["DB_HOST"]
app.config['MYSQL_USER'] = os.environ["DB_USER"]
app.config['MYSQL_PASSWORD'] = os.environ["DB_PASSWORD"]
app.config['MYSQL_DB'] = os.environ["DB"]
mysql.init_app(app)


@app.route('/pictures/<path:path>')
def send_pictures(path):
    return send_from_directory('pictures', path)


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
    #print("[QUIZBOT] PID " + str(os.getpid())+": Getting user profile from user_id: {recipient}".format(recipient=recipient_id))
    r = requests.get("https://graph.facebook.com/v2.6/{psid}?fields=first_name,last_name,gender&access_token={token}".format(psid=recipient_id,token=os.environ["PAGE_ACCESS_TOKEN"]))
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        return
    data = json.loads(r.text)
    return data


@app.route('/', methods=['POST'])
def webhook():

    reminder.RepeatedTimer(86400.0, message.send_reminder, database.show_inactive_user(mysql))
    #print("[QUIZBOT] PID " + str(os.getpid())+": Enter webhook") # endpoint for processing incoming messaging events
    data = request.get_json()
    
    if data["object"] == "page":
        for entry in data["entry"]:
            if entry.get("messaging"):
                for messaging_event in entry["messaging"]:

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    
                    if sender_id == os.environ["CHATBOT_ID"]: # return if this message is sent from the chatbot
                        return "Chatbot ID", 200

                    data = get_user_profile(sender_id)
                    sender_firstname = data['first_name']
                    sender_lastname = data['last_name']
                    if 'gender' in data:
                        sender_gender = data['gender']
                    else:
                        sender_gender = 'unknown'
                    #print("[QUIZBOT] PID " + str(os.getpid())+": Talking to " + sender_firstname)

                    # user clicked/tapped "postback" button in Persistent menu
                    if messaging_event.get("postback"):  
                        payload = messaging_event["postback"]["payload"] # the button's payload
                        message_text = messaging_event["postback"]["title"]  # the button's text
                        print("[QUIZBOT] PID " + str(os.getpid())+": Received a POSTBACK from Persistent Menu")
                        print("[QUIZBOT] PID " + str(os.getpid())+": Payload is \""+payload+"\"")
                        print("[QUIZBOT] PID " + str(os.getpid())+": Message Text is \""+message_text+"\"")
                        chatbot.respond_to_postback(payload, message_text, sender_id, qa_model, mysql)

                    
                    elif messaging_event.get("message"):  


                        # user clicked/tapped "postback" button in earlier message
                        if "quick_reply" in messaging_event.get("message"): 
                            payload = messaging_event["message"]["quick_reply"]["payload"] # the button's payload
                            message_text = messaging_event["message"]["text"]  # the button's text
                            print("[QUIZBOT] PID " + str(os.getpid())+": Received a POSTBACK from earlier message")
                            print("[QUIZBOT] PID " + str(os.getpid())+": Payload is \""+payload+"\"")
                            print("[QUIZBOT] PID " + str(os.getpid())+": Message Text is \""+message_text+"\"")
                            chatbot.respond_to_postback(payload, message_text, sender_id, qa_model, mysql)

                        # user sent an attachment: i.e., audio
                        elif "attachments" in messaging_event.get("message"): 
                            if messaging_event["message"]["attachments"][0]["type"] == "audio": # only getting the first attachment
                                print("[QUIZBOT] PID " + str(os.getpid())+": Received an AUDIO attachment")
                                receive_time = time.time()
                                #print("FB received audio: " + str(receive_time))
                                audio_url = messaging_event["message"]["attachments"][0]["payload"]["url"]
                                print("url is "+ audio_url)
                                final_result = speech.transcribe(audio_url)
                                #print("[QUIZBOT] PID " + str(os.getpid())+": Transcribed Text is \""+final_result+"\"")
                                finish_time = time.time()
                                #print("FB received transcription: " + str(finish_time))
                                print("Total time: " + str(finish_time-receive_time))
                                if final_result != "":
                                    message.send_message(sender_id, "You said: " + final_result)
                                    #print("FB print out transcription: " + str(time.time()))
                                else:
                                    message.send_message(sender_id, "Sorry, I could not recognize it :/")
                                chatbot.respond_to_messagetext(final_result, sender_id, qa_model, mysql)


                        # someone sent us a message
                        elif not "text" in messaging_event["message"]:
                            return "key error", 200
                        
                        else:                      
                            message_text = messaging_event["message"]["text"]  # the message's text
                            print("[QUIZBOT] PID " + str(os.getpid())+": Received a MESSAGE")
                            print("[QUIZBOT] PID " + str(os.getpid())+": Message Text is \""+message_text+"\"")
                            
                            # first-time user
                            if not int(sender_id) in database.show_user_id_list(mysql):
                                print("[QUIZBOT] PID " + str(os.getpid())+": This is a new user!")
                                database.insert_user(mysql, sender_id, sender_firstname, sender_lastname, sender_gender, 1)
                                database.insert_score(mysql, sender_id, -1, message_text, 0)
                                message.choose_mode_quick_reply(sender_id) 

                            else:
                                chatbot.respond_to_messagetext(message_text, sender_id, qa_model, mysql)
    return "ok", 200


# ================== SET UP ==================
def setup_app(app):
    print("[QUIZBOT] PID " + str(os.getpid())+": ============ Start the app ============")
    message.greeting()
    message.persistent_menu()

setup_app(app)

if __name__ == '__main__':
    # model
    doc2vec = 'model_pre_trained/model_d2v_v1'
    pkl_file = 'model_pre_trained/glove/glove.6B.100d.pkl'
    # QA json data
    json_file = 'SciQdataset-23/230questions.json'
    
    qa_kb = QAKnowledgebase.ConstructQA(json_file)

    # select the right model to load based on environment variable "MODEL", which is set in ./start_server.sh
    model = os.environ["MODEL"]
    if model == "TFIDF":
        qa_model = QAModel.TFIDFModel(qa_kb)
    elif model == "SIF":
        qa_model = QAModel.SIFModel(qa_kb)
    elif model == "SIF2":
        qa_model = QAModel.SIF2Model(qa_kb, pkl_file)
    elif model == "DOC2VEC":
        qa_model = QAModel.Doc2VecModel(qa_kb, doc2vec)

    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem', '/etc/letsencrypt/live/smartprimer.org/privkey.pem')

    app.run(host='0.0.0.0', threaded=True, debug=True, port=int(os.environ["PORT"]), ssl_context=context)
    
