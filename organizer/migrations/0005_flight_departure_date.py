# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-14 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0004_auto_20160908_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='departure_date',
            field=models.DateTimeField(null=True),
        ),
    ]