from decimal import Decimal

from django import template
from django.shortcuts import get_object_or_404

from apps.product.models import Product, PriceColumn

register = template.Library()


@register.simple_tag
def calculate(obj_id):
    try:
        prices = []
        product = get_object_or_404(Product, id=obj_id)

        formulas = PriceColumn.objects.filter(provider=product.provider)
        if formulas:
            for formula in formulas:
                prices.append(formula.apply_formula(product.price))

            min_price = min(prices)
        else:
            min_price = product.price

        min_price = Decimal(min_price).normalize()

        min_price_str = format(min_price, 'f').rstrip('0').rstrip('.')

        return min_price_str
    except Exception as e:
        return str(e)
