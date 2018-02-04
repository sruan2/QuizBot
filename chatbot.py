from message import *
from database import *



def respond_to_postback(message_text, sender_id, mysql):
    if message_text == "get started":
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
        question, QID = qa_md.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "chemistry":
        question, QID = qa_md.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "biology":
        question, QID = qa_md.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "geology":
        question, QID = qa_md.pickSubjectRandomQuestion(message_text)
        update_status(mysql, sender_id, 0)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_question(mysql, sender_id,QID,time)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text == "random":
        question, QID = qa_md.pickSubjectRandomQuestion(message_text)
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
                question, QID = qa_md.pickRandomQuestion()
            else:
                question, QID = qa_md.pickSubjectRandomQuestion(last_subject)
            update_status(mysql, sender_id, 0)
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            insert_question(mysql, sender_id,QID,last_subject,time)
        else: 
            QID = show_last_qid_subject(sender_id)[0]
            question = qa_md.pickLastQuestion(QID)
        send_message(sender_id, "Question."+str(QID)+": "+question)

    elif message_text[0:9] == "answering":
        send_message(sender_id, "I'm here to answer your questions! Just type your question below :-) ")