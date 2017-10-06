import os
import sys
import json
import predict_reply
import visualize_sherry
from random import randint

import requests
from flask import Flask, request


tfidf = visualize_sherry.tfidfTransform()

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
            for messaging_event in entry["messaging"]:
                print("\n\messaging_event\n")

                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    print("sender ID is: "+sender_id)
                    print("recipient ID is: "+recipient_id)
                    print("\n-1- tfidf.QID is: "+str(tfidf.QID)+"\n")

                    if sender_id == "1497174250389598": #chatbot
                        return "irrelavant ID", 200
                    
                    #send_message(sender_id, "Your sender ID is: "+sender_id)
                    message_text = messaging_event["message"]["text"]  # the message's text

                    QID = tfidf.QID

                    print("===================== session length is:\n")
                    print len(app.session)

                    if not sender_id in app.session:
                        print("first time user"+"="*50)
                        question, QID = tfidf.pickRandomQuestion()
                        app.session[sender_id] = QID
                        print("===================== session length should be plus one:\n")
                        print len(app.session)
                        send_message(sender_id, "Question."+str(QID)+": "+question)

                    else:
                        # print("\n-2- QID is: "+str(tfidf.QID)+"\n")
                        if message_text == "Next Question" or message_text == "Got it, next!":
                            question, QID = tfidf.pickRandomQuestion()
                            app.session[sender_id] = QID
                            send_message(sender_id, "Question."+str(QID)+": "+question)
                            print("\n-3- QID is: "+str(QID)+"\n")

                        if message_text[:4] == "Why?":
                            send_gotit_quickreply(sender_id)

                        else: # user's respons in natural language    
                            print("not first time"+"="*50)
                            QID = app.session[sender_id]
                            standard_answer, score = tfidf.computeScore(message_text, QID)
                            send_message(sender_id, "Your score is: "+str(score))
                            
                            # Add a why button to show the supporting sentence
                            # you can use a dict instead of a Button class
                            #
                            send_why_quickreply(sender_id, QID, standard_answer)

                        

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

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
def send_why_quickreply(recipient_id, QID, standard_answer):

    # print("="*100)
    # print("sent a message!")

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
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_gitit_quickreply(recipient_id, QID):

    # print("="*100)
    # print("sent a message!")

    log("sending WHY button to {recipient}: {text}".format(recipient=recipient_id, text=str(QID)))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    support_sentence = tfidf.get_support(QID)
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

def setup_app(app):
    tfidf.appendQuestionKB('SciQdataset-23/question_file.txt')
    tfidf.appendSupportKB('SciQdataset-23/support_file.txt')
    tfidf.appendCorrectAnswerKB('SciQdataset-23/correct_answer_file.txt')
    app.session = {}

setup_app(app)


if __name__ == '__main__':
    app.run(debug=True)

    # send_message(sender_id, str("Received. I'm here!"))

    # print(predict(raw_input("Enter something")))
    



    
