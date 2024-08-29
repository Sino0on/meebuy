from django import template
import os
from urllib.parse import unquote

register = template.Library()


@register.filter
def filename(value):
    # Декодирование URL-кодированной строки
    decoded_value = unquote(value)
    # Извлечение имени файла из пути
    return os.path.basename(decoded_value)
