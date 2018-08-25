import datetime
import MySQLdb
import os
import sys
import csv

# use the QUIZBOT database
# users = [("Veronica", "Cruz"), ("Jackie", "Fortin"), ("Eleni", "Aneziris"), ("Zilin", "Ma"), ("Jongho", "Kim"), \
# 		 ("Nina", "Tai"), ("Yi", "Feng"), ("Dae hyun", "Kim"), ("Pingyu", "Wang"), ("Lantao", "Mei"), \
# 		 ("Michael", "Silvernagel"), ("Bianca", "Yu")]

# use the QUIZBOT_DEV database
# within-subject users: use the QUIZBOT_DEV database
users = [("Noah Yinuo", "Yao"), ("Dee Dee", "Thao"), ("Zhenqi", "Hu"), ("Jingyi", "Li"), ("Joy", "Yuzuriha"), \
         ("Andrew", "Ying"), ("Henry", "Qin"), ("Nina", "Horowitz"), ("Daniel", "Do"), ("Fangmingyu", "Yang"), \
         ("Francis", "Yan"), ("Olivia", "Yang"), ("Ted", "Shaowang"), ("Helen", "Wang"), ("Julia", "Thompson"), \
         ("De-an", "Huang"), ("Kylie", "Jue"), ("Tyler", "Yep"), ("Giovanni", "Campagna"), ("Jean", "Coquet"), \
         ("Zhouheng", "Zhuang")]
users.append(("Julia", "Thompson"))


if sys.argv[1] != "" and sys.argv[2] != "":
    users = [(sys.argv[1], sys.argv[2])]

for user in users:

	cux = MySQLdb.connect(db=os.environ["DB"], user=os.environ["DB_USER"], passwd=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"])
	cur = cux.cursor()

	cur.execute("SELECT user_id, user_firstname, user_lastname, uid, sender, recipient, type, dialogue, time_stamp \
	  		  FROM (user RIGHT JOIN conversation ON user.user_id = conversation.sender OR user.user_id = conversation.recipient) \
	          WHERE user_firstname = %s AND user_lastname = %s;", [user[0], user[1]])

	rows = list(cur.fetchall())
	title = ("user_id", "user_firstname", "user_lastname", "uid", "sender", "recipient", "type", "dialogue", "time_stamp")
	rows.insert(0, title)

	with open("user_data/quizbot_conversation_" + user[0] + "_" + user[1] + ".csv", 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerows(rows)


	cur.execute("SELECT user.user_id, user_firstname, user_lastname, qid, subject, score, type, begin_uid, end_uid \
	  		  FROM (user RIGHT JOIN user_history ON user.user_id = user_history.user_id) \
	          WHERE user_firstname = %s AND user_lastname = %s;", [user[0], user[1]])

	rows = list(cur.fetchall())
	title = ("user_id", "user_firstname", "user_lastname", "qid", "subject", "score", "type", "begin_uid", "end_uid")
	rows.insert(0, title)

	with open("user_data/quizbot_user_history_" + user[0] + "_" + user[1] + ".csv", 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerows(rows)

	cur.close()
	cux.close()
