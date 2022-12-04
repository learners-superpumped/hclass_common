import requests
import os
from typing import Dict

MESSAGE_SERVER_TOKEN = os.environ.get("MESSAGE_SERVER_TOKEN")
MESSAGE_SERVER_ENDPOINT = 'https://log.superdots.xyz'
MESSAGE_SERVER_HEADERS = {
  'Content-Type': 'application/json',
  'Authorization': f"Bearer {MESSAGE_SERVER_TOKEN}",
}


def get_message_server_template(template_type: str) -> Dict:
    response = requests.get(f"{MESSAGE_SERVER_ENDPOINT}/templates", params={
        'service': 'h_class',
        'templateType': template_type
    }, headers=MESSAGE_SERVER_HEADERS)
    return response.json()


def send_message(message_dict: Dict, is_test: bool = True) -> Dict:
    if is_test:
        return message_dict
    response = requests.get(f"{MESSAGE_SERVER_ENDPOINT}/messages", json=message_dict, headers=MESSAGE_SERVER_HEADERS)
    return response.json()