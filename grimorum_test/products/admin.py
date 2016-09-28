# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group

from django.contrib import admin
from .models import Product,Order,OrderSale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description','get_price','stock','image_tag',)
    search_fields = ('description', 'name',)

    def image_tag(self, obj):
        return u'<img src="%s" width="150" />' % obj.image.url
    image_tag.short_description = 'Imagen'
    image_tag.allow_tags = True

    def get_price(self, obj):
        return '$ %.2f' % obj.price
    get_price.short_description = 'Precio'
    get_price.allow_tags = True


@admin.register(OrderSale)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_products', 'created', 'get_total',)
    search_fields = ('user__first_name', 'user__last_name', 'user__username',
                     'products__name', 'created')

    def get_total(self, obj):
        return '$ %.2f' % obj.total

    get_total.short_description = 'Total'
    get_total.order_field = 'total'

    def get_products(self, obj):
        html = '<ul>'
        for order in obj.order_set.all():
            html += '<li>'
            html += order.product.name + '({0})'.format(order.quantity)
            html += '</li>'
        html += '</ul>'
        return html

    get_products.allow_tags = True
    get_products.short_description = 'Productos'

    def get_user(self, obj):
        return obj.order.user
    get_user.short_description = 'Usuarios'
    get_user.allow_tags =True


admin.site.site_title = 'Administración Ventas'
admin.site.site_header = 'Administración Ventas'
admin.site.unregister(Group)
admin.site.unregister(Token)




