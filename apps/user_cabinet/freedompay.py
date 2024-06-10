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
    return response.json()
