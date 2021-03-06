from django.db import models
from django.contrib import admin
from django.db.models import Q
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import json, logging
from datetime import date, timedelta
import calendar

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

##############################
### Guide Models #############
##############################

class Guide(Person):

    def __str__(self):
        return self.initial_name()
    def get_absolute_url(self):
        return reverse('guide_detail', kwargs={'pk': self.pk})

class GuideDetail(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    reservation_detail = models.ForeignKey('ReservationDetail', on_delete=models.CASCADE)
    guide = models.ManyToManyField('Guide')
    
    def save(self, *args, **kwargs):
        if self.id == None:
            super(GuideDetail, self).save(*args, **kwargs)

###############################
### Camp model and managers ###
###############################

class CampManager(models.Manager):

    # this function returns a list of dicts with camp names as keys, key values are lists of booleans    
    def get_vacancies(self, year, month):
        camp_list = self.all().order_by('camp_name')
        vacancies = [{'camp_name':camp.camp_name, 'vacancies':[]} for camp in camp_list]
        
        month_to_check = self.month_days(year, month)
        
        for each_day in month_to_check:
            # indexing by place in ordered camp_list
            for camp_number in range(len(camp_list)):
                # getting camp object back from place in list
                camp = camp_list[camp_number]
                # using index to find place in vacancies list, targeting dict key with camp name, and adding to the list of days
                vacancies[camp_number]['vacancies'].append(camp.is_vacant(each_day))

        return (vacancies, month_to_check)
    
    def month_days(self, year, month):
        temp_calendar = calendar.Calendar(firstweekday=6)
        
        month_to_check = temp_calendar.itermonthdates(year=int(year), month=int(month))
        month_to_check = list(month_to_check)
        
        simple_month_to_check = [each_day.day for each_day in month_to_check]
        
        start_day = simple_month_to_check.index(1)
        
        month_to_check = month_to_check[start_day:]
        simple_month_to_check = simple_month_to_check[start_day:]
        
        try:
            stop_day = simple_month_to_check[1:].index(1)
        except ValueError:
            stop_day = len(simple_month_to_check[1:])

        month_to_check = month_to_check[:stop_day+1]
        
        return month_to_check
    

class Camp(models.Model):
    objects = CampManager()

    camp_name = models.CharField(max_length=32)
    num_beds = models.PositiveSmallIntegerField(default=1, help_text="Number of beds")

    def __str__(self):
        return self.camp_name
    def get_absolute_url(self):
        return reverse('camp_detail', kwargs={'pk': self.pk})
    
    #this function returns boolean of whether a res exists for the camp on the given date
    def is_vacant(self, date_to_check):
        return len(ReservationDetail.objects.filter(camps=self.pk, day_reserved=date_to_check)) != 0

class CampDetail(models.Model):
    
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    reservation_detail = models.ForeignKey('ReservationDetail', on_delete=models.CASCADE)
    camp = models.ManyToManyField('Camp')
    num_guests_staying = models.PositiveSmallIntegerField(default=1, help_text="Number of guests staying here")
    num_beds_used = models.PositiveSmallIntegerField(default=1, help_text="Number of beds being used")
    def save(self, *args, **kwargs):
        if self.id == None:
            super(CampDetail, self).save(*args, **kwargs)
    def capacity(self):
        return self.camp.num_beds


#########################
### Reservation Model ###
#########################

class ReservationManager(models.Manager):
    def month_archive(self, year, month):
        in_month = self.filter(Q(arrival__year=year), Q(arrival__month=month) | Q(departure__month=month))
        return in_month
    def day_archive(self, year, month, day):
        day_to_search = date(year, month, day)
        valid_reservations = self.filter(reservationdetail__day_reserved=day_to_search)
        return valid_reservations
 
   

class Reservation(models.Model):
    objects = ReservationManager()

    member = models.ForeignKey('Member', on_delete=models.CASCADE, blank=False, null=False) 
    #party_size = models.PositiveSmallIntegerField(default=1, help_text="Number of Guests in Party")
    #num_beds = models.PositiveSmallIntegerField(default=1, help_text="Number of Beds required")
    arrival = models.DateField(default=date.today)
    departure = models.DateField(default=date.today)
    #MEAL_CHOICES = (
     #       ('B', 'Breakfast'),
      #      ('L', 'Lunch'),
       #     ('D', 'Dinner'),
        #    )
    
    #first_meal = models.CharField('First meal at camp', max_length=1, choices=MEAL_CHOICES, default='LUNCH', help_text="First Meal")
    
    #last_meal = models.CharField('Last meal at camp', max_length=1, choices=MEAL_CHOICES, default='LUNCH', help_text="Last Meal")
    
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    
    
    # METHODS 
    def __str__(self):
        return str(self.id)
    # this next part is skipped for now
        date = self.arrival.strftime('%x')
        return 'Booking #' + str(self.id) + ' - ' + str(self.member) + ' - ' + date
    # Django method modifier
    def save(self, *args, **kwargs):
        print('saving')
        super(Reservation, self).save(*args, **kwargs)
        # this method call adds ReservationDetail objects and removes extra ones in case of date update
        self.add_details()
        return
    
    # custom housekeeping method
    def add_details(self):
        day_list = self.days_there(self.arrival, self.departure)
        for each_day in day_list:
            if not ReservationDetail.objects.filter(day_reserved=each_day, reservation=self):
                if each_day == day_list[0]:
                    # this is the first day of stay
                    ReservationDetail.objects.create(
                            reservation=self, 
                            day_reserved=each_day, 
                            is_first_day=True)
                elif each_day == day_list[-1]:
                    # this is the last day
                    ReservationDetail.objects.create(
                            reservation=self,
                            day_reserved=each_day,
                            is_last_day=True)
                else:
                    # all the other days
                    ReservationDetail.objects.create(
                            reservation=self,
                            day_reserved=each_day)
        # in case of updated entry:
        self.remove_extra_details()
        return

    # backup to add details method
    def remove_extra_details(self):
        #this pulls up the reservation details in a queryset and deletes those outside of arrival - departure
        the_details = ReservationDetail.objects.filter(reservation=self).order_by('day_reserved')
        deleted_items = the_details.filter(day_reserved__lt=self.arrival).delete()
        deleted_items2 = the_details.filter(day_reserved__gt=self.departure).delete()
        print(deleted_items, deleted_items2)
        return

    # utility method, used by add details and co
    def days_there(self, arrival, departure):
        # this returns a list of datetime instances corresponding to arrival - departure
        days_staying = (departure - arrival).days
        day_list = [arrival + timedelta(days=each_day) for each_day in range(days_staying + 1)]
        return day_list

    # Django model method modifier
    def clean(self):
        print('clean method is starting')
        #cleaned_data = super(Reservation, self).clean()
        #print(cleaned_data)
        try:
            self.member
        except:
            raise ValidationError(_('Member required'), code='invalid')

        # this validates whether there are existing res for these dates
        day_list = self.days_there(self.arrival, self.departure)
        for each_day in day_list:
            if ReservationDetail.objects.filter(
                    day_reserved=each_day,
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



###########################
### Reservation DETAILS ###
###########################

class ReservationDetailManager(models.Manager):
    
    pass

class ReservationDetail(models.Model):

    objects = ReservationDetailManager()
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, unique_for_date='day_reserved')
    camps = models.ManyToManyField('Camp', unique_for_date='day_reserved')
    num_guides = models.PositiveSmallIntegerField(default=0)
    day_reserved = models.DateField()
    is_first_day = models.BooleanField(default=False)
    is_last_day = models.BooleanField(default=False)
    eating_breakfast = models.BooleanField(default=True)
    eating_lunch = models.BooleanField(default=True)
    eating_dinner = models.BooleanField(default=True)
    num_guests = models.PositiveSmallIntegerField(default=1, help_text="Number of guests")
    num_beds_required = models.PositiveSmallIntegerField(default=1, help_text="Number of beds required")
    num_guides_required = models.PositiveSmallIntegerField(default=1, help_text="Number of guides requested")

    def __str__(self):
        return self.day_reserved.strftime('%x')

    def save(self, *args, **kwargs):
        if self.id == None:
            super(ReservationDetail, self).save(*args, **kwargs)
    
        # this method call adds GuideDetail objects 
        GuideDetail.objects.create(reservation=self.reservation, reservation_detail=self)
        CampDetail.objects.create(reservation=self.reservation, reservation_detail=self)

        return

    def get_absolute_url(self):
        return reverse('resdetail_detail', kwargs={'pk':self.id})
    
    def guide_list(self):
        return GuideDetail.objects.filter(reservation_detail=self.id)


