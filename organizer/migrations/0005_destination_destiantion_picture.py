# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-31 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0004_trip_shared'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='destiantion_picture',
            field=models.FileField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]