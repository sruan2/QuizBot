import numpy as np


def preprocess(sentences, tokenizer):
    return [tokenizer.tokenize(q.lower()) for q in sentences]

def cosine_similarity(v1, v2):
    similarity = (np.dot(v1, v2.T) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    return similarity
    #return int(((np.dot(v1, v2.T) / (np.linalg.norm(v1) * np.linalg.norm(v2)))+1)*5) # shape is (0,10)
