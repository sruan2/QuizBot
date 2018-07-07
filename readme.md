# Quiz Bot 
This is an AI-powered educational chatbot for memorizing knowledge. Users can play with it through Facebook Messenger.

## Wiki

https://github.com/sruan2/QuizBot/wiki

## Implementation

### QuizBot
QuizBot app is written in Python 3 and deployed on our AWS server (under the ubuntu account). We use Python Flask to build a webhook for Facebook's Messenger Bot API. It is based on a python template from: https://tutorials.botsfloor.com/creating-your-messenger-bot-4f71af99d26b.

To enter the virutal environment, run `source venv/bin/activate` on the AWS server. To exit the virtual environtment, run `deactivate`

We combined all the commands needed to start the application in a script on our server. So to start the application, log on to aws, enter a screen, and simply run `./start_server.sh`.

Contact Sherry if you need to access the AWS server. Before using the server, you should be familiar with basic [Linux commands](https://practicalunix.org/video-schedule) such as [screen](https://www.tecmint.com/screen-command-examples-to-manage-linux-terminals/) and ssh.

### Flash Card App
Flash card front end is written in html, css, and javascript and is converted to a mobile app using [Cordova](https://cordova.apache.org/). Its source code is in `flashcard/www/`.

The backend is written in Python Flask and hosted on our AWS server. Its source code is in `flashcard_backend/`.

## Try Out Our Apps

### QuizBot
The (stable) version is at https://www.facebook.com/quizzzbot/

The dev version is at https://www.facebook.com/quizzzbotdev/

We have not yet published our app, so the testers need to be added to Facebook Developer Testers. To keep updated with Facebook's latest app policy, check https://www.facebook.com/groups/messengerplatform/

### Flash Card app
The flash card app is deployed on Testflight and can be easily installed for iPhone users.


## Dataset
We currently have three types of questions:

Science questions from Allen SciQ: http://data.allenai.org/sciq/

Safety questions from https://www.mysafetysign.com/safety-quiz (data scraping done by Zhengneng)

GRE questions from http://gre.kmf.com/practise (data scraping done by Sherry)

## Features
The chatbot has the following functionalities:

### Question Sequencing
We are experimenting different algorithms (i.e., spaced repetition) to sequence learning materials to maximize the learning outcome.

### Question Asking
The chatbot can ask questions related to a specific topic, and grade the user's answers using a sentence similarity algorithm.

### Topic Selection
This chatbot utilizes [gensim dot2vec](https://radimrehurek.com/gensim/models/doc2vec.html) for question similarity calculation and moving forward more methods will be tested for this feature. Ultimately, we allow user select topic based upon their interest. 

### Leaderboard (currently not in use)
This chatbot has a database setup for user's information storage. Questions which have been asked and the associated performance score will be saved. Leaderboard will show the top 10 users by sorting their total scores descendingly.

### Speech Interaction (currently not in use)
We use Google cloud speech recognition API and ffmpeg to enable the user to send voice clips.

### Question Answering (currently not in use)
The chatbot can answer simple questions asked by users. It is implemented using a retrival model.
