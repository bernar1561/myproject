# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0005_articlestatistic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlestatistic',
            name='views',
            field=models.IntegerField(default=0, verbose_name='просмотры'),
        ),
    ]