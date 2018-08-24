'''
    chatbot.py
    Author: Liwei Jiang, Sherry Ruan, Zhengneng Qiu
    Last Modified Date: 09/08/2018
    Usage: Receiving and sending messages between the users and the chatbot.
'''

# coding: utf8
from time import strftime, localtime
import database as db
from message import *
import utils


def respond_to_payload(payload, sender_id, qa_model, chatbot_text, template_conversation, mysql, cache, uid):
    '''
        This function responds to the QuizBot's payload states.

        Args:
            payload: chatbot's payload state
            sender_id: the sender's unique id assigned by Facebook Messenger
            qa_model: the question answering model containing information about the question dataset
            chatbot_text: the json structure containing the chatbot's text/conversation source
            template_conversation: the json structure containing the conversation and state templates
            mysql: database
            cache: a dictionary containing the information in memory such as current_qid and current_subject needed for the quizbot
            uid: unique id in [conversation] table of the [QUIZBOT_DEV] database for this conversation

        Returns:
            None
    '''
    utils.update_cache(cache, sender_id, last_payload=payload)

    if payload not in ["NEXT_QUESTION", "NEED_HINT"]:
        utils.update_cache(cache, sender_id, waiting_for_answer=0)

    # ---------------------------- INTRO ----------------------------
    if payload == "GET_INTRO_1":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        sender_firstname = cache[sender_id]['firstname']
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
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "GET_INTRO_5":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "GET_INTRO_6":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "GET_READY":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "YUP_IM_READY":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    # ------------------------- USER_MANUAL -------------------------
    elif payload == "USER_MANUAL_1":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_2":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_3":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_4":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_5":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_image(mysql, sender_id, payload, chatbot_text, "image_2")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_6":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_7":
        send_image(mysql, sender_id, payload, chatbot_text, "image_1")
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "USER_MANUAL_8":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    # --------------------- REQUEST A QUESTION ----------------------
    elif payload == "SCIENCE":
        if cache[sender_id]["current_subject"] == "safety":
            send_image(mysql, sender_id, payload, chatbot_text, "SAFETY")
        elif cache[sender_id]["current_subject"] == "gre":
            send_image(mysql, sender_id, payload, chatbot_text, "GRE")
        elif cache[sender_id]["current_subject"] == "random":
            send_image(mysql, sender_id, payload, chatbot_text, "NORMAL")

        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

        db.update_user_current_subject(mysql, sender_id, "science")
        utils.update_cache(
            cache, sender_id, current_subject="science", if_explanation_text=False)

    elif payload == "GRE":
        if cache[sender_id]["current_subject"] == "science":
            send_image(mysql, sender_id, payload, chatbot_text, "SCIENCE")
        elif cache[sender_id]["current_subject"] == "safety":
            send_image(mysql, sender_id, payload, chatbot_text, "SAFETY")
        elif cache[sender_id]["current_subject"] == "random":
            send_image(mysql, sender_id, payload, chatbot_text, "NORMAL")

        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

        db.update_user_current_subject(mysql, sender_id, "gre")
        utils.update_cache(
            cache, sender_id, current_subject="gre", if_explanation_text=False)

    elif payload == "SAFETY":
        if cache[sender_id]["current_subject"] == "science":
            send_image(mysql, sender_id, payload, chatbot_text, "SCIENCE")
        elif cache[sender_id]["current_subject"] == "gre":
            send_image(mysql, sender_id, payload, chatbot_text, "GRE")
        elif cache[sender_id]["current_subject"] == "random":
            send_image(mysql, sender_id, payload, chatbot_text, "NORMAL")

        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

        db.update_user_current_subject(mysql, sender_id, "safety")
        utils.update_cache(
            cache, sender_id, current_subject="safety", if_explanation_text=False)

    elif payload == "RANDOM":
        if cache[sender_id]["current_subject"] == "science":
            send_image(mysql, sender_id, payload, chatbot_text, "SCIENCE")
        elif cache[sender_id]["current_subject"] == "safety":
            send_image(mysql, sender_id, payload, chatbot_text, "SAFETY")
        elif cache[sender_id]["current_subject"] == "gre":
            send_image(mysql, sender_id, payload, chatbot_text, "GRE")

        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

        db.update_user_current_subject(mysql, sender_id, "random")
        utils.update_cache(
            cache, sender_id, current_subject="random", if_explanation_text=False)

    elif payload == "NEXT_QUESTION":
        utils.update_cache(
            cache, sender_id, waiting_for_answer=1, if_explanation_text=False)
        send_question(mysql, sender_id, template_conversation, qa_model, cache)

    # ---------------------- ANSWER A QUESTION ----------------------
    elif payload == "NEED_HINT":
        send_hint(mysql, sender_id, chatbot_text,
                  template_conversation, qa_model, cache)
        utils.update_cache(cache, sender_id, waiting_for_answer=1)

    elif payload == "I_DONT_KNOW":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    # ---------------------- EVALUATE AN ANSWER ---------------------
    elif payload[:10] == "BUTTON_DKB":  # user selects the wrong choice from the hint
        db.update_user_history(
            mysql, sender_id, 0, "multiple-choice", cache[sender_id]['begin_uid'], uid)
        qa_model.updateHistory(
            sender_id, (cache[sender_id]['current_qid'][0], 0, db.show_timestamp(mysql, uid)))
        send_paragraph(
            mysql, sender_id, payload[:10], chatbot_text, template_conversation, "paragraph_1")
        send_correct_answer(mysql, sender_id, payload[:10],
                            template_conversation, qa_model, cache)

    elif payload[:10] == "BUTTON_AKB":  # user selects the correct choice from the hint
        db.update_user_history(
            mysql, sender_id, 10, "multiple-choice", cache[sender_id]['begin_uid'], uid)
        qa_model.updateHistory(
            sender_id, (cache[sender_id]['current_qid'][0], 10, db.show_timestamp(mysql, uid)))
        send_congratulation_image(mysql, sender_id, template_conversation)
        send_paragraph(
            mysql, sender_id, payload[:10], chatbot_text, template_conversation, "paragraph_1")
        send_correct_answer(mysql, sender_id, payload[:10],
                            template_conversation, qa_model, cache)

    # --------------------------- GIVE UP ---------------------------
    elif payload == "GIVEUP_YES":
        send_paragraph(mysql, sender_id, payload, chatbot_text,
                       template_conversation, "paragraph_1")
        send_correct_answer(mysql, sender_id, payload,
                            template_conversation, qa_model, cache)

    elif payload == "GIVEUP_NO":
        send_paragraph(mysql, sender_id, payload, chatbot_text,
                       template_conversation, "paragraph_1")
        send_hint(mysql, sender_id, chatbot_text,
                  template_conversation, qa_model, cache)

    # ----------------------- AFTER AN ANSWER -----------------------
    elif payload == "WHY":
        send_explanation(mysql, sender_id,
                         template_conversation, qa_model, cache)

    elif payload == "SWITCH_SUBJECT":
        send_choose_subject(mysql, sender_id, template_conversation)

    # --------------------------- CONTINUE --------------------------
    elif payload == "CONTINUE":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    # ------------------------- CHAT WITH ME ------------------------
    elif payload == "CHAT_WITH_ME":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "JOKE":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "FUN_FACT_SCIENCE":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    # ----------------------------- MORE ----------------------------
    elif payload == "ABOUT_QUIZBOT_1":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "ABOUT_QUIZBOT_2":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "ABOUT_QUIZBOT_3":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "CONTACT":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")

    elif payload == "REPORT_BUG":
        send_conversation(mysql, sender_id, payload, chatbot_text,
                          template_conversation, "conversation_1")


