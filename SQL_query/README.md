```bash
# to extract flash card user data. Output file is flashcard_Bryce_Tham.csv
./flashcard_analytics.sh Bryce Tham

# to extract quizbot user data. Ouput file is quizbot_conversation_Bryce_Tham.csv and quizbot_user_history_Bryce_Tham.csv
./quizbot_analytics.sh Bryce Tham QUIZBOT (or QUIZBOT_DEV)

To calculate the app usage time, please go to 'score_calculator/app_user_data'. 

# for the user data analysis of the quizbot app.
python quizbot_user_data.py Firstname Lastname 

# for the user data analysis of the flashcards app.
python flashcard_user_data.py Firstname Lastname 

```



