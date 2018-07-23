'''This module handles quizbot and flashcard database operations'''
import os
from flask import request
from time import *
from datetime import datetime
import emoji

from utils import pretty_print


def insert_conversation(mysql, sender, receiver, dialog, tp, time_stamp):
    '''Insert into conversation table
    Returns:
        Unique id (uid) of the inserted row. This is used for cross-reference.
    '''
    dialog = emoji.demojize(dialog)  # convert emoji to text
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute("INSERT INTO conversation (sender, recipient, time_stamp, type, dialogue) VALUES (%s, %s, %s, %s, %s)",
                    (sender, receiver, time_stamp, tp, dialog))
        cur.execute("SELECT LAST_INSERT_ID()")
        uid = cur.fetchall()[0][0]
        con.commit()
        pretty_print("Insert into [conversation]", mode="Database")
        return uid
    except:
        con.rollback()
        pretty_print("Error in inserting into [conversation]", mode="BUG!")
        return None # To indicate a bug


def insert_user_history(mysql, user_id, qid, subject, begin_timestamp, begin_uid):
    '''Insert (partial) user history record into user_history table.
    This operation is called when the app sends the user a question'''
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute("INSERT INTO user_history (user_id, qid, subject, begin_timestamp, begin_uid) VALUES (%s, %s, %s, %s, %s);",
                    (user_id, qid, subject, begin_timestamp, begin_uid))
        con.commit()
        pretty_print("Insert into [user_history]", mode="Database")
    except:
        con.rollback()
        pretty_print("Error in inserting into [user_history]", mode="BUG!")


def show_last_begin_uid(mysql, user_id):
    '''Retrieve begin_uid based on user_id'''
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT begin_uid from user_history where user_id = %s order by begin_timestamp desc limit 1", [user_id])
    rows = cur.fetchall()
    return rows[0]


def update_user_history(mysql, user_id, score, end_uid, end_timestamp):
    '''Updating user_history table: add score, end_uid, end_timestamp entries'''
    begin_uid = show_last_begin_uid(mysql, user_id)
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute("UPDATE table_name SET score = %s, end_timestamp = %s WHERE begin_uid = %s;", (score, end_timestamp, begin_uid))
        con.commit()
        pretty_print("Update [user_history]", mode="Database")
    except:
        con.rollback()
        pretty_print("Error in updating [user_history]", mode="BUG!")


def insert_user(mysql, user_id, user_firstname, user_lastname):
    '''Insert a new user into [user]'''
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute("INSERT INTO user (user_id, user_firstname, user_lastname, reg_time) VALUES (%s, %s, %s, %s)",
                    (user_id, user_firstname, user_lastname, time))
        con.commit()
        pretty_print("Insert a new user into [user]", mode="Database")
        pretty_print('{} {}'.format(user_firstname, user_lastname))
    except:
        con.rollback()
        pretty_print("Error in inserting into [user]", mode="BUG!")


def show_user_id_list(mysql):
    '''Return all users in the [user] database'''
    cur = mysql.connection.cursor()
    cur.execute("select user_id from user")
    rows = cur.fetchall()
    return [x[0] for x in rows]


def update_user_current_subject(mysql, user_id, subject):
    '''Update the current subject of the specified user'''
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute(
            "update user set current_subject = %s where user_id = %s", (subject, user_id))
        con.commit()
        pretty_print("Update current_subject in [user] table", mode="Database")
    except:
        con.rollback()
        pretty_print(
            "Error in updating current_subject in [user] table", mode="BUG!")




# update user question-answer loop status
def update_status(mysql, user_id, status):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute(
                "update user set user_status = %s where user_id = %s", (status, user_id))
            con.commit()
            pretty_print("Update status successfully added", mode="Database")
        except:
            con.rollback()
            pretty_print(
                "Error in updating user status operation", mode="BUG!")


# update the user name
def update_user_name(mysql, user_id, user_firstname, user_lastname):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("update user set user_firstname = %s, user_lastname = %s where user_id = %s",
                        (user_firstname, user_lastname, user_id))
            con.commit()
            pretty_print("Update name successfully added", mode="Database")
        except:
            con.rollback()
            pretty_print("Error in updating user name operation", mode="BUG!")


def show_status(mysql, user_id):
    # cur = mysql.connection.cursor()
    # cur.execute("select user_status from user where user_id = %s", [user_id])

    # rows = cur.fetchall()
    # if len(rows) != 0:
    #     return rows[0][0]
    # else:
    #     return -1

    # sherry: not sure what this function is doing. return 0 for now.
    return 0


