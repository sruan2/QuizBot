from message import *
from database import *
from time import gmtime, strftime


# ================= Chatbot's reply to a postback =================
def respond_to_postback(payload, message_text, sender_id, qa_model, mysql):
    message_text = message_text.lower()

    if payload == GET_STARTED_PAYLOAD:
        send_ready_go(sender_id, "Hi! Welcome! I'm your personal tutor Mr.Q and I'm here to help you master science! Ready? Go!"+u'\uD83D\uDE0A')
        
    elif "yup! i'm ready!" in message_text:
        update_status(mysql, sender_id, 1)
        send_mode_quick_reply(sender_id, "Now tell me which mode you would like to choose:"+u'\uD83D\uDC47') 

    elif message_text == "check total score":
        score = show_score(mysql, sender_id)
        send_gotit_quickreply(sender_id, "Your total score is "+str(score)+". Keep moving!") 

    elif message_text == "check leaderboard":
        records = show_top_10(mysql)
        sentence = ("\n").join(["No." + str(i + 1) + " " + str(records[i][0]+' '+records[i][1]) + ": " + str(records[i][2]) for i in range(len(records))])
        send_gotit_quickreply(sender_id, "Leaderboard: \n" + sentence) 
    elif message_text[0:9] == "quiz mode":
        send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

    elif message_text == "physics":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "chemistry":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "biology":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "geology":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "random":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == 'switch subject' or message_text[:4] == 'sure':
        send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')


    # look for next similar question based off the pre-trained model
    elif message_text == "next question":
        if show_status(mysql, sender_id):
            last_subject = show_last_qid_subject(sender_id)[1]
            if last_subject == 'random' or last_subject == 'no record':
                question, QID = qa_model.pickRandomQuestion()
            else:
                question, QID = qa_model.pickSubjectRandomQuestion(last_subject)
            update_status(mysql, sender_id, 0)
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            insert_question(mysql, sender_id,QID,last_subject,time)
        else: 
            QID = show_last_qid_subject(sender_id)[0]
            question = qa_model.pickLastQuestion(QID)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text[0:9] == "answering":
        send_message(sender_id, "I'm here to answer your questions! Just type your question below :-) ")




# ================= Chatbot's reply to a message text =================
def respond_to_messagetext(message_text, sender_id, qa_model, mysql):
    message_text = message_text.lower()
    QID, _ = show_last_qid_subject(mysql, sender_id) # retrieve the qid and the subject from database

    if message_text == "quiz mode "+u'\u270F':
        send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47') 
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,'-11','SWITCH_SUBJUECT',time)
                                   

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
        send_message(sender_id, "Question."+str(QID)+": "+question)

    # I comment out this part as there is bug here
    # elif app.session[sender_id]["answering"] == True:
    #     answer = tfidf.Featurize(message_text)
    #     send_message(sender_id, answer)    

    elif "yup! i'm ready!" in message_text:
        update_status(mysql, sender_id, 1)
        send_mode_quick_reply(sender_id, "Now tell me which mode you would like to choose:"+u'\uD83D\uDC47') 


    elif message_text[:4] == "why":
        support_sentence = qa_model.getSupport(QID)
        send_why2_quickreply(sender_id, "Here's an explanation: " + support_sentence)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_score(mysql, sender_id,QID,"why",0,time)

    elif message_text == "check total score":
        send_gotit_quickreply(sender_id, "Your accumulated score is "+str(show_score(mysql, sender_id)))

    elif message_text == "report bug":
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_score(sender_id,-1,message_text,-1,time)
        send_interesting(sender_id, "Thanks for reporting! Would you want more questions to practice? :) ")

    elif message_text == "physics":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "chemistry":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "biology":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "geology":
        question, QID = qa_model.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_message(sender_id, "Question."+str(QID)+": "+question)
    
    elif message_text == "random":
        question, QID = qa_model.pickRandomQuestion()
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,message_text.lower(),time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == 'switch subject':
        send_subject_quick_reply(sender_id, "Now tell me which subject you would like to choose:"+u'\uD83D\uDC47')

    else: # user's respons in natural language    
        if not show_status(mysql, sender_id):
            standard_answer = qa_model.getAnswer(QID)
            score = qa_model.compute_score(message_text, QID)
            send_message(sender_id, "Your score this round is "+str(score))
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            insert_score(mysql, sender_id,QID,message_text,score,time)
            send_why_quickreply(sender_id, QID, standard_answer)    
            update_status(mysql, sender_id, 1) 
        else:
            update_status(mysql, sender_id, 1)
            send_interesting(sender_id, "That sounds interesting. Would you want more quiz questions to practice? I'm here to help :) ")


