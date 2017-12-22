# Quiz Bot 
This is an educational chatbot for science question asking and answering hosted on Facebook Messenger platform.

## Wiki

https://github.com/smartprimer/QuizBot/wiki

## Hosting
The chatbot is deployed on Heroku and ses Flask to build a webhook for Facebook's Messenger Bot API.
It is based on a python template from: (https://tutorials.botsfloor.com/creating-your-messenger-bot-4f71af99d26b).

## Dataset
We use the science question dataset from Allen SciQ: http://data.allenai.org/sciq/

## Features
The chatbot has the following functionalities:

### Question Asking
The chatbot can ask questions related to a specific topic, and grade the user's answers using a sentence similarity metric.

### Topic Selection
This chatbot utalizes [gensim dot2vec](https://radimrehurek.com/gensim/models/doc2vec.html) for question similarity calculation and moving forward more methods will be tested for this feature. Ultimately, we allow user select topic based upon their interest. 

### Leaderboard
Zhengneng will set up the database to store user's information as well as the associated performance score and the leaderboard will be based on score sorting.

### Question Answering
The chatbot can answer simple questions asked by users. It is implemented using a retrival model.
