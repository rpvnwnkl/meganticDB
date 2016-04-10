# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-24 18:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0013_auto_20160322_1536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservationdetail',
            old_name='camps',
            new_name='camp',
        ),
        migrations.RenameField(
            model_name='reservationdetail',
            old_name='guides',
            new_name='guide',
        ),
        migrations.RemoveField(
            model_name='reservationdetail',
            name='is_first_day',
        ),
        migrations.RemoveField(
            model_name='reservationdetail',
            name='is_last_day',
        ),
    ]
