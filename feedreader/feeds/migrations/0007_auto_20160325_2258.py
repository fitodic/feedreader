# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0006_auto_20160325_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(blank=True, default='Unspecified', max_length=200, unique=True),
        ),
    ]
