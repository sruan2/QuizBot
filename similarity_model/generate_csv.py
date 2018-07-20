import numpy as np

# you are right / you are correct
# you are wrong

file = 'relatedness_scores.csv'

messages = [
		# numbers
		['5', 'five'],
		['4','four'],
		# true/false
		['true', 'yes'],
		['no', 'false'],
		#capitalization
		['Hydrogen', 'hydrogen'],
		['Carbon', 'carbon'],
		# A, B, A and B
		['carbon', 'carbon and hydrogen', 'hydrogen and carbon'],
		# bonds
		['bond', 'covalent bonds'],
		# human activity
		['human activity', 'careless human activity'],
		# heat
		['heat', 'thermal energy'],
		# atom nucleus
		['atom nucleus', 'the nucleus'],
		# nuclear
		['nuclear', 'medulla'],
		# A and B
		['reproduce asexually and sexually', 'reproduce sexually and asexually'],
		# plural
		['2 hour', '2 hours'],
		# synonyms
		['right', 'correct']]

with open(file, 'w') as f:
	for array_index in range(len(messages)):
		similar_words = messages[array_index]
		# add pairs of words in the same list as 5
		for i in range(len(similar_words)):
			for j in range(i+1, len(similar_words)):
				if similar_words[i] != similar_words[j]:
					f.write(str(similar_words[i] + "," + similar_words[j] + "," + '5\n'))
			# write 0 for words not in the same list
			for index_two in range(array_index + 1, len(messages)):
				for word in messages[index_two]:
					f.write(str(similar_words[i] + "," + word + "," + '1\n'))



