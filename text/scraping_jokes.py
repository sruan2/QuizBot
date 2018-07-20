'''
    scraping_jokes.py
    Author: Liwei Jiang
    Date: 20/07/2018
    Usage: Scraping jokes from https://www.rd.com/jokes/
'''

import codecs
from bs4 import BeautifulSoup
import re
import json
import string

file = codecs.open("jokes.html", 'r')
soup = BeautifulSoup(file, "html.parser")
paragraphs = soup.find_all('p')

jokes = []

cleanr_1 = re.compile('</p>')
cleanr_2 = re.compile('<p>')

for p in paragraphs:
	j = str(p)
	j = re.sub(cleanr_1, '', j)
	j = re.sub(cleanr_2, '', j)

	if "[…]" in j:
		pass
	elif "\u2028" in j:
		pass
	elif "\n" in j:
		pass
	elif "\xa0" in j:
		pass
	else:
		jokes.append(j)

with open('jokes.json', 'w') as outfile:
	json.dump(jokes, outfile, sort_keys=True, indent=4)