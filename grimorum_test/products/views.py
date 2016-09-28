# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product
from django.views.generic import View
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from users.models import User
from .models import Product, OrderSale, Order

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ProductListView(LoginRequiredMixin,View):
    login_url = '/'
    model = Product
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        ctx['products_json'] = serializers.serialize("json", Product.objects.all())
        return render(request, self.template_name, ctx)

class GetCheckout(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(GetCheckout, self).dispatch(*args, **kwargs)

    login_url = '/'
    template_name = 'pages/checkout.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        ctx['products_json'] = serializers.serialize("json", Product.objects.all())
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        order_cart = request.body.decode('utf-8')
        cart = json.loads(order_cart)
        if request.user.is_authenticated():
            sales = OrderSale(user=request.user)
            sales.save()
            total = 0
            for item in cart:
                 print(item['id'])
                 product = Product.objects.get(pk=item['id'])
                 order = Order.objects.create(
                    product_id=product.pk,
                    sale_id=sales.pk,
                    quantity=item['quantity']
                     )
                 total += product.price*order.quantity
                 product.stock -= order.quantity
                 product.save()
            sales.total = total
            sales.save()
            response = {'msg': 'todo bello', 'status':200 }
        else:
            response = {'msg': 'no se ha logeado el useuario', 'status': 403}
        return JsonResponse(response)