# insert user score
def insert_score(mysql, user_id, qid, answer, score):
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO scores (user_id, qid, answer, score, r_time) VALUES (%s, %s, %s, %s, %s)",
                        (user_id, qid, answer, score, time))
            con.commit()
            pretty_print("Score record successfully added", mode="Database")
        except:
            con.rollback()
            pretty_print("Error in inserting score operation", mode="BUG!")

# insert asked questions
def insert_question(mysql, user_id, qid, subject):
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO questions (user_id, qid, subject, r_time) VALUES (%s,%s,%s,%s)",
                        (user_id, qid, subject, time))
            con.commit()
            pretty_print("Questions record successfully added",
                         mode="Database")
        except:
            con.rollback()
            pretty_print("Error in inserting question operation", mode="BUG!")


# retrieve score based on user_id
def show_score(mysql, user_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT sum(score) from scores group by user_id having user_id = %s", [user_id])

    rows = cur.fetchall()
    return rows[0][0] if len(rows) > 0 else 0


# retrieve score based on user_id
def show_last_qid_subject(mysql, user_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT qid, subject from questions where user_id = %s order by id desc limit 1", [user_id])

    rows = cur.fetchall()
    return (rows[0][0] if len(rows) > 0 else -1, rows[0][1] if len(rows) > 0 else (-1, 'no record'))


# retrieve all qids
def show_all_qid(mysql, user_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT qid,subject from questions where user_id = %s order by id", [user_id])

    rows = cur.fetchall()
    rows = [r[0] for r in rows]
    rows.sort()
    science = [r for r in rows if r >= 0 and r < 50]
    safety = [r for r in rows if r >= 50 and r < 100]
    gre = [r for r in rows if r >= 100 and r < 150]
    return science, safety, gre


# show top 10 in leaderboard
def show_top_5(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT t2.user_firstname,t2.user_lastname,t1.sc from \
        (select user_id, sum(score) as sc from scores group by user_id order by sc desc) t1 join user t2 on t2.user_id = t1.user_id \
         order by t1.sc desc limit 5")

    rows = cur.fetchall()
    return rows


def show_current_ranking(mysql, id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_firstname, user_lastname, sc, rn from \
        (SELECT  user_id, sc, @uid:=@uid+1 AS rn FROM (SELECT @uid:= 0) s, (select user_id, sum(score) as sc from \
            scores group by user_id order by sc desc) a ) t1 join user t2 on t2.user_id = t1.user_id and t1.user_id = %s", [id])

    rows = cur.fetchall()
    return rows[0]


# show users who is newly added after 2018-07-12
def show_users_newly_added(mysql):
    date_format_time = "%Y-%m-%d %H:%M:%S"
    date_format_sql = "%Y-%m-%d %H:%i:%s"
    current_datetime = strftime(date_format_time, localtime())

    cur = mysql.connection.cursor()
    cur.execute("SELECT t2.user_id, t2.user_firstname, t1.r_time from (select user_id, min(r_time) as r_time from scores group by user_id) t1 \
        join users t2 on t2.user_id = t1.user_id order by t1.r_time ")

    rows = cur.fetchall()
    return [row[:2] for row in rows if (datetime.strptime(row[2], date_format_time) - datetime.strptime("2018-07-15 00:00:00", date_format_time)).days > 0]


# show users who are inactive for the last 24hr
def show_inactive_user(mysql):
    date_format_time = "%Y-%m-%d %H:%M:%S"
    date_format_sql = "%Y-%m-%d %H:%i:%s"
    current_datetime = strftime(date_format_time, localtime())

    cur = mysql.connection.cursor()
    cur.execute("SELECT t2.user_id, t2.user_firstname, t1.r_time from (select user_id, max(r_time) as r_time from scores group by user_id) t1 \
        join user t2 on t2.user_id = t1.user_id order by t1.r_time ")

    rows = cur.fetchall()
    return [row[:2] for row in rows if (datetime.strptime(current_datetime, date_format_time) - datetime.strptime(row[2], date_format_time)).days]


########## FLASHCARD ##########
# insert flashcard user info
def insert_user_flashcard(mysql, user_id, user_firstname, user_lastname):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO user (user_id, user_firstname, user_lastname) VALUES (%s, %s, %s)",
                        (user_id, user_firstname, user_lastname))
            con.commit()
            pretty_print("Flashcard User record successfully added",
                         mode="FC Database")
        except:
            con.rollback()
            pretty_print(
                "Error in inserting Flashcard user reocrd operation", mode="FC BUG!")


# insert flashcard user action
def insert_user_action_flashcard(mysql, user_id, qid, user_action):
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
