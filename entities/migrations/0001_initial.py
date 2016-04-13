# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 19:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camp_name', models.CharField(max_length=32)),
                ('num_beds', models.PositiveSmallIntegerField(default=1, help_text='Number of beds')),
            ],
        ),
        migrations.CreateModel(
            name='CampDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_guests_staying', models.PositiveSmallIntegerField(default=1, help_text='Number of guests staying here')),
                ('num_beds_used', models.PositiveSmallIntegerField(default=1, help_text='Number of beds being used')),
                ('camp', models.ManyToManyField(to='entities.Camp')),
            ],
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email_address', models.EmailField(blank=True, default=None, max_length=256)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GuideDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide', models.ManyToManyField(to='entities.Guide')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email_address', models.EmailField(blank=True, default=None, max_length=256)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival', models.DateField(default=datetime.date.today)),
                ('departure', models.DateField(default=datetime.date.today)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('edited_on', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Member')),
            ],
            options={
                'ordering': ['arrival'],
            },
        ),
        migrations.CreateModel(
            name='ReservationDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_guides', models.PositiveSmallIntegerField(default=0)),
                ('day_reserved', models.DateField()),
                ('is_first_day', models.BooleanField(default=False)),
                ('is_last_day', models.BooleanField(default=False)),
                ('eating_breakfast', models.BooleanField(default=True)),
                ('eating_lunch', models.BooleanField(default=True)),
                ('eating_dinner', models.BooleanField(default=True)),
                ('num_guests', models.PositiveSmallIntegerField(default=1, help_text='Number of guests')),
                ('num_beds_required', models.PositiveSmallIntegerField(default=1, help_text='Number of beds required')),
                ('num_guides_required', models.PositiveSmallIntegerField(default=1, help_text='Number of guides requested')),
                ('camps', models.ManyToManyField(to='entities.Camp', unique_for_date='day_reserved')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Reservation', unique_for_date='day_reserved')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('first_name', 'last_name')]),
        ),
        migrations.AddField(
            model_name='guidedetail',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Reservation'),
        ),
        migrations.AddField(
            model_name='guidedetail',
            name='reservation_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.ReservationDetail'),
        ),
        migrations.AlterUniqueTogether(
            name='guide',
            unique_together=set([('first_name', 'last_name')]),
        ),
        migrations.AddField(
            model_name='campdetail',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Reservation'),
        ),
        migrations.AddField(
            model_name='campdetail',
            name='reservation_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.ReservationDetail'),
        ),
    ]