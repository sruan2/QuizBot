import pandas as pd

# glove = pd.read_csv('/home/ubuntu/QuizBot/sentence_similarity/glove/glove.6B.300d.txt', sep=" ", quoting=3, header=None, index_col=0)
# glove2 = {key: val.values for key, val in glove.T.items()}

# import pickle
# with open('/home/ubuntu/QuizBot/sentence_similarity/glove/glove.6B/glove.6B.300d.pkl', 'wb') as output:
#     pickle.dump(glove2, output)
# output.close()


glove = pd.read_csv('/home/ubuntu/QuizBot/sentence_similarity/glove/glove.6B.100d.txt', sep=" ", quoting=3, header=None, index_col=0)
glove2 = {key: val.values for key, val in glove.T.items()}

import _pickle as cpickle
with open('/home/ubuntu/QuizBot/sentence_similarity/glove/glove.6B/glove.6B.100d.pkl', 'wb') as output:
    cPickle.dump(glove2, output)
output.close()


# glove = pd.read_csv('/home/ubuntu/QuizBot/sentence_similarity/glove/glove.6B.200d.txt', sep=" ", quoting=3, header=None, index_col=0)
# glove2 = {key: val.values for key, val in glove.T.items()}

# import pickle
# with open('/home/ubuntu/QuizBot/sentence_similarity/glove/glove.6B/glove.6B.200d.pkl', 'wb') as output:
#     pickle.dump(glove2, output)
# output.close()


# glove = pd.read_csv('/home/ubuntu/QuizBot/sentence_similarity/glove/glove.6B.50d.txt', sep=" ", quoting=3, header=None, index_col=0)
# glove2 = {key: val.values for key, val in glove.T.items()}

# import pickle
# with open('/home/ubuntu/QuizBot/sentence_similarity/glove/glove.6B/glove.6B.50d.pkl', 'wb') as output:
#     pickle.dump(glove2, output)
# output.close()