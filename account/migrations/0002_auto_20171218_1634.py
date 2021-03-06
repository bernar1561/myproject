# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 10:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.IntegerField(blank=True, default=None, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fb_link',
            field=models.URLField(blank=True, default=None, verbose_name='ссылка на facebook'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='inst_link',
            field=models.URLField(blank=True, default=None, verbose_name='ссылка на instagram'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter_link',
            field=models.URLField(blank=True, default=None, verbose_name='ссылка на twitter'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='vk_link',
            field=models.URLField(blank=True, default=None, verbose_name='ссылка на Vk'),
        ),
    ]
