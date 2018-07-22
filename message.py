import os
import json
import requests
import random
import time
import messaging_API
import database as db
from utils import *


def persistent_menu(template_conversation):
    '''
        This function sets up the persistence menu.

        Args:
            template_conversation: the json structure containing the conversation and state templates

        Returns:
            None
    '''
    messaging_API.send_persistent_menu(json.dumps(
        template_conversation["STATE"]["PERSISTENT_MENU"]))


def init_payload(template_conversation):
    '''
        This function initializes the payloads.

        Args:
            template_conversation: the json structure containing the conversation and state templates

        Returns:
            None
    '''
    messaging_API.send_get_started(json.dumps(
        template_conversation["STATE"]["GET_STARTED"]))


def send_image(mysql, recipient_id, payload, chatbot_text, image_id):
    '''
        This function sends an image to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            image_id: the name/id of the image being sent, specified in chatbot_text

        Returns:
    '''
    image_data = chatbot_text[payload]["image"][image_id]
    image_data["image_url"] = image_data["image_url"].format(
        os.environ["PORT"])
    messaging_API.send_image(mysql, recipient_id, image_data)


def send_paragraph(mysql, recipient_id, payload, chatbot_text, template_conversation, paragraph_id):
    '''
        This function sends a set of sentences to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates
            paragraph_id: the name/id of the paragraph being sent, specified in chatbot_text

        Returns:
            None
    '''
    paragraph_data = chatbot_text[payload]["paragraph"][paragraph_id]
    num_sentence = len(paragraph_data)

    for i in range(num_sentence):
        message_data = paragraph_data[i]
        messaging_API.send_message(
            mysql, recipient_id, template_conversation, message_data)


def send_conversation(mysql, recipient_id, payload, chatbot_text, template_conversation, conversation_id):
    '''
        This function sends a list of texts, with a short delay and typing action in between scentences,
        along with a set of quick reply button to continue the conversation, to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates
            conversation_id: the name/id of the conversation being sent, specified in chatbot_text

        Returns:
    '''
    conversation_data = chatbot_text[payload]["conversation"][conversation_id]

    message_data = conversation_data["message"]
    for msg in message_data[:-1]:
        messaging_API.send_message(
            mysql, recipient_id, template_conversation, msg)

    quick_reply_data = conversation_data["quick_reply"]
    messaging_API.send_quick_reply(
        mysql, recipient_id, template_conversation, quick_reply_data, message_data[-1])


def send_format_quick_reply_text(mysql, recipient_id, template_conversation, state, format_fill_text):
    '''
        This function sends a quick reply with formatted text message.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates
            state: the state's name, specified in template_conversation
            format_fill_text: the text to be filled into the placeholder of the message text

        Returns:
            None
    '''
    quick_reply_data = template_conversation["STATE"][state]["quick_reply"]
    text_format = quick_reply_data["message"]["text"]
    quick_reply_data["message"]["text"] = quick_reply_data["message"]["text"].format(format_fill_text)
    timestamp, uid = messaging_API.send_quick_reply(
        mysql, recipient_id, template_conversation, quick_reply_data)
    quick_reply_data["message"]["text"] = text_format
    # return timestamp and uid so that we can log the information in the [user_history] dataset when the bot sends a question
    return timestamp, uid


def send_choose_subject(mysql, recipient_id, template_conversation):
    '''
        This function asks the specified recipient to choose a subject.
        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates

        Returns:
    '''
    quick_reply_data = template_conversation["STATE"]["CHOOSE_SUBJECT"]["quick_reply"]
    messaging_API.send_quick_reply(
        mysql, recipient_id, template_conversation, quick_reply_data)


