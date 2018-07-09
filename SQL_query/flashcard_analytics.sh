#!/bin/bash

echo First Name: "$1"
echo Last Name: "$2"
echo Output File: flashcard_$1_$2.csv

mysql -u root -p -e "select  concat('\",'a.user_id), c.user_firstname, c.user_lastname, a.qid, a.event, concat(r_time,'\"') as action_time from action a, (select user_firstname, user_lastname, user_id from users where user_firstname = '$1' and user_lastname = '$2') c  where a.user_id = c.user_id order by a.r_time desc" FLASHCARD | sed 's/[\t]/","/g' > flashcard_$1_$2.csv


