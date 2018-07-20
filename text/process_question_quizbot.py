'''
    process_question_quizbot.py
    Author: Liwei Jiang
    Date: 18/06/2018
    Usage: Remove the HTML syntax in GRE question for the quizbot messenger app.
'''

import json
import random
import re
import codecs
from bs4 import BeautifulSoup



file = codecs.open("jokes.html", 'r')
print file.read()


