source venv/bin/activate
#!/bin/bash

echo Database: "$1"
echo First Name: "$2"
echo Last Name: "$3"


# mysql -u root -p -e "SELECT user_id, user_firstname, user_lastname, uid, sender, recipient, type, dialogue, time_stamp \
#  					 FROM (user RIGHT JOIN conversation ON user.user_id = conversation.sender OR user.user_id = conversation.recipient) \
#  					 WHERE user_firstname = '$1' AND user_lastname = '$2'" $3 | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > quizbot_conversation_$1_$2.csv

# mysql -u root -p -e "SELECT user.user_id, user_firstname, user_lastname, qid, subject, score, type, begin_uid, end_uid \
#  					 FROM (user RIGHT JOIN user_history ON user.user_id = user_history.user_id) \
#  					 WHERE user_firstname = '$1' AND user_lastname = '$2'" $3 | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > quizbot_user_history_$1_$2.csv

export DB_PASSWORD="smartprimer"
export DB_HOST="localhost"
export DB_USER="ubuntu"
export DB="$1"

python quizbot_analytics.py "$2" "$3"