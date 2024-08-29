from django import template
import os
from urllib.parse import unquote

from apps.pages.models import StaticPage

register = template.Library()


@register.filter
def filename(value):
    # Декодирование URL-кодированной строки
    decoded_value = unquote(value)
    # Извлечение имени файла из пути
    return os.path.basename(decoded_value)


@register.simple_tag
def get_static_pages():
    pages = StaticPage.objects.filter(name__isnull=False)
    return pages



