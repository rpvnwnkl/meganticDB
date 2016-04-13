# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 19:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entities', '0001_initial'),
        ('sessions', '0001_initial'),
        ('taggit', '0002_auto_20150616_2121'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival', models.DateField(blank=True, null=True, verbose_name='From')),
                ('departure', models.DateField(blank=True, null=True, verbose_name='Until')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('edited_date', models.DateTimeField(auto_now=True, verbose_name='Edited Date')),
                ('booking_id', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Booking ID')),
                ('notes', models.TextField(blank=True, max_length=1024, verbose_name='Notes')),
                ('camp_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CampRequest', to='entities.Camp', verbose_name='Camp request')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='entities.Member', verbose_name='Member')),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.Session', verbose_name='Session')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='BookingError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=1000, verbose_name='Message')),
                ('details', models.TextField(blank=True, max_length=4000, verbose_name='Details')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Booking', verbose_name='Booking')),
            ],
        ),
        migrations.CreateModel(
            name='BookingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('persons', models.PositiveIntegerField(blank=True, null=True, verbose_name='Persons')),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=36, null=True, verbose_name='Subtotal')),
                ('object_id', models.PositiveIntegerField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Booking', verbose_name='Booking')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-booking__creation_date'],
            },
        ),
        migrations.CreateModel(
            name='ExtraPersonInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forename', models.CharField(max_length=20, verbose_name='First name')),
                ('surname', models.CharField(max_length=20, verbose_name='Last name')),
                ('arrival', models.DateTimeField(blank=True, null=True, verbose_name='Arrival')),
                ('message', models.TextField(blank=True, max_length=1024, verbose_name='Message')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Booking', verbose_name='Booking')),
            ],
            options={
                'ordering': ['-booking__creation_date'],
            },
        ),
    ]