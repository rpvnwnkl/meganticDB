from django.db import models
from django.contrib import admin
from django.db.models import Q
from django.core import serializers

import json
from datetime import date, timedelta

# Create your models here.

 
class PersonManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)
    #def full_name(self):
     #   return self.first_name + ' ' + self.last_name

class Person(models.Model):
    objects = PersonManager()

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    
    def natural_key(self):
        return (self.first_name, self.last_name)

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def initial_name(self):
        return self.first_name[0] + '. ' + self.last_name
    
    
    class Meta:
        abstract = True
        unique_together = (('first_name', 'last_name'),)

class Member(Person):
    def __str__(self):
        return self.full_name()

class Guide(Person):

    def __str__(self):
        return self.initial_name()

class Camp(models.Model):

    camp_name = models.CharField(max_length=32)

    def __str__(self):
        return self.camp_name


### Reservation Model ###

class ReservationManager(models.Manager):
    def month_archive(self, year, month):
        in_month = self.filter(Q(arrival__year=year), Q(arrival__month=month) | Q(departure__month=month))
        return in_month
    def day_archive(self, year, month, day):
        day_to_search = date(year, month, day)
        valid_reservations = self.filter(reservationdetail__day=day_to_search)
        return valid_reservations

class Reservation(models.Model):
    objects = ReservationManager()

    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    party_size = models.IntegerField(default=1, help_text="Number of Guests in Party")
    arrival = models.DateField(default=date.today, help_text="Arrival Date")
    departure = models.DateField(default=date.today, help_text="Arrival Date")
    MEAL_CHOICES = (
            ('B', 'Breakfast'),
            ('L', 'Lunch'),
            ('D', 'Dinner'),
            )
    first_meal = models.CharField('First meal at camp', max_length=1, choices=MEAL_CHOICES, default='LUNCH', help_text="First Meal")
    last_meal = models.CharField('Last meal at camp', max_length=1, choices=MEAL_CHOICES, default='LUNCH', help_text="Last Meal")
    
    def archive_dict(self):
         memberName = self.member.full_name()
         arrivalDate = self.arrival
         departureDate = self.departure
         context = {
                 'member': memberName,
                 'arrival': arrivalDate,
                 'departure': departureDate,
                 }
         return context
 
    def __str__(self):
        date = self.arrival.strftime('%x')
        return 'Booking #' + str(self.id) + ' - ' + str(self.member) + ' - ' + date

    def save(self, *args, **kwargs):
        if self.id == None:
            super(Reservation, self).save(*args, **kwargs)
            reservation_id = self.id
            days_staying = (self.departure - self.arrival).days
            for each_day in range(days_staying + 1): 
                new_detail = ReservationDetail.objects.create(reservation=self, day=(self.arrival+timedelta(days=each_day)))
    
    class Meta:
        ordering = ['arrival']


class ReservationDetail(models.Model):

    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, unique_for_date='day')
    day = models.DateField()
    camp = models.ManyToManyField('Camp')
    guide = models.ManyToManyField('Guide')

    def __str__(self):
        return self.day.strftime('%x')
        #return '{0} - {1} - {2} - {3}'.format(self.day, self.reservation.member, self.camp, self.guide) 
