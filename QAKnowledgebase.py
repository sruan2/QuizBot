'''QA Knowledgebase for safety, gre, and science questions'''

import os
import json

class QAKnowlegeBase():

    def __init__(self, jsonFile):
        print("[QUIZBOT] PID " + str(os.getpid())+": Begin to Construct QA Knowledgebase")
        data = json.load(open(jsonFile))

        self.QID = [] # questin id
        self.QKB = [] # question
        self.SKB = [] # support
        self.AKB = [] # correct answer (NOTE THIS IS A LIST!)
        self.DKB = [] # distractors
        self.SubKB = [] # subject
        self.SubDict = {} # subject dict
        self.KBlength = len(data)

        for entry in data:
            self.QID.append(entry['id'])
            self.QKB.append(entry["question"])
            self.AKB.append(entry["correct_answer"])
            self.SKB.append(entry["support"])
            self.DKB.append(entry["distractor"])
            self.SubKB.append(entry["subject"])

        self.appendSubDict()

        print("\t\t\t\tTotal Number of Questions: " +str(self.KBlength))
        print("[QUIZBOT] PID " + str(os.getpid())+": Finished QA Knowledgebase Construction")

    def appendSubDict(self):
        for i, subject in enumerate(self.SubKB):
            if subject in self.SubDict.keys():
                self.SubDict[subject].append(i)  # append index in list, not qid
            else:
                self.SubDict[subject] = [i]
        print("\t\t\t\tTotal Subject Count is: "+str(len(self.SubDict)))
