# coding: utf8
from message import *
from database import *
import random
import time
from leaderboard.generate_leaderboard import *


# ================= Chatbot's reply to a postback =================
def respond_to_payload(payload, message_text, sender_id, sender_firstname, qa_model, mysql):
    message_text = message_text.lower()

    if payload == "GET_STARTED_PAYLOAD_1":
        msg_intro_1 = []
        msg_intro_1.append("Hi " + sender_firstname + "! My name is Mr. Owl 🦉 and I’m here to help you learn all about science🔬, verbal reasoning (GRE)📖, and safety🔥!")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/owlyellow.png", "", "")
        send_get_it(sender_id, msg_intro_1, 0.6, "GET_STARTED_PAYLOAD_2")

    elif payload == "GET_STARTED_PAYLOAD_2":
        msg_intro_2 = []
        msg_intro_2.append("Here’s how it works.")
        msg_intro_2.append("I ask you questions❓, and you give me answers ✅.")
        msg_intro_2.append("If you get the right answer, you earn points! 🎉")
        msg_intro_2.append("For each question, you get 10 points if you get it right.")
        send_get_it(sender_id, msg_intro_2, 0.6, "GET_STARTED_PAYLOAD_3")

    elif payload == "GET_STARTED_PAYLOAD_3":
        msg_intro_3 = []
        msg_intro_3.append("To discover more abilities of me, you can click on the menu button shown above.👆🏼")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/menubutton.jpg", "", "")
        send_get_it(sender_id, msg_intro_3, 0.6, "GET_STARTED_PAYLOAD_4")

    elif payload == "GET_STARTED_PAYLOAD_4":
        msg_intro_4 = []
        msg_intro_4.append("Feel free to ask for a hint when you get stuck and you will get at most 3 points.📗")
        msg_intro_4.append("You can track your learning progress by clicking on the menu button to see your total score. 💯")
        msg_intro_4.append("You can also switch the subjects using the menu button. 🔀")

        send_get_it(sender_id, msg_intro_4, 0.6, "GET_STARTED_PAYLOAD_5")

    elif payload == "GET_STARTED_PAYLOAD_5":
        msg_intro_5 = "I hope you enjoy the leaning journey!📝"
        msg_intro_6 = "So, are you ready?"

        time.sleep(0.6)
        send_message(sender_id, msg_intro_5)
        time.sleep(0.6)
        send_ready_go(sender_id, msg_intro_6)

    elif payload == "MENU_SCORE":
        score = show_score(mysql, sender_id)
        send_gotit_quickreply(sender_id, "Your total score is "+str(score)+". Keep moving!", False)

    elif payload == "BUTTON_YUP_IM_READY":
        update_status(mysql, sender_id, 1)
        msg_great_get_started = "Great!"
        send_message(sender_id, msg_great_get_started)
        choose_mode_quick_reply(sender_id)

    elif payload == "BUTTON_CONTINUE":
        update_status(mysql, sender_id, 1)
        msg_continue = ["Great! Let's move on.", 
                        "Okay, let's continue.", 
                        "All right! Let's move on.", 
                        "Let's continue learning."]
        random.shuffle(msg_continue)
        send_gotit_quickreply(sender_id, msg_continue[0], False)

    elif payload == "BUTTON_I_NEED_A_HINT":
        msg_hint = "Okay. Which of these is the right answer?👇"
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        pretty_print(qa_model.DKB[QID], mode='QID')
        send_hint(sender_id, msg_hint, qa_model, QID)

    elif payload == "BUTTON_I_DONT_KNOW":
        send_giveup(sender_id)

    elif payload == "BUTTON_GIVEUP_YES":
        send_message(sender_id, "You didn't earn any points this time.")
        msg_giveup_yes = "That’s okay, you’ll get it next time! ☺️"
        send_message(sender_id, msg_giveup_yes)
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        insert_score(mysql, sender_id,QID,payload,0)
        send_correct_answer(sender_id, QID, standard_answer)
        update_status(mysql, sender_id, 1)

    elif payload == "BUTTON_GIVEUP_NO":
        msg_giveup_no = "Okay! Let's try again 💪 Tell me which of these is the right answer:"
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        send_hint(sender_id, msg_giveup_no, qa_model, QID)

    elif payload == "BUTTON_PRACTICE_MODE":
        msg_choose_mode = "Sure, which subject would you like me to quiz you on?👇"
        choose_subject_quick_reply(sender_id, msg_choose_mode)

    elif payload[:10] == "BUTTON_DKB":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        msglist_incorrect = ["I'm sorry, but that was incorrect. You didn't earn any points 😞",
                             "That's not quite right. You didn't earn any points 😞"]
        send_message(sender_id, random.choice(msglist_incorrect))
        insert_score(mysql, sender_id,QID,payload,0)
        send_correct_answer(sender_id, QID, standard_answer)
        update_status(mysql, sender_id, 1)

    elif payload[:10] == "BUTTON_AKB":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        score = 3
        send_message(sender_id, "You earned "+str(score)+ " points!")
        insert_score(mysql, sender_id,QID,payload,score)
        send_correct_answer(sender_id, QID, standard_answer)
        update_status(mysql, sender_id, 1)

    elif payload == "BUTTON_SCIENCE":
        msglist_subject = ["All right! I’ll quiz you on science!",
                     "Okay! Let’s see how much you know about science!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("science")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "BUTTON_GRE":
        msglist_subject = ["All right! I’ll quiz you on GRE!",
                     "Okay! Let’s see how much you know about GRE!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("gre")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "BUTTON_SAFETY":
        msglist_subject = ["All right! I’ll quiz you on SAFETY!",
                     "Okay! Let’s see how much you know about SAFETY!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("safety")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "BUTTON_RANDOM":
        msglist_random =["Okay! Let’s mix it up! 🎲",
                     "All right! A little bit of everything! 🎲"]
        msg_random = random.choice(msglist_random)
        send_message(sender_id, msg_random)
        question, QID = qa_model.pickRandomQuestion()
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == 'BUTTON_SWITCH_SUBJECT' or payload == 'BUTTON_SURE':
        msg_choose_mode = "Sure, which subject would you like me to quiz you on?👇"
        choose_subject_quick_reply(sender_id, msg_choose_mode)

    elif payload == "BUTTON_WHY":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        support_sentence = qa_model.getSupport(QID)
        send_message(sender_id, "Here's an explanation: ")
        send_explanation(sender_id, support_sentence)

    elif payload == "BUTTON_CHECK_TOTAL_SCORE":
        totalscore = str(show_score(mysql, sender_id))
        msglist_total_score = ["Your total score is "+totalscore+". Keep it up! 👊",
                              "Your total score is "+totalscore+". Great work! 👊"]
        send_gotit_quickreply(sender_id, random.choice(msglist_total_score), False)

    elif payload == "BUTTON_REPORT_BUG":
        msg_report_bug = "Okay, I’ll take a note of that. Thanks for the feedback! 👍"
        insert_score(mysql,sender_id,-1,message_text,-1)
        send_bugreport(sender_id, msg_report_bug)

    elif payload == "BUTTON_ABOUT_QUIZBOT":
        msg_about_quizbot = []
        msg_about_quizbot.append("I'm Mr. Owl 🦉 and I'm a QuizBot to help you learn about science🔬, verbal reasoning (GRE)📖, and safety🔥.")
        msg_about_quizbot.append("I'm designed by a group of researchers from Stanford University Computer Science Department. ")
        msg_about_quizbot.append("I use technology in a scientific and interactive way to help you learn knowledge.")
        send_get_it(sender_id, msg_about_quizbot, 0.6, "BUTTON_CONTINUE")

    elif payload == "BUTTON_CONTACT":
        msg_contact = []
        msg_contact.append("If you have any questions, please contact the Protocol Director, Sherry Ruan at ssruan@stanford.edu, or Liwei Jiang at ljiang@colby.edu.")
        send_get_it(sender_id, msg_contact, 0.6, "BUTTON_CONTINUE")

    elif payload == "BUTTON_USER_MANUAL_1":
        msg_user_manual = []
        msg_user_manual.append("To get started, you can click on the get started button. ▶️")
        msg_user_manual.append("Doing so will enable the QuizBot to access your public information (First Name, Last Name).")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/getstartedbutton.png", "", "")
        send_get_it(sender_id, msg_user_manual, 0.6, "BUTTON_USER_MANUAL_2")

    elif payload == "BUTTON_USER_MANUAL_2":
        msg_user_manual = []
        msg_user_manual.append("You can click on the quick reply buttons to proceed to the next steps. 🔜")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/quickreplybutton.png", "", "")
        send_get_it(sender_id, msg_user_manual, 0.6, "BUTTON_USER_MANUAL_3")

    elif payload == "BUTTON_USER_MANUAL_3":
        msg_user_manual = []
        msg_user_manual.append("To study the questions, you can type in your answers in the test field and the QuizBot will evaluate the answers for you. ⌨️")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/typeanswer.png", "", "")
        send_get_it(sender_id, msg_user_manual, 0.6, "BUTTON_USER_MANUAL_4")

    elif payload == "BUTTON_USER_MANUAL_4":
        msg_user_manual = []
        msg_user_manual.append("If you don't know the answers, then you can tap on the hint button.💡")
        msg_user_manual.append("The hint will give you a list of potential answers and you can select one from them.👇🏼")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/needhintbutton.png", "", "")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/hintoptions.png", "", "")
        send_get_it(sender_id, msg_user_manual, 0.6, "BUTTON_USER_MANUAL_5")

    elif payload == "BUTTON_USER_MANUAL_5":
        msg_user_manual = []
        msg_user_manual.append("You can switch the subjects from the menu as well! 🔀")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/menubutton.jpg", "", "")
        send_picture(sender_id, "https://www.smartprimer.org:443/pictures/changesubjects.jpg", "", "")
        send_get_it(sender_id, msg_user_manual, 0.6, "BUTTON_USER_MANUAL_6")

    elif payload == "BUTTON_USER_MANUAL_6":
        msg_user_manual = []
        msg_user_manual.append("Okay, you are all set.")
        send_get_it(sender_id, msg_user_manual, 0.6, "BUTTON_GOT_IT_NEXT")

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
        send_starting_question(sender_id)
        send_a_question(sender_id, question)


# ================= Chatbot's reply to a message text =================
def respond_to_messagetext(message_text, sender_id, qa_model, mysql):
    message_text = message_text.lower()
    QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database

    if message_text == "Practice Mode "+u'\u270F':
        choose_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')
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
            send_starting_question(sender_id)
            send_a_question(sender_id, question)
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
                msglist_correct = ["That’s right! 🎉", "Correct! 🎊" or "Good job! 🙌"]
                msg_correct = random.choice(msglist_correct)
                send_message(sender_id, msg_correct)
                send_message(sender_id, "You earned 10 points!")
            send_correct_answer(sender_id, QID, standard_answer)
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
                msglist_correct = ["That’s right! 🎉", "Correct! 🎊" or "Good job! 🙌"]
                msg_correct = random.choice(msglist_correct)
                send_message(sender_id, msg_correct)
                send_message(sender_id, "You earned 10 points!")
            send_correct_answer(sender_id, QID, standard_answer)
            insert_score(mysql, sender_id, QID, message_text, score)
            update_status(mysql, sender_id, 1)
        else:
            update_status(mysql, sender_id, 1)
            send_interesting(sender_id, "That sounds interesting. Would you want more quiz questions to practice? I'm here to help :) ")


