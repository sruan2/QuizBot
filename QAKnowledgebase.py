import os
import json

class ConstructQA():

    def __init__(self, jsonFile):
        print("[QUIZBOT] PID " + str(os.getpid())+": Begin to Construct QA Knowledgebase")
        data = json.load(open(jsonFile))

        self.QKB = [] # question
        self.SKB = [] # support
        self.AKB = [] # correct answer (NOTE THIS IS A LIST!)
        self.DKB = [] # distractor 1
        self.SubKB = [] # subject
        self.DifficultyKB = [] # difficulty level
        self.SubDict = {} # subject dict
        self.KBlength = len(data)
        
        for entry in data:
            self.QKB.append(entry["question"])
            self.AKB.append(entry["correct_answer"])
            self.SKB.append(entry["support"])
            self.DKB.append(entry["distractor"])
            self.SubKB.append(entry["subject"])
            self.DifficultyKB.append(entry["difficulty"])
        self.appendSubDict()
        
        print("[QUIZBOT] PID " + str(os.getpid())+": Finished QA Knowledgebase Construction")
        print("[QUIZBOT] PID " + str(os.getpid())+": Total Number of Questions: " +str(self.KBlength))
    
    def appendSubDict(self):       
        for i, subject in enumerate(self.SubKB):
            if subject in self.SubDict.keys():
                self.SubDict[subject].append(i)
            else:
                self.SubDict[subject] = [i]
        print("[QUIZBOT] PID " + str(os.getpid())+": Finished Subject Dictionary Construction")
        print("[QUIZBOT] PID " + str(os.getpid())+": Total Subject Count is: "+str(len(self.SubDict)))
