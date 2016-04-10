# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-02 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0025_auto_20160402_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='campdetail',
            name='reservation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookings.Reservation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guidedetail',
            name='reservation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookings.Reservation'),
            preserve_default=False,
        ),
    ]