import os

class QATransform():

    def __init__(self, QuestionFile, SupportFile, CorrectAnswerFile, SubjectFile):
        print("\n" + str(os.getpid()) + "Begin to construct QA knowledgebase\n")
        self.QKB = [] # question
        self.SKB = [] # support
        self.AKB = [] # answer
        self.SubKB = {} # subject dict
        self.KBlength = 0
        
        self.appendQuestionKB(QuestionFile)
        self.appendSupportKB(SupportFile)
        self.appendCorrectAnswerKB(CorrectAnswerFile)
        self.appendSubjectKB(SubjectFile)

        assert(len(self.QKB) == len(self.SKB))
        assert(len(self.QKB) == len(self.AKB))
        
        print("\n" + str(os.getpid()) + "Finished QA knowledgebase Construction\n")
    
    def appendQuestionKB(self, QuestionFile):
        with open(QuestionFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+QuestionFile)
            for line in f:
                self.QKB.append(line)
        print("="*87+"\n"+"Question KB is appended. Length is: "+str(len(self.QKB)))
        self.KBlength = len(self.QKB)

    def appendSubjectKB(self, SubjectFile):
        with open(SubjectFile, 'r') as f:
            i = 0
            for line in f:
                if line.rstrip() in self.SubKB.keys():
                    self.SubKB[line.rstrip()].append(i)
                else:
                    self.SubKB[line.rstrip()] = [i]
                i += 1
        assert(i == self.KBlength)
        print("="*87+"\n"+"Subject KB is appended. Total Subject Count is: "+str(len(self.SubKB)))
        print("="*87+"\n"+"Subject KB is appended. Length is: "+str(i))


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


    # def LoadQuery(self):
    #     query = raw_input("="*87+"\n"+"Enter a query: ")
    #     print("="*87+"\n"+"Your query is: "+query)
    #     self.QKB = [query] + self.QKB # concat
    #     self.query = query
    #     return query 
    
    # def Featurize(self, query):
    #     self.QKB = [query] + self.QKB # concat
    #     self.tfidf_features = TfidfVectorizer().fit_transform(self.QKB)
    #     cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
    #     related_docs_indices = cosine_similarities.argsort()[:-10:-1]
    #     index = related_docs_indices[1]
        
    #     print("Here is the answer!\n")
    #     return self.AKB[int(index)-1]