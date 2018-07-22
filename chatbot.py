# coding: utf8
import time
#from leaderboard.generate_leaderboard import *
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
            None
    '''

    if payload == "GET_INTRO_1":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_say_hi(mysql, sender_id, template_conversation, sender_firstname)

    elif payload == "GET_INTRO_2":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "GET_INTRO_3":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "GET_INTRO_4":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_image(mysql, sender_id, payload, chatbot_text, "image_2")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "GET_INTRO_5":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "GET_READY":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "YUP_IM_READY":
        update_status(mysql, sender_id, 1)
        insert_question(mysql, sender_id, -1, payload)
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_1":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_2":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_image(mysql, sender_id, payload, chatbot_text, "image_2")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_3":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_4":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_image(mysql, sender_id, payload, chatbot_text, "image_2")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    # elif payload == "USER_MANUAL_5":
    #     send_image(mysql, sender_id, payload, chatbot_text, "image_1")
    #     send_conversation(mysql, sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_6":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_7":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "ABOUT_QUIZBOT":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "CONTACT":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "REPORT_BUG":
        # insert_score(mysql, sender_id, -1, payload, -1)
        database.insert_conversation(
            mysql, sender_id, -1, "report_bug", "report_bug", payload, 0)

        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "CONTINUE":
        update_status(mysql, sender_id, 1)
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "I_DONT_KNOW":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "WHY":
        send_explanation(mysql, sender_id, template_conversation, qa_model)

    elif payload == "SWITCH_SUBJECT":
        send_choose_subject(mysql, sender_id, template_conversation)

    elif payload == "SCIENCE":
        QID = show_last_qid_subject(mysql, sender_id)[0]
        if QID >= 50 and QID < 100:
            send_image(mysql, sender_id, payload, chatbot_text, "SAFETY")
        elif QID >= 100 and QID < 150:
            send_image(mysql, sender_id, payload, chatbot_text, "GRE")
        else:
            send_image(mysql, sender_id, payload, chatbot_text, "NORMAL")

        send_paragraph(mysql, sender_id, payload, chatbot_text, template_conversation, "paragraph_1")
        send_question(mysql, sender_id, template_conversation,
                      payload, qa_model, "science")

    elif payload == "GRE":
        QID = show_last_qid_subject(mysql, sender_id)[0]
        if QID >= 0 and QID < 50:
            send_image(mysql, sender_id, payload, chatbot_text, "SCIENCE")
        elif QID >= 50 and QID < 100:
            send_image(mysql, sender_id, payload, chatbot_text, "SAFETY")
        else:
            send_image(mysql, sender_id, payload, chatbot_text, "NORMAL")

        send_paragraph(mysql, sender_id, payload, chatbot_text, template_conversation, "paragraph_1")
        send_question(mysql, sender_id, template_conversation,
                      payload, qa_model, "gre")

    elif payload == "SAFETY":
        QID = show_last_qid_subject(mysql, sender_id)[0]
        if QID >= 0 and QID < 50:
            send_image(mysql, sender_id, payload, chatbot_text, "SCIENCE")
        elif QID >= 100 and QID < 150:
            send_image(mysql, sender_id, payload, chatbot_text, "GRE")
        else:
            send_image(mysql, sender_id, payload, chatbot_text, "NORMAL")

        send_paragraph(mysql, sender_id, payload, chatbot_text, template_conversation, "paragraph_1")
        send_question(mysql, sender_id, template_conversation,
                      payload, qa_model, "safety")

    elif payload == "RANDOM":
        QID = show_last_qid_subject(mysql, sender_id)[0]
        if QID >= 0 and QID < 50:
            send_image(mysql, sender_id, payload, chatbot_text, "SCIENCE")
        elif QID >= 50 and QID < 100:
            send_image(mysql, sender_id, payload, chatbot_text, "SAFETY")
        elif QID >= 100 and QID < 150:
            send_image(mysql, sender_id, payload, chatbot_text, "GRE")
        else:
            send_image(mysql, sender_id, payload, chatbot_text, "NORMAL")

        send_paragraph(mysql, sender_id, payload, chatbot_text, template_conversation, "paragraph_1")
        send_question(mysql, sender_id, template_conversation,
                      payload, qa_model, "random")

    elif payload == "GIVEUP_YES":
        send_paragraph(mysql, sender_id, payload, chatbot_text,
                       template_conversation, "paragraph_1")
        send_correct_answer(mysql, sender_id, payload,
                            template_conversation, qa_model, 0)

    elif payload == "PRACTICE_MODE":
        send_choose_subject(mysql, sender_id, template_conversation)

    elif payload[:10] == "BUTTON_DKB":
        send_paragraph(mysql, sender_id, payload[:10], chatbot_text, template_conversation, "paragraph_1")
        send_correct_answer(mysql, sender_id, payload,
                            template_conversation, qa_model, 0)

    elif payload[:10] == "BUTTON_AKB":
        send_paragraph(mysql, sender_id, payload[:10], chatbot_text, template_conversation, "paragraph_1")
        send_correct_answer(mysql, sender_id, payload,
                            template_conversation, qa_model, 3)

    elif payload == "NEED_HINT":
        send_paragraph(mysql, sender_id, payload, chatbot_text, template_conversation, "paragraph_1")
        send_hint(mysql, sender_id, qa_model)

    elif payload == "GIVEUP_NO":
        send_paragraph(mysql, sender_id, payload, chatbot_text,
                       template_conversation, "paragraph_1")
        send_hint(mysql, sender_id, qa_model)

    elif payload == "CHAT_WITH_ME":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "JOKE":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")



    # elif payload == "INTERACT":
    #     science, safety, gre = show_all_qid(mysql, sender_id)
    #     num_science = len(science)
    #     num_safety = len(science)
    #     num_gre = len(science)

    #     if num_science >= num_safety and num_science >= num_gre:
    #         send_image(sender_id, payload, chatbot_text, "SCIENCE")
    #         send_conversation(sender_id, payload, chatbot_text, template_conversation, "SCIENCE")

    #     elif num_safety >= num_science and num_safety >= num_gre:
    #         send_image(sender_id, payload, chatbot_text, "SAFETY")
    #         send_conversation(sender_id, payload, chatbot_text, template_conversation, "SAFETY")

    #     elif num_gre >= num_science and num_gre >= num_safety:
    #         send_image(sender_id, payload, chatbot_text, "GRE")
    #         send_conversation(sender_id, payload, chatbot_text, template_conversation, "GRE")

    elif payload == "NEXT_QUESTION":
        send_question(mysql, sender_id, template_conversation, qa_model)

        # if show_status(mysql, sender_id):
        #     subject = show_last_qid_subject(mysql, sender_id)[1]
        #     subject = subject if subject in [
        #         "SCIENCE", "GRE", "SAFETY"] else "random"
        #     send_question(mysql, sender_id, template_conversation,
        #                   payload=payload, qa_model=qa_model, subject=subject.lower())
        # else:
        #     QID = show_last_qid_subject(mysql, sender_id)[0]
        #     send_question(mysql, sender_id, template_conversation,
        #                   question=qa_model.pickQuestion(subject='random'))

# TODO: Remove redundant code
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
            None
    '''
    message_text = message_text.lower()
    QID, _ = show_last_qid_subject(mysql, sender_id)

    if message_text == "Practice Mode "+u'\u270F':
        send_choose_subject_quick_reply(
            mysql, sender_id, template_conversation)
        insert_question(mysql, sender_id, '-11', 'MENU_PRACTICE_MODE')

    elif message_text == "next question" or message_text == "got it, next!" or message_text[:4] == "sure":
        if show_status(mysql, sender_id):
            subject = show_last_qid_subject(mysql, sender_id)[1]
            subject = subject if subject in [
                "SCIENCE", "GRE", "SAFETY"] else "random"
            send_question(mysql, sender_id, template_conversation,
                          payload=payload, qa_model=qa_model, subject=subject.lower())
        else:
            score = qa_model.compute_score(message_text, QID)
            if score < 5:
                send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                              chatbot_text, template_conversation, "paragraph_1")
                send_correct_answer(
                    mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, 0)
            elif score < 10 and score >= 5:
                send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                              chatbot_text, template_conversation, "paragraph_2")
                send_correct_answer(
                    mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, 3)
            else:
                send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                               chatbot_text, template_conversation, "paragraph_3")
                send_correct_answer(
                    mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, 10)
    else:
        if not show_status(mysql, sender_id):
            score = qa_model.compute_score(message_text, QID)
            if score < 5:
                send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                              chatbot_text, template_conversation, "paragraph_1")
                send_correct_answer(
                    mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, 0)
            elif score < 10:
                send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                              chatbot_text, template_conversation, "paragraph_2")
                send_correct_answer(
                    mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, 3)
            else:
                send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                               chatbot_text, template_conversation, "paragraph_3")
                send_correct_answer(
                    mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, 10)
        else:
            update_status(mysql, sender_id, 1)
            send_conversation(mysql, sender_id, "MESSAGE_TEXT",
                              chatbot_text, template_conversation, "conversation_1")
