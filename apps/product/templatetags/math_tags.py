import traceback
from decimal import Decimal

from django import template
from django.shortcuts import get_object_or_404

from apps.pages.models import FooterColumn
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

        min_price_decimal = Decimal(min_price)
        if min_price_decimal == min_price_decimal.to_integral():
            min_price_str = str(min_price_decimal.quantize(Decimal('1')))
        else:
            min_price_str = str(min_price_decimal).rstrip('0').rstrip('.')

        return min_price_str
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return product.price


@register.simple_tag
def nesting_level(level):
    return '-' * level


@register.simple_tag
def get_footer_columns():
    return FooterColumn.objects.prefetch_related('links').order_by('order')

