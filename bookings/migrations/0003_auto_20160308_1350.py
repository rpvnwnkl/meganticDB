# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-08 18:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_auto_20160308_1341'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Booking',
            new_name='Reservation',
        ),
    ]