def send_question(mysql, recipient_id, template_conversation, qa_model, cache):
    '''
        This function sends a question to the specified recipient.

        Args:
            mysql: database
            recipient_id (str): the recipient's unique id assigned by Facebook
                Messenger
            template_conversation: the json structure containing the
                conversation and state templates
            qa_model: the question answering model containing information
                about the question dataset
            cache: a dictionary storing useful information in memory for each
                user
    '''
    # TODO: sherry: let the subject be random for now. QA Model should memorize the subject for each user.
    subject = cache[recipient_id]['current_subject'] \
        if cache[recipient_id]['current_subject'] else 'random'
    question, QID = qa_model.pickQuestion(subject)

    message_data = template_conversation["STATE"]["QUESTION"]["message"]
    messaging_API.send_message(mysql, recipient_id, template_conversation,
                               message_data)

    timestamp, uid = send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "QUESTION", question)

    # insert the question to the [user_history] table
    db.insert_user_history(mysql, recipient_id, QID, "random", timestamp, begin_uid=uid)

    # store the QID into cache for this user (for continuity of the conversation)
    cache[recipient_id]['current_qid'] = QID


def send_say_hi(mysql, recipient_id, template_conversation, recipient_firstname):
    '''
        This function sends a hi message to the specified recipient.
    '''
    send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "SAY_HI", recipient_firstname)


def send_correct_answer(mysql, recipient_id, payload, template_conversation, qa_model, score):
    '''
        This function sends the correct answer of a question to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            template_conversation: the json structure containing the conversation and state templates
            qa_model: the question answering model containing information about the question dataset
            score: the score to be logged into the database
            mysql: database

        Returns:
            None
    '''
    QID, _ = db.show_last_qid_subject(mysql, recipient_id)
    standard_answer = qa_model.getAnswer(QID)
    # insert_score(mysql, recipient_id, QID, payload, score)
    # insert_conversation(mysql, recipient_id, QID, "user_typing", "subject", payload, score)
    send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "CORRECT_ANSWER", standard_answer)
    db.update_status(mysql, recipient_id, 1)

# insert_conversation(mysql, sender_id, receiver_id, dialog, type, timestamp, qid, score)


def send_explanation(mysql, recipient_id, template_conversation, qa_model):
    '''
        This function sends the explanation of a question to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates
            mysql: database
            explanation: the explanation of a question to be sent to the recipient

        Returns:
            None
    '''
    QID, _ = db.show_last_qid_subject(mysql, recipient_id)
    explanation_sentence = qa_model.getSupport(QID)

    message_data = template_conversation["STATE"]["EXPLANATION"]["message"]
    messaging_API.send_message(
        mysql, recipient_id, template_conversation, message_data)

    send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "EXPLANATION", explanation_sentence)


def send_total_score(recipient_id, template_conversation, total_score):
    '''
        This function sends the total score of the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates
            total score: the total score of the recipient, extracted from the database

        Returns:
            None
    '''
    send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "TOTAL_SCORE", total_score)


def send_hint(mysql, recipient_id, qa_model):
    '''
        This function sends a list of hints(distractors) to the specified recipient.

        Args:
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            qa_model: the question answering model containing information about the question dataset
            mysql: database

        Returns:
            None
    '''
    QID, _ = db.show_last_qid_subject(mysql, recipient_id)

    message_text = ""
    options = []
    index = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
             "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for x in qa_model.DKB[QID]:
        options.append({
            "content_type": "text",
            "title": str(x),
            "payload": "BUTTON_DKB_"+str(x)
        })
    for x in qa_model.AKB[QID]:
        options.append({
            "content_type": "text",
            "title": str(x),
            "payload": "BUTTON_AKB_"+str(x)
        })
    random.shuffle(options)

    for i in range(len(options)):
        message_text += index[i % 10]
        message_text += " "
        message_text += str(options[i]["title"])
        message_text += "\n"
        options[i]["title"] = index[i % 10]

    options.append({
        "content_type": "text",
        "title": "I don’t know 😓",
        "payload": "I_DONT_KNOW"
    })

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
            "quick_replies": options
        }
    })
    messaging_API.send_data(data)
