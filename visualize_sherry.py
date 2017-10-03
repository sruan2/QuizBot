import pickle as pkl 
import re 
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import unicodedata
from sklearn.metrics.pairwise import linear_kernel
from random import randint

class tfidfTransform():
    def __init__(self):
        # self.KB = reader.makeKB('Data/Aristo-Mini-Corpus-Dec2016/Aristo-Mini-Corpus-In-Parts/CurrentWebCorpus-allSources-v1.txt')
        self.QKB = [] # question
        self.SKB = [] # support
        self.AKB = [] # answer
        self.KBlength = 0

    def appendQuestionKB(self, QuestionFile):
        with open(QuestionFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+QuestionFile)
            for line in f:
                self.QKB.append(line)
        print("="*87+"\n"+"Question KB is appended. Length is: "+str(len(self.QKB)))
        self.KBlength = len(self.QKB)

    def appendSupportKB(self, SupportFile):
        with open(SupportFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+SupportFile)
            for line in f:
                self.SKB.append(line)
        print("="*87+"\n"+"Support KB is appended. Length is: "+str(len(self.SKB)))

    def appendCorrectAnswerKB(self, CorrectAnswerFile):
        with open(CorrectAnswerFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+CorrectAnswerFile)
            for line in f:
                self.AKB.append(line)
        print("="*87+"\n"+"Correct Answer KB is appended. Length is: "+str(len(self.AKB)))

    def LoadQuery(self):
        query = raw_input("="*87+"\n"+"Enter a query: ")
        print("="*87+"\n"+"Your query is: "+query)
        self.QKB = [query] + self.QKB # concat
        self.query = query
        return query 
    
    def Featurize(self):
        self.tfidf_features = TfidfVectorizer().fit_transform(self.QKB)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-10:-1]
        print("=======================================================================================")
        print("QUERY:{}".format(self.query)) 
        print("=======================================================================================")
        i = 1
        for index in related_docs_indices[1:]:
            print("Candidate {} - (Index: {}; Similarity: {:5.4f})".format(i, index, cosine_similarities[index]))
            question = self.QKB[index]
            # if len(question) > 80:
            #     question = question[:80] + '...'
            print(question)
            i += 1
            print("---------------------------------------------------------------------------------------")
        index = raw_input("="*87+"\n"+"Enter an Index: ")
        support = self.SKB[int(index)-1]
        print(support)

    def pickRandomQuestion(self):
        print("=======================================================================================")
        random_number = randint(0, self.KBlength)
        picked_question = self.QKB[random_number].rstrip()

        # print(picked_question)
        # user_answer = raw_input("Enter Your Answer:")
        # answer.append(user_answer)
        # print("Standard Answer is: "+picked_answer)

        return picked_question, random_number

    def computeScore(self, user_answer, question_id):
        picked_answer = self.AKB[question_id].rstrip()
        answer = [picked_answer]
        answer.append(user_answer)
        self.tfidf_features = TfidfVectorizer().fit_transform(answer)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        print("Similarity between the standard answer and yours is: " + str(cosine_similarities[1]))
        return picked_answer, cosine_similarities[1]
               
if __name__ == '__main__':
    tfidf = tfidfTransform()
    tfidf.appendQuestionKB('Data/SciQdataset-23/question_file.txt')
    tfidf.appendSupportKB('Data/SciQdataset-23/support_file.txt')
    tfidf.appendCorrectAnswerKB('Data/SciQdataset-23/correct_answer_file.txt')
    while True:
        tfidf.pickRandomQuestion()
        # tfidf.LoadQuery()
        # tfidf.Featurize()


