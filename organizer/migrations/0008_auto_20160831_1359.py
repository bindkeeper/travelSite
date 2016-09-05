# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-31 10:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0007_trip_trip_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='existing_hotel',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='organizer.Hotel'),
        ),
        migrations.AddField(
            model_name='trip',
            name='existing_hotel_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]