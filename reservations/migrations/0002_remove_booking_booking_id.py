# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 19:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='booking_id',
        ),
    ]
