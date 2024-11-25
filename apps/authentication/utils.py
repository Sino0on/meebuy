import requests
import uuid
import random

from django.conf import settings

from xml.etree import ElementTree as ET
from decouple import config

from django.core.mail import EmailMessage


def send_sms_code(email, link):
    try:
        message = EmailMessage(
            to=[email],
            subject='',
            body=f'Ваша ссылка для сброса пароля {link}.\nНикому не говорите ваш код',
            from_email='noreply@zherdesh.ru'
        )

        message.send()
    except:
        return False
    return True


def generate_confirmation_code():
    confirmation_code = ''.join(random.choices('0123456789', k=4))
    print(confirmation_code)
    return confirmation_code


def send_sms(phone_number, confirmation_code):
    login = config('login_nikita')
    password = config('password_nikita')
    transaction_id = str(uuid.uuid4())
    sender = config('sender_nikita')
    message_send = f"Ваш код подтверждения: {confirmation_code}"

    request_body = ET.Element("message")
    ET.SubElement(request_body, "login").text = login
    ET.SubElement(request_body, "pwd").text = password
    ET.SubElement(request_body, "id").text = transaction_id
    ET.SubElement(request_body, "sender").text = sender
    ET.SubElement(request_body, "text").text = message_send
    phones_element = ET.SubElement(request_body, "phones")
    ET.SubElement(phones_element, "phone").text = phone_number

    print(f"Request Body: {ET.tostring(request_body, encoding='UTF-8', method='xml')}")

    url = 'https://smspro.nikita.kg/api/message'
    headers = {'Content-Type': 'application/xml'}

    response = requests.post(url, data=ET.tostring(request_body, encoding="UTF-8", method="xml"), headers=headers)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")

    if response.status_code == 200:
        print('SMS sent successfully')
    else:
        print('Failed to send SMS')
