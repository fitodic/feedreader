# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0009_auto_20160325_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='image',
            field=models.ImageField(null=True, upload_to='entry_images/'),
        ),
    ]
