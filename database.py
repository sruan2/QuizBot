import os
from flask import request
from time import *
from datetime import datetime
from utils import pretty_print

# insert user info
def insert_user(mysql, user_id,user_firstname,user_lastname,user_gender,user_status):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO user (user_id,user_firstname,user_lastname,user_gender,user_status) VALUES (%s, %s, %s, %s, %s)",(user_id,user_firstname,user_lastname,user_gender,user_status))
            con.commit()
            pretty_print("User record successfully added", mode="Database")
        except:
            con.rollback()
            pretty_print("Error in inserting user reocrd operation", mode="BUG!")

# update user question-answer loop status
def update_status(mysql, user_id, status):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("update user set user_status = %s where user_id = %s",(status, user_id))
            con.commit()
            pretty_print("Update status successfully added", mode="Database")
        except:
            con.rollback()
            pretty_print("Error in updating user status operation", mode="BUG!")

# update the user name
def update_user_name(mysql,user_id,user_firstname,user_lastname):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("update user set user_firstname = %s, user_lastname = %s where user_id = %s",(user_firstname, user_lastname, user_id))
            con.commit()
            pretty_print("Update name successfully added", mode="Database")
        except:
            con.rollback()
            pretty_print("Error in updating user name operation", mode="BUG!")

def show_status(mysql, user_id):
    cur = mysql.connection.cursor()
    cur.execute("select user_status from user where user_id = %s", [user_id])

    rows = cur.fetchall()
    if len(rows) != 0:
        return rows[0][0]
    else:
        return -1

# insert user score
def insert_score(mysql, user_id,qid,answer,score):
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO scores (user_id,qid,answer,score,r_time) VALUES (%s, %s, %s, %s, %s)", (user_id,qid,answer,score,time))
            con.commit()
            pretty_print("Score record successfully added", mode="Database")
        except:
            con.rollback()
            pretty_print("error in inserting score operation", mode="BUG!")

# insert asked questions
def insert_question(mysql, user_id, qid, subject):
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO questions (user_id,qid,subject,r_time) VALUES (%s,%s,%s,%s)",(user_id,qid,subject,time))
            con.commit()
            pretty_print("Questions record successfully added", mode="Database")
        except:
            con.rollback()
            pretty_print("Error in inserting question operation", mode="BUG!")

def show_user_id_list(mysql):
    cur = mysql.connection.cursor()
    cur.execute("select user_id from user")

    rows = cur.fetchall()
    return [x[0] for x in rows]

# retrieve score based on user_id
def show_score(mysql, user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT sum(score) from scores group by user_id having user_id = %s", [user_id])

    rows = cur.fetchall();
    return rows[0][0] if len(rows) > 0 else 0

# retrieve score based on user_id
def show_last_qid_subject(mysql, user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT qid,subject from questions where user_id = %s order by id desc limit 1", [user_id])

    rows = cur.fetchall();
    return (rows[0][0] if len(rows) > 0 else -1, rows[0][1] if len(rows) > 0 else 'no record')

# show top 10 in leaderboard
def show_top_5(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT t2.user_firstname,t2.user_lastname,t1.sc from \
        (select user_id, sum(score) as sc from scores group by user_id order by sc desc) t1 join user t2 on t2.user_id = t1.user_id \
         order by t1.sc desc limit 5")

    rows = cur.fetchall();
    return rows

def show_current_ranking(mysql, id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_firstname, user_lastname, sc, rn from \
        (SELECT  user_id, sc, @uid:=@uid+1 AS rn FROM (SELECT @uid:= 0) s, (select user_id, sum(score) as sc from \
            scores group by user_id order by sc desc) a ) t1 join user t2 on t2.user_id = t1.user_id and t1.user_id = %s", [id])

    rows = cur.fetchall();
    return rows[0]

# show users who is newly added after 2018-07-12
def show_users_newly_added(mysql):
    date_format_time = "%Y-%m-%d %H:%M:%S"
    date_format_sql = "%Y-%m-%d %H:%i:%s"
    current_datetime = strftime(date_format_time, localtime())

    cur = mysql.connection.cursor()
    cur.execute("SELECT t2.user_id, t2.user_firstname, t1.r_time from (select user_id, min(r_time) as r_time from scores group by user_id) t1 \
        join users t2 on t2.user_id = t1.user_id order by t1.r_time ")

    rows = cur.fetchall();
    return [row[:2] for row in rows if (datetime.strptime(row[2], date_format_time) - datetime.strptime("2018-07-15 00:00:00", date_format_time)).days > 0]
    

# show users who are inactive for the last 24hr
def show_inactive_user(mysql):
    date_format_time = "%Y-%m-%d %H:%M:%S"
    date_format_sql = "%Y-%m-%d %H:%i:%s"
    current_datetime = strftime(date_format_time, localtime())

    cur = mysql.connection.cursor()
    cur.execute("SELECT t2.user_id, t2.user_firstname, t1.r_time from (select user_id, max(r_time) as r_time from scores group by user_id) t1 \
        join user t2 on t2.user_id = t1.user_id order by t1.r_time ")

    rows = cur.fetchall();
    return [row[:2] for row in rows if (datetime.strptime(current_datetime, date_format_time) - datetime.strptime(row[2], date_format_time)).days]



########## FLASHCARD ##########
# insert flashcard user info
def insert_user_flashcard(mysql,user_id,user_firstname,user_lastname):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO user (user_id,user_firstname,user_lastname) VALUES (%s, %s, %s)",(user_id,user_firstname,user_lastname))
            con.commit()
            pretty_print("Flashcard User record successfully added", mode="FC Database")
        except:
            con.rollback()
            pretty_print("Error in inserting Flashcard user reocrd operation", mode="FC BUG!")

# insert flashcard user action
def insert_user_action_flashcard(mysql, user_id, qid, user_action):
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO action (user_id, qid, event, r_time) VALUES (%s, %s, %s, %s)",(user_id, qid, user_action, time))
            con.commit()
            pretty_print("FLASHCARD User action record successfully added", mode="FC Database")
        except:
            con.rollback()
            pretty_print("Error in inserting FLASHCARD user action reocrd operation", mode="FC BUG!")
