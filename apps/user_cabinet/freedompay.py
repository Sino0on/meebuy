import xml.etree.ElementTree as ET

import requests
from django.conf import settings


def send_get_request(endpoint, params):
    url = settings.PAYBOX_URL + endpoint
    response = requests.get(url, params=params)
    return response.json()


def send_post_request(endpoint, data):
    url = settings.PAYBOX_URL + endpoint
    response = requests.post(url, data=data)
    print("Response Text:", response.text)
    try:
        return response.json()
    except ValueError:
        try:
            root = ET.fromstring(response.text)
            response_dict = {child.tag: child.text for child in root}
            return response_dict
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return {"error": "Invalid XML response", "response_text": response.text}
