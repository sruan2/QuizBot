glove = pd.read_csv('/Users/sherryruan/data/glove/glove.6B/glove.6B.300d.txt', sep=" ", quoting=3, header=None, index_col=0)
glove2 = {key: val.values for key, val in glove.T.items()}

import pickle
with open('/Users/sherryruan/data/glove/glove.6B/glove.6B.300d.pkl', 'wb') as output:
    pickle.dump(glove2, output)