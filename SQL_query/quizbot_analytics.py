'''
    quizbot_analytics.py
    Author: Liwei Jiang
    Date: 08/01/2018
    Usage: 
        Request the quizbot conversation and user history record from MySQL database.
'''
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
users = [("Noah Yinuo", "Yao"), ("Dee Dee", "Thao"), ("Zhenqi", "Hu"), ("Jingyi", "Li"), ("Joy", "Yuzuriha"), \
         ("Andrew", "Ying"), ("Henry", "Qin"), ("Nina", "Horowitz"), ("Daniel", "Do"), ("Fangmingyu", "Yang"), \
         ("Francis", "Yan"), ("Olivia", "Yang"), ("Ted", "Shaowang"), ("Helen", "Wang"), ("Julia", "Thompson"), \
         ("De-an", "Huang"), ("Kylie", "Jue"), ("Tyler", "Yep"), ("Giovanni", "Campagna"), ("Jean", "Coquet"), \
         ("Zhouheng", "Zhuang"), ("Yue", "Hui"), ("Clayton", "Ellington"), ("Nathaniel", "Ramos"), ("Paul", "Walter"), \
         ("Flora", "Wang"), ("Christine", "Liu"), ("Selen", "Bozkurt"), ("Maisam", "Pyarali"), ("Nathan", "Dalal"), \
         ("Sorathan", "Chaturapruek"), ("Daniel", "Choe"), ("Owen", "Wang"), ("Richard", "Xu"), ("Yang", "Wang"), \
         ("Hongsheng", "Fang"), ("Mike", "Solorio"), ("Jessica", "De la paz"), ("Nina", "Wei"), ("Janice", "Zang"),\
         ("Grace", "Hong")]
# users.append(("Julia", "Thompson"))

# request a single user's record specified in command line
if sys.argv[1] != "" and sys.argv[2] != "":
    users = [(sys.argv[1], sys.argv[2])]

for user in users:
	# connect to MySQL database with DB the name of the database, DB_USER the user name, DB_PASSWORD the password of the database, DB_HOST the host name
	cux = MySQLdb.connect(db=os.environ["DB"], user=os.environ["DB_USER"], passwd=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"])
	cur = cux.cursor()

	# request the conversation data from database
	cur.execute("SELECT user_id, user_firstname, user_lastname, uid, sender, recipient, type, dialogue, time_stamp \
	  		  FROM (user RIGHT JOIN conversation ON user.user_id = conversation.sender OR user.user_id = conversation.recipient) \
	          WHERE user_firstname = %s AND user_lastname = %s;", [user[0], user[1]])

	rows = list(cur.fetchall())
	title = ("user_id", "user_firstname", "user_lastname", "uid", "sender", "recipient", "type", "dialogue", "time_stamp")
	rows.insert(0, title)
	
	# dump the conversation result into a csv file
	with open("user_data/quizbot_conversation_" + user[0] + "_" + user[1] + ".csv", 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerows(rows)

	# request the user history data from database
	cur.execute("SELECT user.user_id, user_firstname, user_lastname, qid, subject, score, type, begin_uid, end_uid \
	  		  FROM (user RIGHT JOIN user_history ON user.user_id = user_history.user_id) \
	          WHERE user_firstname = %s AND user_lastname = %s;", [user[0], user[1]])

	rows = list(cur.fetchall())
	title = ("user_id", "user_firstname", "user_lastname", "qid", "subject", "score", "type", "begin_uid", "end_uid")
	rows.insert(0, title)

	# dump the user history result into a csv file
	with open("user_data/quizbot_user_history_" + user[0] + "_" + user[1] + ".csv", 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerows(rows)
	    
	# shut down the connect to the database
	cur.close()
	cux.close()
