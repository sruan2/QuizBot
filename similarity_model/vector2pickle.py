import numpy as np

textFile = 'vectors.txt'

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
pickleFile = 'vectors.pkl'

import _pickle as cPickle
with open(pickleFile, 'wb') as output:
    cPickle.dump(paragram, output)
output.close()