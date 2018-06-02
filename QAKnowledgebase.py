'''QA Knowledgebase for safety, gre, and science questions'''

import json
from utils import pretty_print

class QAKnowlegeBase():

    def __init__(self, jsonFile):
        pretty_print("Begin to Construct QA Knowledgebase", mode="QA KB")
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
            # group all science subjects together
            if entry["subject"] in ("physics, chemistry, geology, biology"):
                self.SubKB.append("science")
            else:
                self.SubKB.append(entry["subject"])

        self.appendSubDict()

        pretty_print("Total Number of Questions: " +str(self.KBlength))
        pretty_print("Finished QA Knowledgebase Construction", mode="QA KB")

    def appendSubDict(self):
        for i, subject in enumerate(self.SubKB):
            if subject in self.SubDict.keys():
                self.SubDict[subject].append(i)  # append index in list, not qid
            else:
                self.SubDict[subject] = [i]

        pretty_print("Total Subject Count is: "+str(len(self.SubDict)))
        for subject in self.SubDict.keys():
            pretty_print("{}: {}".format(subject, len(self.SubDict[subject])))
