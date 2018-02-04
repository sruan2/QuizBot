import os
import json

class ConstructQA():

    def __init__(self, jsonFile):
        print("[QUIZBOT] "+str(os.getpid()) + ": Begin to Construct QA Knowledgebase\n")
        data = json.load(open('SciQdataset-23/230questions.json'))

        self.QKB = [] # question
        self.SKB = [] # support
        self.AKB = [] # answer
        self.D1KB = [] # distractor 1
        self.D2KB = [] # distractor 2
        self.D3KB = [] # distractor 3
        self.SubKB = [] # subject
        self.DifficultyKB = [] # difficulty level
        self.SubDict = {} # subject dict
        self.KBlength = len(data)
        
        for entry in data:
            self.QKB.append(entry["question"])
            self.AKB.append(entry["correct_answer"])
            self.D1KB.append(entry["distractor1"])
            self.D2KB.append(entry["distractor2"])
            self.D3KB.append(entry["distractor3"])
            self.SubKB.append(entry["subject"])
            self.DifficultyKB.append(entry["difficulty"])
        self.appendSubDict()
        
        print("[QUIZBOT] Finished QA Knowledgebase Construction\n")
        print("[QUIZBOT] Total Number of Questions: " +str(len(self.KBlength))"\n")
    
    def appendSubDict(self):       
        for i, subject in enumerate(self.SubKB):
            if subject in self.SubDict.keys():
                self.SubDict[subject].append(i)
            else:
                self.SubDict[subject] = [i]
        print("[QUIZBOT] Finished Subject Dictionary Construction. Total Subject Count is: "+str(len(self.SubKB)))
