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

            return min(prices)

        return product.price
    except Exception as e:
        return str(e)
