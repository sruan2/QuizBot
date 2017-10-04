import os
import sys
import json
import predict_reply
import visualize_sherry
from random import randint

import requests
from flask import Flask, request


tfidf = visualize_sherry.tfidfTransform()
question_id = {}
QID = -1


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

    print("\n\nwebhook\n\n")

    global question_id
    global QID

    # endpoint for processing incoming messaging events

    data = request.get_json()
    #log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            print("\n\entry\n\n")
            for messaging_event in entry["messaging"]:
                print("\n\messaging_event\n\n")

                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    print("sender ID is: "+sender_id)
                    print("recipient ID is: "+recipient_id)
                    print("\n-1- QID is: "+str(QID)+"\n")

                    if sender_id == "1497174250389598": #chatbot
                        return "irrelavant ID", 200
                    
                    send_message(sender_id, "Your sender ID is: "+sender_id)
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if QID == -1:
                        print("first time user"+"="*50)
                        question, QID = tfidf.pickRandomQuestion()
                        send_message(sender_id, "Question."+str(QID)+": "+question)
                    else:
                        print("\n-2- QID is: "+str(QID)+"\n")
                        print("true"+"="*50)
                        standard_answer, score = tfidf.computeScore(message_text, QID)
                        send_message(sender_id, "Answer." +str(QID) + ": "+standard_answer)
                        send_message(sender_id, "Your score is: "+str(score))

                        question, QID = tfidf.pickRandomQuestion()
                        send_message(sender_id, "Question."+str(QID)+": "+question)
                        print("\n-3- QID is: "+str(QID)+"\n")

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


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

def predict(incoming_msg):
    return predict_reply.classify(incoming_msg);

def setup_app(app):
    tfidf.appendQuestionKB('SciQdataset-23/question_file.txt')
    tfidf.appendSupportKB('SciQdataset-23/support_file.txt')
    tfidf.appendCorrectAnswerKB('SciQdataset-23/correct_answer_file.txt')
setup_app(app)

if __name__ == '__main__':
    app.run(debug=True)

    # send_message(sender_id, str("Received. I'm here!"))

    # print(predict(raw_input("Enter something")))
    



    
