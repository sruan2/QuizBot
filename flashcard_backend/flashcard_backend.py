import sys
sys.path.append("../")
import os
from flask import Flask
from flask import request
from flask_mysqldb import MySQL
import database



app = Flask(__name__, static_url_path='')

# ================== MySQL Setup ==================
mysql = MySQL()
app.config['MYSQL_HOST'] = os.environ["DB_HOST"]
app.config['MYSQL_USER'] = os.environ["DB_USER"]
app.config['MYSQL_PASSWORD'] = os.environ["DB_PASSWORD"]
app.config['MYSQL_DB'] = os.environ["DB"]
mysql.init_app(app)


@app.route('/')
def index():
    return 'Hello world'

@app.route('/test', methods=['GET'])
def verify():
    print("received")
    return "test", 200

@app.route('/logdata', methods=['POST'])
def webhook():

    print (request)
    data = request.get_json()['data']
    sender_id = data['user_id']
    if not int(sender_id) in database.show_user_id_list(mysql):
        sender_firstname = data['firstname']
        sender_lastname = data['lastname']
        print("[FLASHCARD] PID " + str(os.getpid())+": This is a new user!")
        database.insert_user_flashcard(mysql, sender_id, sender_firstname, sender_lastname)

    insert_user_action_flashcard(mysql, sender_id, qid, user_action)

    return "ok", 200


if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem', '/etc/letsencrypt/live/smartprimer.org/privkey.pem')
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=context)
