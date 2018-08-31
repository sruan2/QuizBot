'''
File that helps generate the csv file which we train our supervised model on.
Contains a list of lists of words, where the lists of words are related words and all other words are non related

July 2018
'''

import numpy as np

# you are right / you are correct
# you are wrong

file = 'relatedness_scores.csv'

messages = [
    # numbers
    ['5', 'five'],
    ['4', 'four'],
    # true/false
    ['true', 'yes', 'i think this is true',
                    'this is true', 'I think its true'],
    ['no', 'false', 'this is false'],
    # capitalization
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
    # not the same
    ['kinetic energy'],
    ['nervous', 'central nervous system'],
    ['neural'],
    ['sexual reproduction', 'sexual'],
    ['asexual reproduction', 'asexual'],
    # atom nucleus
    ['atom nucleus', 'the nucleus'],
    # nuclear
    ['nuclear', 'medulla'],
    # A and B
    ['reproduce asexually and sexually', 'reproduce sexually and asexually'],
    ['high viscosity', 'high viscousity'],
    # make sure evasiveness and cogency aren't the same for some reason
    ['evasiveness'],
    ['cogency'],
    # genetic variation and alternative variation to
    ['genetic variation'],
    ['alternative variation'],
    # insects and spider
    ['insects', 'insect'],
    ['spider'],
    ['fibrosis'],
    ['elephantiasis'],
    ['Both water and multipurpose dry chemical', 'Both water and multi-purpose dry chemical'],
    ['admires'],
    ['evokes'],
    # plural
    ['2 hour', '2 hours'],
    # synonyms
    ['twist', 'twist your body'],
    ['right', 'correct','you are right', 'you are correct'],
    ['wrong', 'incorrect', 'you are wrong', 'you are incorrect'],
    ['at the fire','at the base of the fire', 'base of fire'],
    ['loved', 'cherished'],
    ['a mathematician found a solution to the problem', 'A problem was solved by a young mathematician']]

with open(file, 'w') as f:
    for array_index in range(len(messages)):
        similar_words = messages[array_index]
        # add pairs of words in the same list as 5
        for i in range(len(similar_words)):
            for j in range(i+1, len(similar_words)):
                if similar_words[i] != similar_words[j]:
                    f.write(
                        str(similar_words[i] + "," + similar_words[j] + "," + '5\n'))
            # write 0 for words not in the same list
            for index_two in range(array_index + 1, len(messages)):
                for word in messages[index_two]:
                    f.write(str(similar_words[i] + "," + word + "," + '1\n'))
