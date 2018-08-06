```bash
# to extract flash card user data. Output file is flashcard_Bryce_Tham.csv
./flashcard_analytics.sh Bryce Tham

# to extract quizbot user data. Ouput file is quizbot_conversation_Bryce_Tham.csv and quizbot_user_history_Bryce_Tham.csv
./quizbot_analytics.sh Bryce Tham QUIZBOT (or QUIZBOT_DEV)

To calculate the app usage time, please go to 'score_calculator/app_use_time'. 

Run 'python quizbot_time.py Firstname Lastname' for the quizbot app usage time for the specified user.

Run 'python flashcard_time.py Firstname Lastname' for the flashcard app usage time for the specified user.


```
