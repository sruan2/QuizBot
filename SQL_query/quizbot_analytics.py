import datetime
import MySQLdb
import os
import sys
import csv

cux = MySQLdb.connect(db=os.environ["DB"], user=os.environ["DB_USER"], passwd=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"])
cur = cux.cursor()

cur.execute("SELECT user_id, user_firstname, user_lastname, uid, sender, recipient, type, dialogue, time_stamp \
  		  FROM (user RIGHT JOIN conversation ON user.user_id = conversation.sender OR user.user_id = conversation.recipient) \
          WHERE user_firstname = %s AND user_lastname = %s;", [sys.argv[1], sys.argv[2]])

rows = list(cur.fetchall())
title = ("user_id", "user_firstname", "user_lastname", "uid", "sender", "recipient", "type", "dialogue", "time_stamp")
rows.insert(0, title)

with open("quizbot_conversation_" + sys.argv[1] + "_" + sys.argv[2] + ".csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)


cur.execute("SELECT user.user_id, user_firstname, user_lastname, qid, subject, score, type, begin_uid, end_uid \
  		  FROM (user RIGHT JOIN user_history ON user.user_id = user_history.user_id) \
          WHERE user_firstname = %s AND user_lastname = %s;", [sys.argv[1], sys.argv[2]])

rows = list(cur.fetchall())
title = ("user_id", "user_firstname", "user_lastname", "qid", "subject", "score", "type", "begin_uid", "end_uid")
rows.insert(0, title)

with open("quizbot_user_history_" + sys.argv[1] + "_" + sys.argv[2] + ".csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

cur.close()
cux.close()