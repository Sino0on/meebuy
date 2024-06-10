import hashlib
import hmac
from django.conf import settings


def generate_signature(data):
    secret_key = settings.PAYBOX_MERCHANT_SECRET
    print("Secret Key:", secret_key)
    sorted_data = sorted(data.items())
    concat_string = '&'.join([f"{k}={v}" for k, v in sorted_data])
    hmac_hash = hmac.new(secret_key.encode(), concat_string.encode(), hashlib.md5).hexdigest()
    return hmac_hash
