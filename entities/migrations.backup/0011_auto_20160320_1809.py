# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-20 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0010_auto_20160320_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationdetail',
            name='camp',
            field=models.ManyToManyField(to='bookings.Camp'),
        ),
        migrations.AlterField(
            model_name='reservationdetail',
            name='guide',
            field=models.ManyToManyField(to='bookings.Guide'),
        ),
    ]