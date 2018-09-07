'''
    flashcard_analytics.py
    Author: Liwei Jiang
    Date: 08/01/2018
    Usage:
        Request the flashcard user record from MySQL database.
'''
import datetime
import MySQLdb
import os
import sys
import csv

users = [("Golrokh", "Emami"), ("Cynthia", "Torma"), ("Jordan", "Cho"), ("Laura", "Davey"), ("Courtney", "Smith"), \
         ("Marianne", "Cowherd"), ("Tugce", "Tasci"), ("Edgar", "Rios"), ("Kimberly", "Ha"), ("Sen", "Wu"), ("Max", "Cobb"), \
         ("Yinuo", "Yao"), ("Dee Dee", "Thao"), ("Jenn", "Hu"), ("jingyi", "li"), ("Joy", "Yuzuriha"), ("Tyler", "Yep"), \
         ("Andrew", "Ying"), ("Henry", "Qin"), ("Nina", "Horowitz"), ("Daniel", "Do"), ("Claire", "Yang"), \
         ("Francis", "Yan"), ("Olivia", "Yang"), ("Wangjianzhe", "Shao"), ("Helen", "Wang"), ("Kylie", "Jue"),\
         ("De-An", "Huang"), ("Kylie", "Jue"), ("Giovanni", "Campagna"), ("Jean", "Coquet"), ("Philip", "Zhuang"), \
         ("yue", "hui"), ("Clayton", "Ellington"), ("Nathaniel", "Ramos"), ("Paul", "Walter"), ("Flora", "Wang"), \
         ("Christine", "Liu"), ("Maisam", "Pyarali"), ("Nathan", "Dalal"), ("Sorathan", "Chaturapruek"), ("Daniel", "Choe"), \
         ("Owen", "Wang"), ("Richard", "Xu"), ("Yang", "Wang"), ("Hongsheng", "Fang"), ("Michael", "Solorio"), \
         ("Nina", "Wei"), ("Jessica", "de la Paz"), ("Janice", "Zang"), ("Grace", "Hong"), \
         ("Yufeng", "Yin"), ("Jorge", "Nam")]

users.extend([("Jeongeun", "Park"), ("shuo", "han"), ("Harry", "Liu"), ("Yunan", "Xu"), ("Jackie", "Yang"), ("xuebing", "leng"), ("Zhiyuan", "Lin"),
              ("Jerry", "Hong"), ("Kebing", "Li"), ("Yun", "Zhang"), ("Xiaoou", "Wang"), ("Yue", "Lian"), ("Jackie", "Hang"),  
              ("wenjing", "yan"), ("Heidi", "He"), ("Anna", "Yu"), ("Irene", "Lai"), ("Yin", "Li"), 
              ("Qiwen", "Zhang"), ("Ran", "Gong"), ("Tianshi", "Li"),
              ("Yiran", "Shen"), ("Harry", "Liu"), ("Wendy", "Li"), ("Wenming", "Zhang"), ("Miao", "Zhang"), ("Fangjie", "Cao"), ("Meng", "Tang"),
              ("Elaine", "Yin"), ("Ziang","Zhu"), ("Hao", "Chen"), ("Akemi","Wijayabahu"), ("Yifan", "He"),
              ("Mkhanyisi", "Gamedze")])

# request a single user's record specified in command line
if sys.argv[1] != "" and sys.argv[2] != "":
    users = [(sys.argv[1], sys.argv[2])]

for user in users:
	# connect to MySQL database with DB the name of the database, DB_USER the user name, DB_PASSWORD the password of the database, DB_HOST the host name
	cux = MySQLdb.connect(db=os.environ["DB"], user=os.environ["DB_USER"], passwd=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"])
	cur = cux.cursor()

	# request the user data from database
	cur.execute("SELECT users.user_id, user_firstname, user_lastname, qid, event, r_time \
	  		  	 FROM (users RIGHT JOIN action ON users.user_id = action.user_id) \
	          	 WHERE user_firstname = %s AND user_lastname = %s;", [user[0], user[1]])

	rows = list(cur.fetchall())
	title = ("user_id", "user_firstname", "user_lastname", "qid", "event", "r_time")
	rows.insert(0, title)

	# dump the user record result into a csv file
	with open("user_data/flashcard_" + user[0] + "_" + user[1] + ".csv", 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerows(rows)

	# shut down the connect to the database
	cur.close()
	cux.close()
