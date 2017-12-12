# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0004_auto_20171206_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge.Article')),
            ],
            options={
                'db_table': 'ArticleStatistic',
            },
        ),
    ]