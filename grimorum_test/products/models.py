# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from common.models import TimeStampedModel
from django.db import models
from users.models import User


class Product(models.Model):
    """ Productos  """
    name = models.CharField(
            max_length=256,
            verbose_name="Producto"
            )
    description = models.TextField(
            blank=True,
            null=True,
            verbose_name="Descripción"
            )
    price = models.DecimalField(
            verbose_name="Precio",
            max_digits=1000,
            decimal_places=2
            )
    stock = models.IntegerField(
            verbose_name="En inventario",
            default=0
            )
    feature = models.CharField(
            max_length=256,
            verbose_name="Caracteristicas"
            )
    image = models.ImageField(
            verbose_name="Imagen",
            upload_to ='media')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Productos"
        verbose_name = "Producto"

class OrderSale(TimeStampedModel):
    """ Pedidos  relacion"""

    user = models.ForeignKey(
            User,
            verbose_name="Cliente",
            help_text="Cliente",
            on_delete=models.CASCADE)
    products = models.ManyToManyField(
            Product,
            verbose_name="Producto(s)",
            help_text="Producto(s)",
            through='Order',
            )

    total = models.DecimalField(
            verbose_name="Total",
            max_digits=1000,
            decimal_places=2,
            default=0
            )

    def __str__(self):              # __unicode__ on Python 2
        return "%s-%s" % (self.user, self.total)

    class Meta:
        verbose_name_plural = "Ventas"
        verbose_name = "Venta"

class Order(TimeStampedModel):
    """ Pedidos  """
    product = models.ForeignKey(
            Product,
            verbose_name="Producto",
            help_text="Producto",
            on_delete=models.CASCADE)

    quantity = models.IntegerField(
            verbose_name="Cantidad",
            default=0
            )

    sale = models.ForeignKey(
            OrderSale,
            verbose_name="Venta",
            help_text="Venta",
            on_delete=models.CASCADE)

    def __str__(self):              # __unicode__ on Python 2
        return "%s-%s" % (self.sale.pk, self.product.name)

    class Meta:
        verbose_name_plural = "Pedidos"
        verbose_name = "Pedido"



