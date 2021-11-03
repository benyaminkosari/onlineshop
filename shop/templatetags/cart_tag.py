from django import template
from shop.models import Order, Cart,Product
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def cart_total(user):
    order = Order.objects.filter(user=user)

    if order.exists():
        return order[0].orderitems.count()
    else:
        return 0

@register.filter
def get_order_pk(user):
    try:
        order = get_object_or_404(Order,user=user)
        return 'http://127.0.0.1:8000/shop/orders/'+str(order.pk)+'/'
    except:
        return 'http://127.0.0.1:8000/shop/products'

@register.filter
@stringfilter
def lower(value):
    return value.lower()

@register.filter
def ordering_product_by_time(products):
    return products.order_by('-publish_time')
