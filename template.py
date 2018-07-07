'''
    template.py
    Author: Liwei Jiang
    Date: 06/07/2018
    Usage: Create json templates of Facebook Messenger elements.
'''
import random
import json
import yaml

def create_typing_action_template_json(recipient_id):
    '''
        This function creates a json template of sending a typing action.
    '''
    template = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": "typing_on"
    })
    return template


def create_image_template_json(recipient_id, image_data):
    '''
        This function creates a json template of sending a image.
    '''
    if image_data["template_type"] == "generic":
        template = json.dumps(
                {"recipient": {
                    "id": recipient_id
                    },
                    "message": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "generic",
                                "elements": [{
                                    "title": image_data["title"],
                                    "subtitle": image_data["subtitle"],
                                    "image_url": image_data["image_url"]
                                }]
                            }
                        }
                    }
                })
    else:
        template = json.dumps(
                {"recipient": {
                    "id": recipient_id
                    },
                    "message": {
                        "attachment": {
                            "type": "image",
                            "payload": {
                                "url": image_data["image_url"]
                            }
                        }
                    }
                })
    return template


def create_message_template_json(recipient_id, template_conversation, message_data, message_text = ""):
    '''
        This function creates a json template of sending a text message.
    '''
    if message_text == "":
        if message_data["source"] != "TEMPLATE":
            message_text = message_data["text"]
        else:
            random.shuffle(template_conversation["TEMPLATE"][message_data["text"]])
            message_text = template_conversation["TEMPLATE"][message_data["text"]][0]
    template = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    return template


def create_quick_reply_template_json(recipient_id, template_conversation, quick_reply_data, message_data = ""):
    '''
        This function creates a json template of sending a set of quick reply buttons along with a text message.
    '''
    if message_data == "":
        if quick_reply_data["message"]["source"] != "TEMPLATE":
            message_text = quick_reply_data["message"]["text"]
        else:
            random.shuffle(template_conversation["TEMPLATE"][quick_reply_data["message"]["text"]])
            message_text = template_conversation["TEMPLATE"][quick_reply_data["message"]["text"]][0]
    else:
        if message_data["source"] != "TEMPLATE":
            message_text = message_data["text"]
        else:
            random.shuffle(template_conversation["TEMPLATE"][message_data["text"]])
            message_text = template_conversation["TEMPLATE"][message_data["text"]][0]

    template = {
                    "recipient": {
                        "id": recipient_id
                    },
                    "message": {
                        "text": message_text,
                        "quick_replies": []
                    }
                }
    num_quick_replies = len(quick_reply_data["title"])

    for i in range(num_quick_replies):
        if quick_reply_data["source"][i] != "TEMPLATE":
            title = quick_reply_data["title"][i]
        else:
            random.shuffle(template_conversation["TEMPLATE"][quick_reply_data["title"][i]])
            title = template_conversation["TEMPLATE"][quick_reply_data["title"][i]][0]
        template["message"]["quick_replies"].append(
            {
                "content_type": "text",
                "title": title,
                "payload": quick_reply_data["payload"][i]
            }
        )
    template = json.dumps(template)
    return template


def create_persistent_menu_json(persistent_menu_data):
    '''
        This function creates a json template of setting up a persistence menu.
    '''
    template = persistent_menu_data
    return template


def create_get_started_json(get_started_data):
    '''
        This function creates a json template of initializing the payloads.
    '''
    template = get_started_data
    return template  
