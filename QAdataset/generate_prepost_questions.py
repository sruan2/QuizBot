import json
import random

for data_set in ['sci_data', 'safety_data', 'gre_data']:

    with open(data_set + '_filtered_50.json') as data_file:
        data = json.load(data_file)

    random.shuffle(data)
    pre_data = data[:20]
    post_data = data[10:30]

    for i in range(10):
        post_data[i]['v'] = 'old'
    for i in range(10, 20):
        post_data[i]['v'] = 'new'

    with open(data_set + '_pre_20.json', 'w') as out_file:
        json.dump(pre_data, out_file)

    with open(data_set + '_post_20.json', 'w') as out_file:
        json.dump(post_data, out_file)
