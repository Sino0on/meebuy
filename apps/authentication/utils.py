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
