import json

with open('230_gre_safety.json') as data_file:
    data = json.load(data_file)

print("Loaded 230_gre_safety.json")
print("Number of QAs:", len(data))

sci_data = []
safety_data = []
gre_data = []

sci_file = 'sci_data.json'
safety_file = 'safety_data.json'
gre_file = 'gre_data.json'

for one_qa in data:
    subject = one_qa['subject']
    if subject == 'gre':
        gre_data.append(one_qa)
    elif subject == 'safety':
        safety_data.append(one_qa)
    elif subject == 'physics' or subject == 'chemistry' or subject == 'biology' or subject == 'geology':
        sci_data.append(one_qa)
    else:
        print(subject, "NOT SUPPORTED!")


with open(sci_file, 'w') as f:
    json.dump(sci_data, f)

with open(safety_file, 'w') as f:
    json.dump(safety_data, f)

with open(gre_file, 'w') as f:
    json.dump(gre_data, f)


print("\nGenerated three files:")
print(sci_file, ":", len(sci_data))
print(safety_file, ":", len(safety_data))
print(gre_file, ":", len(gre_data))




    #[u'support', u'question', u'distractor', u'difficulty', u'correct_answer', u'subject']
