import os
import json
import random
import time
import messaging_API
import database as db
import copy
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
            mysql: database
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            image_id: the name/id of the image being sent, specified in chatbot_text

        Returns:
            None
    '''
    image_data = chatbot_text[payload]["image"][image_id]
    random.shuffle(image_data["image_url"])
    image_data["image_url"][0] = image_data["image_url"][0].format(
        os.environ["PORT"])
    messaging_API.send_image(mysql, recipient_id, image_data)


def send_congratulation_image(mysql, recipient_id, template_conversation):
    '''
        This function sends a congratulation image to the specified recipient.

        Args:
            mysql: database
            recipient_id: the recipient's unique id assigned by Facebook Messengerng sent, specified in chatbot_text
            template_conversation: the json structure containing the conversation and state templates

        Returns:
            None
    '''
    if random.random() < 0.4:
        image_data = template_conversation["STATE"]["CONGRATULATION"]["image"]
        random.shuffle(image_data["image_url"])
        image_data["image_url"][0] = image_data["image_url"][0].format(
            os.environ["PORT"])
        messaging_API.send_image(mysql, recipient_id, image_data)


def send_paragraph(mysql, recipient_id, payload, chatbot_text, template_conversation, paragraph_id):
    '''
        This function sends a set of sentences to the specified recipient.

        Args:
            mysql: database
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
            mysql: database
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates
            conversation_id: the name/id of the conversation being sent, specified in chatbot_text

        Returns:
            None
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
            mysql: database
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates
            state: the state's name, specified in template_conversation
            format_fill_text: the text to be filled into the placeholder of the message text

        Returns:
            None
    '''
    quick_reply_data = copy.deepcopy(template_conversation["STATE"][state]["quick_reply"])
    quick_reply_data["message"]["text"] = quick_reply_data["message"]["text"].format(format_fill_text)
    uid = messaging_API.send_quick_reply(mysql, recipient_id, template_conversation, quick_reply_data)

    # return uid so that we can log the information in the [user_history] dataset when the bot sends a question
    return uid


def send_choose_subject(mysql, recipient_id, template_conversation):
    '''
        This function asks the specified recipient to choose a subject.
        Args:
            mysql: database
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
            recipient_id (str): the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates
            qa_model: the question answering model containing information about the question dataset
            cache: a dictionary storing useful information in memory for each user
        Return:
            None
    '''
    subject = cache[recipient_id]['current_subject'] if cache[recipient_id]['current_subject'] != None else 'random'
    question, qid = qa_model.pickQuestion(recipient_id, subject)

    message_data_1 = template_conversation["STATE"]["QUESTION"]["message_1"]
    message_data_2 = template_conversation["STATE"]["QUESTION"]["message_2"]
    messaging_API.send_message(
        mysql, recipient_id, template_conversation, message_data_1)
    
    # and cache[recipient_id]['current_qid'] < 150 and cache[recipient_id]['current_qid'] >= 100

    if random.random() < 0.5:
        messaging_API.send_message(mysql, recipient_id, template_conversation, message_data_2)

    uid = send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "QUESTION", question)

    # insert the question to the [user_history] table
    db.insert_user_history(mysql, recipient_id, qid, "random", begin_uid=uid)
    update_cache(cache, recipient_id, current_qid=qid, begin_uid=uid)


def send_say_hi(mysql, recipient_id, template_conversation, recipient_firstname):
    '''
        This function sends a hi message to the specified recipient.

        Args:
            mysql: database
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            template_conversation: the json structure containing the conversation and state templates
            recipient_firstname: the recipient's first name

        Returns:
            None
    '''
    send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "SAY_HI", recipient_firstname)


def send_correct_answer(mysql, recipient_id, payload, template_conversation, qa_model, cache):
    '''
        This function sends the correct answer of a question to the specified recipient.

        Args:
            mysql: database
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            payload: chatbot's payload state
            template_conversation: the json structure containing the conversation and state templates
            qa_model: the question answering model containing information about the question dataset
            cache: a dictionary containing the information in memory such as current_qid and current_subject needed for the quizbot

        Returns:
            None
    '''
    qid = cache[recipient_id]['current_qid']
    correct_answer = qa_model.getAnswer(qid)
    send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "CORRECT_ANSWER", correct_answer)


def send_explanation(mysql, recipient_id, template_conversation, qa_model, cache):
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
    qid = cache[recipient_id]['current_qid']
    explanation_sentence = qa_model.getSupport(qid)

    message_data = template_conversation["STATE"]["EXPLANATION"]["message"]
    messaging_API.send_message(
        mysql, recipient_id, template_conversation, message_data)

    if cache[recipient_id]['if_explanation_text'] and cache[recipient_id]['current_qid'] >= 100 and cache[recipient_id]['current_qid'] < 150:
        explanation_sentence = explanation_sentence.split("\n")
        explanation_sentence = explanation_sentence[0]

    send_format_quick_reply_text(
        mysql, recipient_id, template_conversation, "EXPLANATION", explanation_sentence)



def send_hint(mysql, recipient_id, chatbot_text, template_conversation, qa_model, cache):
    '''
        This function sends a list of hints(distractors) to the specified recipient.

        Args:
            mysql: database
            recipient_id: the recipient's unique id assigned by Facebook Messenger
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates
            qa_model: the question answering model containing information about the question dataset
            cache: a dictionary containing the information in memory such as current_qid and current_subject needed for the quizbot

        Returns:
            None
    '''
    qid = cache[recipient_id]['current_qid']
    message_text = ""
    options = []
    index = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
             "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    chatbot_text_local = copy.deepcopy(chatbot_text)

    for x in qa_model.DKB[qid]:
        options.append({
            "content_type": "text",
            "title": str(x),
            "payload": "BUTTON_DKB_" + str(x)
        })
    for x in qa_model.AKB[qid]:
        options.append({
            "content_type": "text",
            "title": str(x),
            "payload": "BUTTON_AKB_" + str(x)
        })
    random.shuffle(options)

    for i in range(len(options)):
        j = len(options) - i - 1
        message_text += index[i % 10]
        message_text += " "
        message_text += str(options[i]["title"])
        message_text += "\n"
        chatbot_text_local["NEED_HINT"]["conversation"]["conversation_1"]["quick_reply"]["source"].insert(
            0, "LOCAL")
        chatbot_text_local["NEED_HINT"]["conversation"]["conversation_1"]["quick_reply"]["title"].insert(
            0, index[j % 10])
        chatbot_text_local["NEED_HINT"]["conversation"]["conversation_1"]["quick_reply"]["payload"].insert(
            0, options[j]["payload"])

    chatbot_text_local["NEED_HINT"]["conversation"]["conversation_1"]["message"][1]["text"] = message_text
    send_conversation(mysql, recipient_id, "NEED_HINT",
                      chatbot_text_local, template_conversation, "conversation_1")