def respond_to_messagetext(message_text, sender_id, qa_model, chatbot_text, template_conversation, mysql, cache, uid):
    '''
        This function responds to the user's message texts.

        Args:
            message_text: the user's message text
            sender_id: the sender's unique id assigned by Facebook Messenger
            qa_model: the question answering model containing information
                about the question dataset
            chatbot_text: the json structure containing the chatbot's
                text/conversation source
            template_conversation: the json structure containing the
                conversation and state templates
            mysql: database
            cache: a dictionary containing the information in memory such as
                current_qid and current_subject needed for the quizbot
            uid: unique id in [conversation] table of the [QUIZBOT_DEV] database for this conversation

        Returns:
            None
    '''
    message_text = message_text.lower()

    # allow user to type in the bug report
    if cache[sender_id]["last_payload"] == "REPORT_BUG":
        send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                           chatbot_text, template_conversation, "paragraph_4")
        return

    qid = cache[sender_id]["current_qid"]
    if cache[sender_id]["waiting_for_answer"]:
        score = qa_model.computeScore(message_text, qid[0])
        db.update_user_history(
            mysql, sender_id, score, "fill_in_the_blank", cache[sender_id]['begin_uid'], uid)
        qa_model.updateHistory(
            sender_id, (qid[0], score, db.show_timestamp(mysql, uid)))
        if score < 9:
            send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                           chatbot_text, template_conversation, "paragraph_1")
            send_correct_answer(
                mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, cache)
        elif score < 10:
            send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                           chatbot_text, template_conversation, "paragraph_2")
            send_correct_answer(
                mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, cache)
        else:
            send_congratulation_image(mysql, sender_id, template_conversation)
            send_paragraph(mysql, sender_id, "MESSAGE_TEXT",
                           chatbot_text, template_conversation, "paragraph_3")
            send_correct_answer(
                mysql, sender_id, "MESSAGE_TEXT", template_conversation, qa_model, cache)
        utils.update_cache(
            cache, sender_id, waiting_for_answer=0, if_explanation_text=True)
    else:  # That sounds interesting. Would you want more quiz questions?
        send_conversation(mysql, sender_id, "MESSAGE_TEXT",
                          chatbot_text, template_conversation, "conversation_1")
