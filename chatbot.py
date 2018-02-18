# coding: utf8
from message import *
from database import *
import random
from leaderboard.generate_leaderboard import *


# ================= Chatbot's reply to a postback =================
def respond_to_postback(payload, message_text, sender_id, qa_model, mysql):
    message_text = message_text.lower()

    if payload == "GET_STARTED_PAYLOAD":
        msg_intro_1 = "Hi there! My name is Mr. Owl 🦉 and I’m here to help you learn all about science 🔬"
        msg_intro_2 = "Here’s how it works. I ask you questions, and you give me answers. If you get the right answer, you earn points! 🎉"
        msg_intro_3 = "For each question, you get 10 points if you get it right. You can also ask for a hint but you will get at most 3 points. You can click on the menu button to see the leaderboard. Also, feel free to send me voice messages since I can understand them too!"
        msg_intro_4 = "So, are you ready?"
        send_picture(sender_id, "https://www.smartprimer.org:8443/pictures/Owl_Design_Orange_cap.png", "", "")
        send_message(sender_id, msg_intro_1)
        send_message(sender_id, msg_intro_2)
        send_ready_go(sender_id, msg_intro_3)
        send_ready_go(sender_id, msg_intro_4)

    elif payload == "MENU_SCORE":
        score = show_score(mysql, sender_id)
        send_gotit_quickreply(sender_id, "Your total score is "+str(score)+". Keep moving!") 

    elif payload == "MENU_LEADERBOARD":
        records = show_top_5(mysql)
        cur_ranking = show_current_ranking(mysql, sender_id)
        sentence = ("\n").join(["No." + str(i + 1) + " " + str(records[i][0]+' '+records[i][1]) + ": " + str(records[i][2]) for i in range(len(records))])
        send_picture(sender_id, str(generate(records, cur_ranking)), "", "") 
        
    
    elif payload == "YUP_IM_READY" or payload == "CONTINUE":
        update_status(mysql, sender_id, 1)
        msg_great_get_started = "Great! Let’s get started 🚀"
        send_message(sender_id, msg_great_get_started)
        choose_mode_quick_reply(sender_id) 

    elif payload == "I_NEED_A_HINT":
        msg_hint = "Okay. Which of these is the right answer?👇"
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        send_hint(sender_id, msg_hint, qa_model, QID)

    elif payload == "I_DONT_KNOW":
        send_giveup(sender_id)

    elif payload == "GIVEUP_YES":
        send_message(sender_id, "You didn't earn any points this time.")
        msg_giveup_yes = "That’s okay, you’ll get it next time! ☺️"
        send_message(sender_id, msg_giveup_yes)
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        insert_score(mysql, sender_id,QID,payload,0)
        send_correct_answer(sender_id, QID, standard_answer)    
        update_status(mysql, sender_id, 1)
        # show answer

    elif payload == "GIVEUP_NO":
        msg_giveup_no = "Okay! Let's try again 💪 Tell me which of these is the right answer:"
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        send_hint(sender_id, msg_giveup_no, qa_model, QID)
        # QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        # question = qa_model.QA_KB.QKB[QID]
        # send_a_question(sender_id, question)
        # ask the question again
        
    
    elif payload == "PRACTICE_MODE":
        msg_choose_mode = "Sure, which subject would you like me to quiz you on?👇"
        choose_subject_quick_reply(sender_id, msg_choose_mode)


    elif payload == "DKB":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        msglist_incorrect = ["I'm sorry, but that was incorrect. You didn't earn any points 😞",
                             "That's not quite right. You didn't earn any points 😞"]
        send_message(sender_id, random.choice(msglist_incorrect))
        insert_score(mysql, sender_id,QID,payload,0)
        send_correct_answer(sender_id, QID, standard_answer)    
        update_status(mysql, sender_id, 1)         

    elif payload == "AKB":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        score = 3
        send_message(sender_id, "You earned "+str(score)+ " points!")
        insert_score(mysql, sender_id,QID,payload,score)
        send_correct_answer(sender_id, QID, standard_answer)    
        update_status(mysql, sender_id, 1)        

    elif payload == "PHYSICS":
        msglist_subject = ["All right! I’ll quiz you on physics!",
                           "Okay! Let’s see how much you know about physics!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("physics")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id, QID, payload) # contains an emoji
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "CHEMISTRY":
        msglist_subject = ["All right! Let’s I’ll quiz you on chemistry!",
                           "Okay! Let’s see how much you know about chemistry!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("chemistry")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id,QID,payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "BIOLOGY":
        msglist_subject = ["All right! I’ll quiz you on biology!",
                           "Okay! Let’s see how much you know about biology!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("biology")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id,QID,payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "GEOLOGY":
        msglist_subject = ["All right! I’ll quiz you on geology!",
                     "Okay! Let’s see how much you know about geology!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("geology")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id,QID, payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "GRE":
        msglist_subject = ["All right! I’ll quiz you on GRE!",
                     "Okay! Let’s see how much you know about GRE!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("gre")
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id,QID, payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "RANDOM":
        msglist_random =["Okay! Let’s mix it up! 🎲",
                     "All right! A little bit of everything! 🎲"]
        msg_random = random.choice(msglist_random)
        send_message(sender_id, msg_random)
        question, QID = qa_model.pickRandomQuestion()
        update_status(mysql, sender_id, 0)
        insert_question(mysql, sender_id,QID,payload)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == 'SWITCH_SUBJECT' or payload == 'SURE':
        msg_choose_mode = "Sure, which subject would you like me to quiz you on?👇"
        choose_subject_quick_reply(sender_id, msg_choose_mode)

    elif payload == "WHY":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        support_sentence = qa_model.getSupport(QID)
        send_message(sender_id, "Here's an explanation: ") 
        send_explanation(sender_id, support_sentence) 

    elif payload == "CHECK_TOTAL_SCORE":
        totalscore = str(show_score(mysql, sender_id))
        msglist_total_score = ["Your total score is "+totalscore+". Keep it up! 👊",
                              "Your total score is "+totalscore+". Great work! 👊"]
        send_gotit_quickreply(sender_id, random.choice(msglist_total_score))

    elif payload == "REPORT_BUG":
        msg_report_bug = "Okay, I’ll take a note of that. Thanks for the feedback! 👍"
        insert_score(mysql,sender_id,-1,message_text,-1)
        send_bugreport(sender_id, msg_report_bug)

    # look for next similar question based off the pre-trained model
    elif payload == "NEXT_QUESTION" or payload == "GOT_IT_NEXT":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        if show_status(mysql, sender_id):
            last_subject = show_last_qid_subject(mysql, sender_id)[1]
            #if last_subject == 'random' or last_subject == 'no record':
            if last_subject in ["physics", "chemistry", "biology", "geology", "gre"]:
                question, QID = qa_model.pickSubjectRandomQuestion(last_subject)
            else:
                question, QID = qa_model.pickRandomQuestion()
            update_status(mysql, sender_id, 0)
            insert_question(mysql, sender_id,QID,last_subject)
        else: 
            QID = show_last_qid_subject(mysql, sender_id)[0]
            question = qa_model.pickLastQuestion(QID)
        send_starting_question(sender_id)
        send_a_question(sender_id, question)

    elif payload == "CHALLENGE_MODE":
        send_message(sender_id, "The developers are working hard to get this feature implemented...")
        choose_mode_quick_reply(sender_id) 





# ================= Chatbot's reply to a message text =================
def respond_to_messagetext(message_text, sender_id, qa_model, mysql):
    message_text = message_text.lower()
    QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database

    if message_text == "Practice Mode "+u'\u270F':
        choose_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47') 
        insert_question(mysql, sender_id,'-11','PRACTICE_MODE')                                   

    # elif message_text == "next question" or message_text == "got it, next!" or message_text[:4] == "sure":

    #     if show_status(mysql, sender_id):
    #         last_subject = show_last_qid_subject(mysql, sender_id)[1]
    #         if last_subject == 'random' or last_subject == 'no record':
    #             question, QID = qa_model.pickRandomQuestion()
    #         else:
    #             question, QID = qa_model.pickSubjectRandomQuestion(last_subject)
    #         update_status(mysql, sender_id, 0)
    #         insert_question(mysql, sender_id,QID,last_subject)
    #     else: 
    #         QID = show_last_qid_subject(mysql, sender_id)[0]
    #         question = qa_model.pickLastQuestion(QID)
    #     send_starting_question(sender_id)    
    #     send_a_question(sender_id, question) 

    # elif "yup! i'm ready!" in message_text:
    #     update_status(mysql, sender_id, 1)
    #     choose_mode_quick_reply(sender_id) 


    # elif message_text[:4] == "why":
    #     support_sentence = qa_model.getSupport(QID)
    #     send_why2_quickreply(sender_id, "Here's an explanation: " + support_sentence)

    # elif message_text == "check total score":
    #     send_gotit_quickreply(sender_id, "Your accumulated points are "+str(show_score(mysql, sender_id)))

    # elif message_text == "report bug":
    #     insert_score(mysql, sender_id,-1,message_text,-1)
    #     send_why2_quickreply(sender_id, "Thanks for letting us know. We will use your feedback to improve our algorithm! Now what would you like to do next?")

    # elif message_text == "physics":
    #     question, QID = qa_model.pickSubjectRandomQuestion(message_text)
    #     update_status(mysql, sender_id, 0)
    #     insert_question(mysql, sender_id,QID,message_text.lower())
    #     send_starting_question(sender_id)
    #     send_a_question(sender_id, question)

    # elif message_text == "chemistry":
    #     question, QID = qa_model.pickSubjectRandomQuestion(message_text)
    #     update_status(mysql, sender_id, 0)
    #     insert_question(mysql, sender_id,QID,message_text.lower())
    #     send_starting_question(sender_id)
    #     send_a_question(sender_id, question)

    # elif message_text == "biology":
    #     question, QID = qa_model.pickSubjectRandomQuestion(message_text)
    #     update_status(mysql, sender_id, 0)
    #     insert_question(mysql, sender_id,QID,message_text.lower())
    #     send_starting_question(sender_id)
    #     send_a_question(sender_id, question)

    # elif message_text == "geology":
    #     question, QID = qa_model.pickSubjectRandomQuestion(message_text)
    #     update_status(mysql, sender_id, 0)
    #     insert_question(mysql, sender_id,QID,message_text)
    #     send_starting_question(sender_id)
    #     send_a_question(sender_id, question)
    
    # elif message_text == "random":
    #     question, QID = qa_model.pickRandomQuestion()
    #     update_status(mysql, sender_id, 0)
    #     insert_question(mysql, sender_id, QID, message_text)
    #     send_starting_question(sender_id)
    #     send_a_question(sender_id, question)

    # elif message_text == 'switch subject':
    #     choose_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

    else: # user's respons in natural language    
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


