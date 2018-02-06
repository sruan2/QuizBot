from message import *
from database import *
from time import gmtime, strftime
import random


# ================= Chatbot's reply to a postback =================
def respond_to_postback(payload, message_text, sender_id, qa_model, mysql):
    message_text = message_text.lower()

    if payload == "GET_STARTED_PAYLOAD":
        msg_intro_1 = "Hi there! My name is Mr. Owl 🦉 and I’m here to help you learn all about science 🔬"
        msg_intro_2 = "Here’s how it works. I ask you questions, and you give me answers. If you get the right answer, you earn points! 🎉"
        msg_intro_3 = "So, are you ready?"
        send_picture(sender_id, "https://lh3.googleusercontent.com/3xMTHXRP2WpVISylhzubvU5b1ffCnLRDGLNRyLjtLYvudOekwpjU15k1AyKUQPRoAu8t9X5dgSO0oU8HKW29z41edjSQC3s5bbStHAQ9WpLN61dchCTdc3dM1VIChuMybCBrRbYB", "", "")
        send_message(sender_id, msg_intro_1)
        send_message(sender_id, msg_intro_2)
        send_ready_go(sender_id, msg_intro_3)

    elif payload == "MENU_SCORE":
        score = show_score(mysql, sender_id)
        send_gotit_quickreply(sender_id, "Your total score is "+str(score)+". Keep moving!") 

    elif payload == "MENU_LEADERBOARD":
        records = show_top_10(mysql)
        sentence = ("\n").join(["No." + str(i + 1) + " " + str(records[i][0]+' '+records[i][1]) + ": " + str(records[i][2]) for i in range(len(records))])
        send_gotit_quickreply(sender_id, "Leaderboard: \n" + sentence) 
    
    ######## Sherry: Seems that none of the following conditions is ever met ###################    
    elif payload == "YUP_IM_READY":
        update_status(mysql, sender_id, 1)
        msg_great_get_started = "“Great! Let’s get started 🚀”"
        send_message(sender_id, msg_great_get_started)
        choose_mode_quick_reply(sender_id) 

    elif payload == "I_NEED_A_HINT":
        msg_hint = "Okay. Which is these is the right answer?👇"
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        send_hint(sender_id, msg_hint, qa_model, QID)

    elif payload == "I_DONT_KNOW":
        send_giveup(sender_id)

    elif payload == "GIVEUP_YES":
        msg_giveup_yes = "That’s okay, you’ll get it next time! ☺️"
        send_giveup(sender_id, msg_giveup_yes)
        # show answer

    elif payload == "GIVEUP_NO":
        pass
        # ask the question again
        
    
    elif payload == "PRACTICE_MODE":
        msg_choose_mode = "Sure, which subject would you like me to quiz you on?👇"
        choose_subject_quick_reply(sender_id, msg_choose_mode)


    elif payload == "D1KB" or payload == "D2KB" or payload == "D3KB":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        score = 0
        send_message(sender_id, "You earned "+str(score)+ " points!")
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_score(mysql, sender_id,QID,payload,score,time)
        send_why_quickreply(sender_id, QID, standard_answer)    
        update_status(mysql, sender_id, 1)         

    elif payload == "AKB":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        standard_answer = qa_model.getAnswer(QID)
        score = 3
        send_message(sender_id, "You earned "+str(score)+ " points!")
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_score(mysql, sender_id,QID,payload,score,time)
        send_why_quickreply(sender_id, QID, standard_answer)    
        update_status(mysql, sender_id, 1)        

    elif payload == "PHYSICS":
        msglist_subject = ["All right! Let’s I’ll quiz you on Physics!",
                           "Okay! Let’s see how much you know about Physics!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("physics")
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text,time)
        send_a_question(sender_id, question)

    elif payload == "CHEMISTRY":
        msglist_subject = ["All right! Let’s I’ll quiz you on Chemistry!",
                           "Okay! Let’s see how much you know about Chemistry!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("chemistry")
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text,time)
        send_a_question(sender_id, question)

    elif payload == "BIOLOGY":
        msglist_subject = ["All right! Let’s I’ll quiz you on Biology!",
                           "Okay! Let’s see how much you know about Biology!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("biology")
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text,time)
        send_a_question(sender_id, question)

    elif payload == "GEOLOGY":
        msglist_subject = ["All right! Let’s I’ll quiz you on Geology!",
                     "Okay! Let’s see how much you know about Geology!"]
        msg_subject = random.choice(msglist_subject)
        send_message(sender_id, msg_subject)
        question, QID = qa_model.pickSubjectRandomQuestion("geology")
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID, message_text,time)
        send_a_question(sender_id, question)

    elif payload == "RANDOM":
        msglist_random =["Okay! Let’s mix it up! 🎲",
                     "All right! A little bit of everything! 🎲"]
        msg_random = random.choice(msglist_random)
        send_message(sender_id, msg_random)
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text,time)
        send_a_question(sender_id, question)

    elif payload == 'SWITCH_SUBJECT' or payload == 'SURE':
        send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

    elif payload == "WHY":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        support_sentence = qa_model.getSupport(QID)
        send_why2_quickreply(sender_id, "Here's an explanation: " + support_sentence)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_score(mysql, sender_id,QID,"why",0,time)        

    elif payload == "CHECK_TOTAL_SCORE":
        send_gotit_quickreply(sender_id, "Your accumulated points are "+str(show_score(mysql, sender_id)))

    elif payload == "REPORT_BUG":
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_score(mysql,sender_id,-1,message_text,-1,time)
        send_why2_quickreply(sender_id, "Thanks for letting us know. We will use your feedback to improve our algorithm! Now what would you like to do next?")

    # look for next similar question based off the pre-trained model
    elif payload == "NEXT_QUESTION" or payload == "GOT_IT_NEXT":
        QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database
        if show_status(mysql, sender_id):
            last_subject = show_last_qid_subject(mysql, sender_id)[1]
            if last_subject == 'random' or last_subject == 'no record':
                question, QID = qa_model.pickRandomQuestion()
            else:
                question, QID = qa_model.pickSubjectRandomQuestion(last_subject)
            update_status(mysql, sender_id, 0)
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            insert_question(mysql, sender_id,QID,last_subject,time)
        else: 
            QID = show_last_qid_subject(mysql, sender_id)[0]
            question = qa_model.pickLastQuestion(QID)
        send_a_question(sender_id, question)

    elif payload == "CHALLENGE_MODE":
        send_message(sender_id, "I'm here to answer your questions! Just type your question below :-) ")





