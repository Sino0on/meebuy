import random

from captcha.conf import settings

def only_digit_challenge():
    ret = ''.join([str(random.randint(0, 9)) for _ in range(settings.CAPTCHA_LENGTH)])
    return ret, ret