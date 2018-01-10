import os

class QATransform():

    def __init__(self, QuestionFile, SupportFile, CorrectAnswerFile, SubjectFile):
        # self.KB = reader.makeKB('Data/Aristo-Mini-Corpus-Dec2016/Aristo-Mini-Corpus-In-Parts/CurrentWebCorpus-allSources-v1.txt')
        print("\n" + str(os.getpid())+" tfidf initialization begins\n")
        self.QKB = [] # question
        self.SKB = [] # support
        self.AKB = [] # answer
        self.SubKB = {} # subject dict
        self.KBlength = 0
        #self.MODEL = Doc2Vec.load(PreTrainedModel) # load the model in the very beginning
        self.appendQuestionKB(QuestionFile)
        self.appendSupportKB(SupportFile)
        self.appendCorrectAnswerKB(CorrectAnswerFile)
        self.appendSubjectKB(SubjectFile)
        print("\nqa_knowledgebase ends\n")
    
    def appendQuestionKB(self, QuestionFile):
        with open(QuestionFile, 'r') as f:
            print("="*87+"\n"+"File opened: "+QuestionFile)
            for line in f:
                self.QKB.append(line)
        print("="*87+"\n"+"Question KB is appended. Length is: "+str(len(self.QKB)))
        self.KBlength = len(self.QKB)

    def appendSubjectKB(self, SubjectFile):
        with open(SubjectFile, 'r') as f:
            for i in range(len(f)):
                if f[i] in self.SubKB.keys():
                    self.SubKB[f[i]].append(i)
                else:
                    self.SubKB[f[i]] = [i]
        print("="*87+"\n"+"Subject KB is appended. Total Subject Count is: "+str(len(self.SubKB)))

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
    
    def Featurize(self, query):
        self.QKB = [query] + self.QKB # concat
        #self.query = query

        self.tfidf_features = TfidfVectorizer().fit_transform(self.QKB)
        cosine_similarities = linear_kernel(self.tfidf_features[0:1], self.tfidf_features).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-10:-1]
        # print("=======================================================================================")
        # print("QUERY:{}".format(self.query)) 
        # print("=======================================================================================")
        # i = 1
        index = related_docs_indices[1]
        # for index in related_docs_indices[1:]:
        #     print("Candidate {} - (Index: {}; Similarity: {:5.4f})".format(i, index, cosine_similarities[index]))
        #     question = self.QKB[index]
        #     # if len(question) > 80:
        #     #     question = question[:80] + '...'
        #     print(question)
        #     i += 1
        #     print("---------------------------------------------------------------------------------------")
        # index = raw_input("="*87+"\n"+"Enter an Index: ")
        # support = self.SKB[int(index)-1]
        # print(support)
        print("Here is the answer!\n")
        return self.AKB[int(index)-1]