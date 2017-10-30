# Facebook Messenger Bot
This is a chatbot for science question answering and quiz.

It is based on a python template that uses Flask to build a webhook for Facebook's Messenger Bot API.

How to set up the template is at: (https://tutorials.botsfloor.com/creating-your-messenger-bot-4f71af99d26b).

callback URL:https://quizz-bot.herokuapp.com/
verify token:nothing_to_verify

original procfile:
web: gunicorn app:app --log-file=-