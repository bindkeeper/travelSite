# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-08 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0003_newtrip_trip_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='sequance_in_trip',
            field=models.IntegerField(null=True),
        ),
    ]
