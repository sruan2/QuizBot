# coding: utf8
import random
import time
from leaderboard.generate_leaderboard import *
from message import *
from database import *


def respond_to_payload(payload, sender_id, sender_firstname, qa_model, chatbot_text, template_conversation, mysql):
    '''
        This function responds to the QuizBot's payload states.

        Args:
            payload: chatbot's payload state
            sender_id: the sender's unique id assigned by Facebook Messenger
            sender_firstname: the sender's first name requested from the Facebook profile
            qa_model: the question answering model containing information about the question dataset
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates 
            mysql: database

        Returns:
    '''

    if payload == "GET_INTRO_1":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_say_hi(sender_id, template_conversation, sender_firstname)

    elif payload == "GET_INTRO_2":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "GET_INTRO_3":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "GET_INTRO_4":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_image(sender_id, payload, chatbot_text, "image_2")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "GET_INTRO_5":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "GET_READY":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "YUP_IM_READY":
        update_status(mysql, sender_id, 1)
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_1":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_2":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_image(sender_id, payload, chatbot_text, "image_2")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_3":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_4":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_image(sender_id, payload, chatbot_text, "image_2")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_5":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_6":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_7":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "ABOUT_QUIZBOT":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "CONTACT":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "REPORT_BUG":
        insert_score(mysql, sender_id, -1, payload, -1)
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "CONTINUE":
        update_status(mysql, sender_id, 1)
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "CHECK_TOTAL_SCORE":
        send_total_score(sender_id, template_conversation, str(show_score(mysql, sender_id)))

    elif payload == "I_DONT_KNOW":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "WHY":
        send_explanation(sender_id, template_conversation, mysql, explanation_sentence)

    elif payload == "SWITCH_SUBJECT":
        send_choose_subject(sender_id, template_conversation)

    elif payload == "SCIENCE":
        send_sentence(sender_id, payload, chatbot_text, template_conversation, "sentence_1")
        send_question(sender_id, template_conversation, payload, qa_model, mysql, "science")

    elif payload == "GRE":
        send_sentence(sender_id, payload, chatbot_text, template_conversation, "sentence_1")
        send_question(sender_id, template_conversation, payload, qa_model, mysql, "gre")

    elif payload == "SAFETY":
        send_sentence(sender_id, payload, chatbot_text, template_conversation, "sentence_1")
        send_question(sender_id, template_conversation, payload, qa_model, mysql, "safety")

    elif payload == "RANDOM":
        send_sentence(sender_id, payload, chatbot_text, template_conversation, "sentence_1")
        send_question(sender_id, template_conversation, payload, qa_model, mysql, "random")

    elif payload == "GIVEUP_YES":
        send_paragraph(sender_id, payload, chatbot_text, template_conversation, "paragraph_1")
        send_correct_answer(sender_id, payload, template_conversation, qa_model, 0, mysql)

    elif payload == "PRACTICE_MODE":
        send_choose_subject(sender_id, template_conversation)

    elif payload[:10] == "BUTTON_DKB":
        send_sentence(sender_id, payload[:10], chatbot_text, template_conversation, "sentence_1")
        send_correct_answer(sender_id, payload, template_conversation, qa_model, 0, mysql)

    elif payload[:10] == "BUTTON_AKB":
        send_sentence(sender_id, payload[:10], chatbot_text, template_conversation, "sentence_1")
        send_correct_answer(sender_id, payload, template_conversation, qa_model, 3, mysql)

    elif payload == "NEED_HINT":
        send_sentence(sender_id, payload[:10], chatbot_text, template_conversation, "sentence_1")
        send_hint(sender_id, qa_model, mysql)

    elif payload == "GIVEUP_NO":
        send_sentence(sender_id, payload[:10], chatbot_text, template_conversation, "sentence_1")
        send_hint(sender_id, qa_model, mysql)

    elif payload == "NEXT_QUESTION":
        if show_status(mysql, sender_id):
            subject = show_last_qid_subject(mysql, sender_id)[1] 
            subject = subject if subject in ["SCIENCE", "GRE", "SAFETY"] else "random"
            send_question(sender_id, template_conversation, payload = payload, qa_model = qa_model, mysql = mysql, subject = subject.lower())
        else:
            QID = show_last_qid_subject(mysql, sender_id)[0]
            send_question(sender_id, template_conversation, question = qa_model.pickLastQuestion(QID))


def respond_to_messagetext(message_text, sender_id, qa_model, chatbot_text, template_conversation, mysql):
    '''
        This function responds to the user's message texts.

        Args:
            message_text: the user's message text
            sender_id: the sender's unique id assigned by Facebook Messenger
            qa_model: the question answering model containing information about the question dataset
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates 
            mysql: database

        Returns:
    '''
    message_text = message_text.lower()
    QID, _ = show_last_qid_subject(mysql, sender_id)

    if message_text == "Practice Mode "+u'\u270F':
        send_choose_subject_quick_reply(sender_id, template_conversation)
        insert_question(mysql, sender_id,'-11','MENU_PRACTICE_MODE')

    elif message_text == "next question" or message_text == "got it, next!" or message_text[:4] == "sure":
        if show_status(mysql, sender_id):
            subject = show_last_qid_subject(mysql, sender_id)[1] 
            subject = subject if subject in ["SCIENCE", "GRE", "SAFETY"] else "random"
            send_question(sender_id, template_conversation, payload = payload, qa_model = qa_model, mysql = mysql, subject = subject.lower())
        else:
            score = qa_model.compute_score(message_text, QID)
            if score < 5:
                send_sentence(sender_id, payload[:10], chatbot_text, template_conversation, "sentence_1")
                send_correct_answer(recipient_id, payload, template_conversation, qa_model, 0, mysql)
            elif score < 10 and score >= 5:
                send_sentence(sender_id, payload[:10], chatbot_text, template_conversation, "sentence_2")
                send_correct_answer(recipient_id, payload, template_conversation, qa_model, 3, mysql)
            else:
                send_paragraph(sender_id, payload, chatbot_text, template_conversation, "paragraph_1")
                send_correct_answer(recipient_id, payload, template_conversation, qa_model, 10, mysql)
    else:
        if not show_status(mysql, sender_id):
            score = qa_model.compute_score(message_text, QID)
            if score < 5:
                send_sentence(sender_id, payload[:10], chatbot_text, template_conversation, "sentence_1")
                send_correct_answer(recipient_id, payload, template_conversation, qa_model, 0, mysql)
            elif score < 10:
                send_sentence(sender_id, payload[:10], chatbot_text, template_conversation, "sentence_2")
                send_correct_answer(recipient_id, payload, template_conversation, qa_model, 3, mysql)
            else:
                send_paragraph(sender_id, payload, chatbot_text, template_conversation, "paragraph_1")
                send_correct_answer(recipient_id, payload, template_conversation, qa_model, 10, mysql)
        else:
            update_status(mysql, sender_id, 1)
            response_message = ["That sounds interesting. Would you want more quiz questions to practice? I'm here to help 😄"]
            send_conversation(sender_id, DELAY_TIME, response_message, "SURE")

