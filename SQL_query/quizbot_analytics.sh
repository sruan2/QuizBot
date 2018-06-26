#!/bin/bash

echo First Name: "$1"
echo Last Name: "$2"
echo Output File: quizbot_"$1"_"$2".csv

mysql -u root -p -e "select  a.user_id, c.user_firstname, c.user_lastname, a.qid, a.r_time as question_time, b.answer,b.score, b.r_time as answer_time from questions a, scores b, (select user_firstname, user_lastname, user_id from users where user_firstname = '$1' and user_lastname = '$2') c  where a.user_id = b.user_id and a.qid=b.qid and a.user_id = c.user_id and a.r_time <= b.r_time order by a.r_time desc, b.r_time desc limit 50" QUIZBOT | sed 's/[\t]/,/g' > quizbot_$1_$2.csv

