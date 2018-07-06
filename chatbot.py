# coding: utf8
from message import *
from database import *
import random
import time
from leaderboard.generate_leaderboard import *
# import text.chatbot_text as txt


# ================= Chatbot's reply to a postback =================
def respond_to_payload(payload, message_text, sender_id, sender_firstname, qa_model, chatbot_text, template_conversation, mysql):
    message_text = message_text.lower()

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

    elif payload == "BUTTON_YUP_IM_READY":
        update_status(mysql, sender_id, 1)
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")





    elif payload == "MENU_SCORE":
        score = show_score(mysql, sender_id)
        send_gotit_quickreply(sender_id, "Your total score is " + str(score) + ". Keep moving! 💪🏼", False)




    elif payload == "BUTTON_CONTINUE":
        update_status(mysql, sender_id, 1)
        msg_continue = ["Great! Let's move on.", 
                        "Okay, let's continue.", 
                        "All right! Let's move on.", 
                        "Let's continue learning."]
        random.shuffle(msg_continue)
        send_gotit_quickreply(sender_id, msg_continue[0], False)

    elif payload == "BUTTON_I_NEED_A_HINT":
        msg_hint = "Okay. Which of these is the right answer?👇🏼"
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        pretty_print(qa_model.DKB[QID], mode='QID')
        send_hint(sender_id, msg_hint, qa_model, QID)

    elif payload == "BUTTON_I_DONT_KNOW":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_GIVEUP_YES":
        send_message(sender_id, "You didn't earn any points this time.")
        msg_giveup_yes = "That’s okay, you’ll get it next time! ☺️"
        send_message(sender_id, msg_giveup_yes)
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        insert_score(mysql, sender_id,QID,payload,0)
        send_correct_answer(sender_id, template_conversation, standard_answer)
        update_status(mysql, sender_id, 1)

    elif payload == "BUTTON_GIVEUP_NO":
        msg_giveup_no = "Okay! Let's try again 💪🏼 Tell me which of these is the right answer:"
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        send_hint(sender_id, msg_giveup_no, qa_model, QID)

    elif payload == "BUTTON_PRACTICE_MODE":
        msg_choose_mode = "Sure, which subject would you like me to quiz you on?👇🏼"
        send_choose_subject(sender_id, template_conversation)

    elif payload[:10] == "BUTTON_DKB":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        msglist_incorrect = ["I'm sorry, but that was incorrect. You didn't earn any points 😞",
                             "That's not quite right. You didn't earn any points 😞"]
        send_message(sender_id, random.choice(msglist_incorrect))
        insert_score(mysql, sender_id,QID,payload,0)
        send_correct_answer(sender_id, template_conversation, standard_answer)
        update_status(mysql, sender_id, 1)

    elif payload[:10] == "BUTTON_AKB":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        score = 3
        send_message(sender_id, "You earned "+str(score)+ " points!")
        insert_score(mysql, sender_id,QID,payload,score)
        send_correct_answer(sender_id, template_conversation, standard_answer)
        update_status(mysql, sender_id, 1)

    elif payload == "BUTTON_SCIENCE":
        msglist_subject = ["All right! I’ll quiz you on science!",
                     "Okay! Let’s see how much you know about science!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("science")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload)
        send_question(sender_id, template_conversation, question)

    elif payload == "BUTTON_GRE":
        msglist_subject = ["All right! I’ll quiz you on GRE!",
                     "Okay! Let’s see how much you know about GRE!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("gre")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload)
        send_question(sender_id, template_conversation, question)

    elif payload == "BUTTON_SAFETY":
        msglist_subject = ["All right! I’ll quiz you on SAFETY!",
                     "Okay! Let’s see how much you know about SAFETY!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("safety")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload)
        send_question(sender_id, template_conversation, question)
    elif payload == "BUTTON_RANDOM":
        msglist_random = ["Okay! Let’s mix it up! 🎲",
                     "All right! A little bit of everything! 🎲"]
        msg_random = random.choice(msglist_random)
        send_message(sender_id, msg_random)
        question, QID = qa_model.pickRandomQuestion()
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload)
        send_question(sender_id, template_conversation, question)

    elif payload == 'BUTTON_SWITCH_SUBJECT' or payload == 'BUTTON_SURE':
        msg_choose_mode = "Sure, which subject would you like me to quiz you on?👇🏼"
        send_choose_subject(sender_id, template_conversation)

    elif payload == "BUTTON_WHY":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        support_sentence = qa_model.getSupport(QID)
        send_explanation(sender_id, template_conversation, support_sentence)

    elif payload == "BUTTON_CHECK_TOTAL_SCORE":
        totalscore = str(show_score(mysql, sender_id))
        msglist_total_score = ["Your total score is "+totalscore+". Keep it up! 💪🏼",
                              "Your total score is "+totalscore+". Great work! 💪🏼"]
        send_gotit_quickreply(sender_id, random.choice(msglist_total_score), False)

    elif payload == "BUTTON_REPORT_BUG":
        msg_report_bug = "Okay, I’ll take a note of that. Thanks for the feedback! 👍🏼"
        insert_score(mysql,sender_id,-1,message_text,-1)
        send_bugreport(sender_id, msg_report_bug)

    elif payload == "BUTTON_ABOUT_QUIZBOT":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_USER_MANUAL_1":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_USER_MANUAL_2":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_image(sender_id, payload, chatbot_text, "image_2")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_USER_MANUAL_3":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_USER_MANUAL_4":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_image(sender_id, payload, chatbot_text, "image_2")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_USER_MANUAL_5":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_USER_MANUAL_6":
        send_image(sender_id, payload, chatbot_text, "image_1")
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_USER_MANUAL_7":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")

    elif payload == "BUTTON_CONTACT":
        send_conversation(sender_id, payload, chatbot_text, template_conversation, "conversation_1")


    # look for next similar question based off the pre-trained model
    elif payload == "BUTTON_NEXT_QUESTION" or payload == "BUTTON_GOT_IT_NEXT":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        if show_status(mysql, sender_id):
            last_subject = show_last_qid_subject(mysql, sender_id)[1]
            #if last_subject == 'random' or last_subject == 'no record':
            if last_subject in ["BUTTON_SCIENCE", "BUTTON_GRE", "BUTTON_SAFETY"]:
                if last_subject == "BUTTON_SCIENCE":
                    question, QID = qa_model.pickSubjectRandomQuestion("science")
                elif last_subject == "BUTTON_GRE":
                    question, QID = qa_model.pickSubjectRandomQuestion("gre")
                elif last_subject == "BUTTON_SAFETY":
                    question, QID = qa_model.pickSubjectRandomQuestion("safety")
            else:
                question, QID = qa_model.pickRandomQuestion()
            update_status(mysql, sender_id, 0)
            insert_question(mysql, sender_id, QID,last_subject)
        else:
            QID = show_last_qid_subject(mysql, sender_id)[0]
            question = qa_model.pickLastQuestion(QID)
        send_question(sender_id, template_conversation, question)


def respond_to_messagetext(message_text, sender_id, qa_model, chatbot_text, template_conversation, mysql):
    '''
        ================= Chatbot's reply to a message text =================
    '''
    message_text = message_text.lower()
    QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database

    if message_text == "Practice Mode "+u'\u270F':
        send_choose_subject_quick_reply(sender_id, template_conversation)
        insert_question(mysql, sender_id,'-11','MENU_PRACTICE_MODE')

    elif message_text == "next question" or message_text == "got it, next!" or message_text[:4] == "sure":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        if show_status(mysql, sender_id):
            last_subject = show_last_qid_subject(mysql, sender_id)[1]
            if last_subject in ["BUTTON_SCIENCE", "BUTTON_GRE", "BUTTON_SAFETY"]:
                question, QID = qa_model.pickSubjectRandomQuestion(last_subject)
            else:
                question, QID = qa_model.pickRandomQuestion()
            update_status(mysql, sender_id, 0)
            insert_question(mysql, sender_id,QID,last_subject)
            send_question(sender_id, template_conversation, question)
        else:
            standard_answer = qa_model.getAnswer(QID)
            score = qa_model.compute_score(message_text, QID)
            if score < 5:
                msglist_incorrect = ["I'm sorry, but that was incorrect. You didn't earn any points 😞",
                                    "That's not quite right. You didn't earn any points 😞"]
                send_message(sender_id, random.choice(msglist_incorrect))
                #insert_score(mysql, sender_id, QID, message_text, 0)
            elif score < 10:
                send_message(sender_id, "You earned "+str(score)+ " points!")
            else:
                msglist_correct = ["That’s right! 🎉", "Correct! 🎊", "Good job! 🙌🏼"]
                msg_correct = random.choice(msglist_correct)
                send_message(sender_id, msg_correct)
                send_message(sender_id, "You earned 10 points!")
            send_correct_answer(sender_id, template_conversation, standard_answer)
            insert_score(mysql, sender_id, QID, message_text, score)
            update_status(mysql, sender_id, 1)


    else: # user's response in natural language
        if not show_status(mysql, sender_id):
            standard_answer = qa_model.getAnswer(QID)
            score = qa_model.compute_score(message_text, QID)
            if score < 5:
                msglist_incorrect = ["I'm sorry, but that was incorrect. You didn't earn any points 😞",
                                    "That's not quite right. You didn't earn any points 😞"]
                send_message(sender_id, random.choice(msglist_incorrect))
                #insert_score(mysql, sender_id, QID, message_text, 0)
            elif score < 10:
                send_message(sender_id, "You earned "+str(score)+ " points!")
            else:
                msglist_correct = ["That’s right! 🎉", "Correct! 🎊", "Good job! 🙌🏼"]
                msg_correct = random.choice(msglist_correct)
                send_message(sender_id, msg_correct)
                send_message(sender_id, "You earned 10 points!")
            send_correct_answer(sender_id, template_conversation, standard_answer)
            insert_score(mysql, sender_id, QID, message_text, score)
            update_status(mysql, sender_id, 1)
        else:
            update_status(mysql, sender_id, 1)
            response_message = ["That sounds interesting. Would you want more quiz questions to practice? I'm here to help 😄"]
            send_conversation(sender_id, DELAY_TIME, response_message, "BUTTON_SURE")


