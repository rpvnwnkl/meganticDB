# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0022_auto_20160402_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campdetail',
            name='camp',
        ),
        migrations.AddField(
            model_name='campdetail',
            name='camp',
            field=models.ForeignKey(to='bookings.Camp', default=None),
        ),
        migrations.RemoveField(
            model_name='guidedetail',
            name='guide',
        ),
        migrations.AddField(
            model_name='guidedetail',
            name='guide',
            field=models.ForeignKey(to='bookings.Guide', default=None),
        ),
    ]
