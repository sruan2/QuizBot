import re 
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import unicodedata
from sklearn.metrics.pairwise import linear_kernel

class tfidfTransform():
    def __init__(self):
        # self.KB = reader.makeKB('Data/Aristo-Mini-Corpus-Dec2016/Aristo-Mini-Corpus-In-Parts/CurrentWebCorpus-allSources-v1.txt')
        self.QKB = []
        self.SKB = []

    def appendQuestionKB(self, QuestionFile):
        with open(QuestionFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+QuestionFile)
            for line in f:
                self.QKB.append(line)
        print("="*87+"\n"+"Question KB is appended. Length is: "+str(len(self.QKB)))

    def appendSupportKB(self, SupportFile):
        with open(SupportFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+SupportFile)
            for line in f:
                self.SKB.append(line)
        print("="*87+"\n"+"Support KB is appended. Length is: "+str(len(self.SKB)))
    
    def retrieveAnswer(self, query):
        # Load Query
        self.queryKB = [query] + self.QKB # concat
        self.query = query

        # Featurize
        self.tfidf_features = TfidfVectorizer().fit_transform(self.queryKB)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-10:-1]
        print("=======================================================================================")
        print("QUERY:{}".format(self.query)) 
        print("=======================================================================================")
        i = 1
        for index in related_docs_indices[1:]:
            print("Candidate {} - (Index: {}; Similarity: {:5.4f})".format(i, index, cosine_similarities[index]))
            question = self.queryKB[index]
            # if len(question) > 80:
            #     question = question[:80] + '...'
            print(question)
            i += 1
            print("---------------------------------------------------------------------------------------")
        index = raw_input("="*87+"\n"+"Enter an Index: ")
        support = self.SKB[int(index)-1]
        return support # return the answer to the question given