# ================= Chatbot's reply to a message text =================
def respond_to_messagetext(message_text, sender_id, qa_model, mysql):
    message_text = message_text.lower()
    QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database

    if message_text == "Practice Mode "+u'\u270F':
        send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47') 
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,'-11','SWITCH_SUBJUECT',time)

    #elif message_text == "I need a hint...":
        #send_multiple_choice()
                                   

    elif message_text == "next question" or message_text == "got it, next!" or message_text[:4] == "sure":

        if show_status(mysql, sender_id):
            last_subject = show_last_qid_subject(mysql, sender_id)[1]
            if last_subject == 'random' or last_subject == 'no record':
                question, QID = qa_model.pickRandomQuestion()
            else:
                question, QID = qa_model.pickSubjectRandomQuestion(last_subject)
            update_status(mysql, sender_id, 0)
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            insert_question(mysql, sender_id,QID,last_subject,time)
        else: 
            QID = show_last_qid_subject(mysql, sender_id)[0]
            question = qa_model.pickLastQuestion(QID)
        send_a_question(sender_id, question)

    # I comment out this part as there is bug here
    # elif app.session[sender_id]["answering"] == True:
    #     answer = tfidf.Featurize(message_text)
    #     send_message(sender_id, answer)    

    elif "yup! i'm ready!" in message_text:
        update_status(mysql, sender_id, 1)
        choose_mode_quick_reply(sender_id) 


    elif message_text[:4] == "why":
        support_sentence = qa_model.getSupport(QID)
        send_why2_quickreply(sender_id, "Here's an explanation: " + support_sentence)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_score(mysql, sender_id,QID,"why",0,time)

    elif message_text == "check total score":
        send_gotit_quickreply(sender_id, "Your accumulated points are "+str(show_score(mysql, sender_id)))

    elif message_text == "report bug":
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_score(mysql, sender_id,-1,message_text,-1,time)
        send_why2_quickreply(sender_id, "Thanks for letting us know. We will use your feedback to improve our algorithm! Now what would you like to do next?")

    elif message_text == "physics":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_a_question(sender_id, question)

    elif message_text == "chemistry":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_a_question(sender_id, question)

    elif message_text == "biology":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_a_question(sender_id, question)

    elif message_text == "geology":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_a_question(sender_id, question)
    
    elif message_text == "random":
        question, QID = qa_model.pickRandomQuestion()
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_a_question(sender_id, question)

    elif message_text == 'switch subject':
        send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

    else: # user's respons in natural language    
        if not show_status(mysql, sender_id):
            standard_answer = qa_model.getAnswer(QID)
            score = qa_model.compute_score(message_text, QID)
            send_message(sender_id, "You earned "+str(score)+ " points!")
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            insert_score(mysql, sender_id,QID,message_text,score,time)
            send_why_quickreply(sender_id, QID, standard_answer)    
            update_status(mysql, sender_id, 1) 
        else:
            update_status(mysql, sender_id, 1)
            send_interesting(sender_id, "That sounds interesting. Would you want more quiz questions to practice? I'm here to help :) ")


