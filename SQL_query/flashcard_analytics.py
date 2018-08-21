import datetime
import MySQLdb
import os
import sys
import csv

users = [("Golrokh", "Emami"), ("Cynthia", "Torma"), ("Jordan", "Cho"), ("Laura", "Davey"), ("Courtney", "Smith"), \
		 ("Marianne", "Cowherd"), ("Tugce", "Tasci"), ("Edgar", "Rios"), ("Kimberly", "Ha"), ("Sen", "Wu"), ("Max", "Cobb")]

if sys.argv[1] != "" and sys.argv[2] != "":
    users = [(sys.argv[1], sys.argv[2])]

for user in users:
	cux = MySQLdb.connect(db=os.environ["DB"], user=os.environ["DB_USER"], passwd=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"])
	cur = cux.cursor()

	cur.execute("SELECT users.user_id, user_firstname, user_lastname, qid, event, r_time \
	  		  	 FROM (users RIGHT JOIN action ON users.user_id = action.user_id) \
	          	 WHERE user_firstname = %s AND user_lastname = %s;", [user[0], user[1]])

	rows = list(cur.fetchall())
	title = ("user_id", "user_firstname", "user_lastname", "qid", "event", "r_time")
	rows.insert(0, title)

	with open("user_data/flashcard_" + user[0] + "_" + user[1] + ".csv", 'w') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerows(rows)


	cur.close()
	cux.close()