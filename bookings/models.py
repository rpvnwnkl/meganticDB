from django.db import models
from django.contrib import admin
from django.db.models import Q
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import json, logging
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
    def get_absolute_url(self):
        return reverse('member_detail', kwargs={'pk': self.pk})

class Guide(Person):

    def __str__(self):
        return self.initial_name()
    def get_absolute_url(self):
        return reverse('guide_detail', kwargs={'pk': self.pk})

class Camp(models.Model):

    camp_name = models.CharField(max_length=32)
    sleeps = models.PositiveSmallIntegerField(default=1, help_text="Sleeps how many")

    def __str__(self):
        return self.camp_name
    def get_absolute_url(self):
        return reverse('camp_detail', kwargs={'pk': self.pk})


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
    party_size = models.PositiveSmallIntegerField(default=1, help_text="Number of Guests in Party")
    arrival = models.DateField(default=date.today, help_text="Arrival Date")
    departure = models.DateField(default=date.today, help_text="Arrival Date")
    MEAL_CHOICES = (
            ('B', 'Breakfast'),
            ('L', 'Lunch'),
            ('D', 'Dinner'),
            )
    
    first_meal = models.CharField('First meal at camp', max_length=1, choices=MEAL_CHOICES, default='LUNCH', help_text="First Meal")
    
    last_meal = models.CharField('Last meal at camp', max_length=1, choices=MEAL_CHOICES, default='LUNCH', help_text="Last Meal")
    
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    
    
    # METHODS 
    def __str__(self):
        date = self.arrival.strftime('%x')
        return 'Booking #' + str(self.id) + ' - ' + str(self.member) + ' - ' + date
    # Django method modifier
    def save(self, *args, **kwargs):
        super(Reservation, self).save(*args, **kwargs)
        # this method call adds ReservationDetail objects and removes extra ones in case of date update
        self.add_details()
        return
    
    # custom housekeeping method
    def add_details(self):
        day_list = self.days_there(self.arrival, self.departure)
        for each_day in day_list:
            if not ReservationDetail.objects.filter(day=each_day, reservation=self):
                if each_day == day_list[0]:
                    # this is the first day of stay
                    ReservationDetail.objects.create(
                            reservation=self, 
                            day=each_day, 
                            is_first_day=True)
                elif each_day == day_list[-1]:
                    # this is the last day
                    ReservationDetail.objects.create(
                            reservation=self,
                            day=each_day,
                            is_last_day=True)
                else:
                    # all the other days
                    ReservationDetail.objects.create(
                            reservation=self,
                            day=each_day)
        # in case of updated entry:
        self.remove_extra_details()
        return

    # backup to add details method
    def remove_extra_details(self):
        #this pulls up the reservation details in a queryset and deletes those outside of arrival - departure
        the_details = ReservationDetail.objects.filter(reservation=self).order_by('day')
        deleted_items = the_details.filter(day__lt=self.arrival).delete()
        deleted_items2 = the_details.filter(day__gt=self.departure).delete()
        print(deleted_items, deleted_items2)
        return

    # utility method, used by add details and co
    def days_there(self, arrival, departure):
        # this returns a list of datetime instances corresponding to arrival - departure
        days_staying = (departure - arrival).days
        day_list = [arrival + timedelta(days=each_day) for each_day in range(days_staying + 1)]
        return day_list

    # Django method modifier
    def clean(self):
        print('clean method is starting')
        # this validates whether there are existing res for these dates
        day_list = self.days_there(self.arrival, self.departure)
        for each_day in day_list:
            if ReservationDetail.objects.filter(
                    day=each_day,
                    reservation__member=self.member,
                    ).exclude(reservation__pk=self.pk):
                raise ValidationError(
                        {'member':_('overlapping dates')},
                        code='invalid',
                        )

    # django method modifier
    def get_absolute_url(self):
        return reverse('reservation_detail', kwargs={'pk':self.id})

    class Meta:
        ordering = ['arrival']


class ReservationDetail(models.Model):

    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, unique_for_date='day')
    day = models.DateField()
    camps = models.ManyToManyField('Camp')
    guides = models.ManyToManyField('Guide')
    is_first_day = models.BooleanField(default=False)
    is_last_day = models.BooleanField(default=False)

    def __str__(self):
        return self.day.strftime('%x')

    def save(self, *args, **kwargs):
        if self.id == None:
            super(ReservationDetail, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('resdetail_detail', kwargs={'pk':self.id})

