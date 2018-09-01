'''This module handles quizbot and flashcard database operations'''
import os
from flask import request
from time import *
from datetime import datetime
import emoji
import MySQLdb
from utils import pretty_print

########## QUIZBOT ##########


def insert_conversation(mysql, sender, receiver, dialog, tp, time_stamp):
    '''
        This function inserts the conversation record into the [user_history] table of <QUIZBOT> database.
        Returns:
            Unique id (uid) of the inserted row. This is used for cross-reference.
    '''
    dialog = emoji.demojize(dialog)  # convert emoji to text
    try:
        con = mysql.connection
        if con == None:
            con = MySQLdb.connect(db=os.environ["DB"], user=os.environ["DB_USER"],
                                  passwd=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"])
        cur = con.cursor()
        cur.execute("INSERT INTO conversation (sender, recipient, time_stamp, type, dialogue) VALUES (%s, %s, %s, %s, %s)",
                    (sender, receiver, time_stamp, tp, dialog))
        cur.execute("SELECT LAST_INSERT_ID()")
        uid = cur.fetchall()[0][0]
        con.commit()
        return uid
    except:
        con.rollback()
        pretty_print("Error in inserting into [conversation]", mode="BUG!")
        return None


def insert_user_history(mysql, user_id, qid, subject, begin_uid):
    '''
        This function inserts (partial) user history record into the [user_history] table of <QUIZBOT> database.
        This operation is called when the app sends the user a question
    '''
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute("INSERT INTO user_history (user_id, qid, subject, begin_uid) VALUES (%s, %s, %s, %s);",
                    (user_id, qid, subject, begin_uid))
        con.commit()
        pretty_print("Insert into [user_history]", mode="Database")
    except:
        con.rollback()
        pretty_print("Error in inserting into [user_history]", mode="BUG!")


def insert_user(mysql, user_id, user_firstname, user_lastname):
    '''
        This function inserts a new user in the [user] table of <QUIZBOT> database.
    '''
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute("INSERT INTO user (user_id, user_firstname, user_lastname, reg_time) VALUES (%s, %s, %s, %s);",
                    (user_id, user_firstname, user_lastname, time))
        con.commit()
        pretty_print("Insert a new user into [user]", mode="Database")
        pretty_print('{} {}'.format(user_firstname, user_lastname))
    except:
        con.rollback()
        pretty_print("Error in inserting into [user]", mode="BUG!")


def update_user_history(mysql, user_id, score, tp, begin_uid, end_uid):
    '''
        This function updates the [user_history] table (add score, end_uid entries) of <QUIZBOT> database.
    '''
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute("UPDATE user_history SET score = %s, type = %s, end_uid = %s WHERE begin_uid = %s AND user_id = %s;",
                    (score, tp, end_uid, begin_uid, user_id))
        con.commit()
        pretty_print("Update [user_history]", mode="Database")
    except:
        con.rollback()
        pretty_print("Error in updating [user_history]", mode="BUG!")


def update_user_current_subject(mysql, user_id, subject):
    '''
        This function updates the current subject of a specified user in the [user] table of <QUIZBOT> database.
    '''
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute(
            "UPDATE user SET current_subject = %s WHERE user_id = %s;", (subject, user_id))
        con.commit()
        pretty_print("Update current_subject in [user] table", mode="Database")
    except:
        con.rollback()
        pretty_print(
            "Error in updating current_subject in [user] table", mode="BUG!")


def show_user_id_list(mysql):
    '''
        This function returns all users in the [user] table of <QUIZBOT> database.
    '''
    cur = mysql.connection.cursor()
    cur.execute("select user_id from user")
    rows = cur.fetchall()
    return [x[0] for x in rows]


def show_last_begin_uid(mysql, user_id):
    '''
        This function returns the begin_uid in the [user_history] table of <QUIZBOT> database.
    '''
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute(
            "SELECT begin_uid FROM user_history WHERE user_id = %s;", [user_id])
        rows = cur.fetchall()
        return rows[-1][0]
    except:
        con.rollback()
        pretty_print(
            "Error in retrieving begin_uid from [user_history]", mode="BUG!")
        return None


def show_current_subject(mysql, user_id):
    '''
        This function returns the current subject in the [user] table of <QUIZBOT> database.
    '''
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT current_subject FROM user WHERE user_id = %s;", [user_id])
    rows = cur.fetchall()
    return rows[0][0]


def show_users_newly_added(mysql):
    '''
        This function returns the newly added users after 2018-07-23 in the [user] table of <QUIZBOT> database.
    '''
    date_format_time = "%Y-%m-%d %H:%M:%S"
    date_format_sql = "%Y-%m-%d %H:%i:%s"
    current_datetime = strftime(date_format_time, localtime())


    con = mysql.connection
    if con == None:
        con = MySQLdb.connect(db=os.environ["DB"], user=os.environ["DB_USER"],
                              passwd=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"])
    cur = con.cursor()
    cur.execute("SELECT user_id, user_firstname, reg_time FROM user;")

    rows = cur.fetchall()
    return [row[:2] for row in rows if (datetime.strptime(row[2], date_format_time) - datetime.strptime("2018-08-26 00:00:00", date_format_time)).days > 0]


def show_current_qid(mysql, user_id):
    '''
        This function returns the current qid in the [user_history] table of <QUIZBOT> database.
    '''
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT qid from user_history WHERE user_id = %s;", [user_id])
    rows = cur.fetchall()
    return rows[-1][0]


def show_user_history(mysql, user_id):
    '''
        This function returns the user history record used for the question sequencing model 
        initialization in the [user_history] table of <QUIZBOT> database.
    '''
    cur = mysql.connection.cursor()
    cur.execute("SELECT qid, score, time_stamp FROM (user_history RIGHT JOIN conversation \
        on user_history.begin_uid = conversation.uid) WHERE end_uid IS NOT NULL AND user_id = %s;", [user_id])
    rows = cur.fetchall()
    return rows


def show_timestamp(mysql, uid):
    '''
        This function returns the timestamp associated with a uid in the [conversation] table of <QUIZBOT> database.
    '''
    cur = mysql.connection.cursor()
    cur.execute("SELECT time_stamp FROM conversation WHERE uid = %s;", [uid])
    rows = cur.fetchall()
    return rows[-1][0]


########## FLASHCARD ##########
def insert_user_flashcard(mysql, user_id, user_firstname, user_lastname):
    '''
        This function inserts a user into the [users] table of <FLASHCARD> database.
    '''
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO users (user_id, user_firstname, user_lastname) VALUES (%s, %s, %s)",
                        (user_id, user_firstname, user_lastname))
            con.commit()
            pretty_print("Flashcard User record successfully added",
                         mode="FC Database")
        except:
            con.rollback()
            pretty_print(
                "Error in inserting Flashcard user reocrd operation", mode="FC BUG!")


def insert_user_action_flashcard(mysql, user_id, qid, user_action):
    '''
        This function inserts a user action into the [action] table of <FLASHCARD> database.
    '''
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO action (user_id, qid, event, r_time) VALUES (%s, %s, %s, %s)",
                        (user_id, qid, user_action, time))
            con.commit()
            pretty_print(
                "FLASHCARD User action record successfully added", mode="FC Database")
        except:
            con.rollback()
            pretty_print(
                "Error in inserting FLASHCARD user action reocrd operation", mode="FC BUG!")


def show_user_id_list_flashcard(mysql):
    '''
        This function returns all users in the [user] table of <FLASHCARD> database.
    '''
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM users")
    rows = cur.fetchall()
    return [x[0] for x in rows]


def show_user_history_flashcard(mysql, user_id):
    '''
        This function returns all users in the [user] table of <FLASHCARD> database.
    '''
    cur = mysql.connection.cursor()
    cur.execute('SELECT qid, event, r_time FROM (users RIGHT JOIN action ON users.user_id = action.user_id) WHERE users.user_id = %s AND action.event = "got it" OR action.event = "I don\'t know";', [user_id])
    rows = cur.fetchall()
    result = []
    for r in rows:
        if r[1] == "I don't know":
            result.append((r[0], 0, r[2]))
        else:
            result.append((r[0], 1, r[2]))
    return result
