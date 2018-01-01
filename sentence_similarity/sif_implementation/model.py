import numpy as np


def preprocess(sentences, tokenizer):
    return [tokenizer.tokenize(q.lower()) for q in sentences]

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


