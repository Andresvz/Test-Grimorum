# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-27 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20160927_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='feature',
        ),
        migrations.AddField(
            model_name='product',
            name='feature',
            field=models.CharField(default=1, max_length=256, verbose_name='Caracteristicas'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Feature',
        ),
    ]
