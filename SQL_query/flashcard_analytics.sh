#!/bin/bash

echo First Name: "$1"
echo Last Name: "$2"
echo Output File: flashcard_$1_$2.csv

mysql -u root -p -e "SELECT users.user_id, user_firstname, user_lastname, qid, event, r_time \
 					 FROM (users RIGHT JOIN action ON users.user_id = action.user_id) \
 					 WHERE user_firstname = '$1' AND user_lastname = '$2'" FLASHCARD | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > flashcard_$1_$2.csv

