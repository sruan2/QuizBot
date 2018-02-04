from flask import request


# insert user info
def insert_user(mysql, user_id,user_firstname,user_lastname,user_gender,user_status):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()    
            print ()       
            cur.execute("INSERT INTO users (user_id,user_firstname,user_lastname,user_gender,user_status) VALUES (%s, %s, %s, %s, %s)",(user_id,user_firstname,user_lastname,user_gender,user_status))           
            con.commit()  
            print ("User record successfully added")
        except:
            con.rollback()
            print ("error in inserting user reocrd operation")
        # finally:
        #     con.close()  


# update user question-answer loop status
def update_status(mysql, user_id, status):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()             
            cur.execute("update users set user_status = %s where user_id = %s",(status, user_id))           
            con.commit()
            print ("update status successfully added")
        except:
            con.rollback()
            print ("error in updating user status operation")
        # finally:
        #     con.close()      

def show_status(mysql, user_id):
    cur = mysql.connection.cursor() 
    cur.execute("select user_status from users where user_id = %s", [user_id])

    rows = cur.fetchall()
    if len(rows) != 0:
        return rows[0][0] 
    else:
        return -1

# insert user score
def insert_score(mysql, user_id,qid,answer,score,time):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()              
            cur.execute("INSERT INTO scores (user_id,qid,answer,score,r_time) VALUES (%s, %s, %s, %s, %s)", (user_id,qid,answer,score,time))           
            con.commit()
            print ("Score record successfully added")
        except:
            con.rollback()
            print ("error in inserting score operation")
        # finally:
        #     con.close()

# insert asked questions
def insert_question(mysql, user_id,qid,subject,time):
    if request.method == 'POST':
        try:
            con = mysql.connection
            cur = con.cursor()            
            cur.execute("INSERT INTO questions (user_id,qid,subject,r_time) VALUES (%s,%s,%s,%s)",(user_id,qid,subject,time))           
            con.commit()
            print ("Questions record successfully added")
        except:
            con.rollback()
            print ("error in inserting question operation")
        # finally:
        #     con.close()

def show_user_id_list(mysql):
    cur = mysql.connection.cursor() 
    cur.execute("select user_id from users")

    rows = cur.fetchall()
    return [x[0] for x in rows]   


# retrieve score based on user_id 
def show_score(mysql, user_id):
    cur = mysql.connection.cursor() 
    cur.execute("select sum(score) from scores group by user_id having user_id = %s", [user_id])

    rows = cur.fetchall();
    return rows[0][0] if len(rows) > 0 else 0

# retrieve score based on user_id 
def show_last_qid_subject(mysql, user_id):
    cur = mysql.connection.cursor() 
    cur.execute("select qid,subject from questions where user_id = %s order by id desc limit 1", [user_id])

    rows = cur.fetchall();
    return (rows[0][0] if len(rows) > 0 else -1, rows[0][1] if len(rows) > 0 else 'no record')

# show top 10 in leaderboard
def show_top_10(mysql):
    cur = mysql.connection.cursor() 
    cur.execute("select t2.user_firstname,t2.user_lastname,t1.sc from \
        (select user_id, sum(score) as sc from scores group by user_id order by sc desc limit 10) t1 join users t2 on t2.user_id = t1.user_id \
         order by t1.sc desc")

    rows = cur.fetchall();
    return rows