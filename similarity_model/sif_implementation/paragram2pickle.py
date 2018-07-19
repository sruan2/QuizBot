import numpy as np

# textFile = 'C:/Users/Justin Xu/Desktop/paragram_vectors.txt'
# textFile = 'C:/Users/Justin Xu/Desktop/paragram_300_sl999/paragram_300_sl999/paragram_300_sl999.txt~'
textFile = 'C:/Users/Justin Xu/Desktop/SciQ dataset-2 3/vectors.txt'

def getWordmap(textfile):
    wordMap={}
    with open(textfile,'r', encoding = 'utf8', errors = 'ignore') as f:
        for i, line in enumerate(f):
            try:
                line = line.split()
                v = list(map(float,np.array(line[1:])))
                word = line[0]
                wordMap[word] = v
            except:
                # weird or invalid format
                continue
    return wordMap

paragram = getWordmap(textFile)
# pickleFile = 'C:/Users/Justin Xu/Desktop/paragram_vectors_big.pkl'
pickleFile = 'C:/Users/Justin Xu/Desktop/SciQ dataset-2 3/vectors.pkl'

import _pickle as cPickle
with open(pickleFile, 'wb') as output:
    cPickle.dump(paragram, output)
output.close()