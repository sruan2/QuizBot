'''
    yaml_to_json.py
    Author: Liwei Jiang
    Date: 02/07/2018
    Usage: Convert a yaml file to a json file.
'''

import yaml
import json

def yaml_to_json():
    with open("chatbot_text.yml", 'r') as stream:
        try:
            data = yaml.load(stream)
            with open('chatbot_text.json', 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
        except yaml.YAMLError as exc:
            print(exc)

    with open("template_conversation.yml", 'r') as stream:
        try:
            data = yaml.load(stream)
            with open('template_conversation.json', 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
        except yaml.YAMLError as exc:
            print(exc)

<<<<<<< HEAD

=======
>>>>>>> 457596426367f4bca6379e747d4c558f92b12efd
yaml_to_json()