from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.forms.models import model_to_dict
from django.core import serializers

from .models import Reservation
# Create your views here.

def index(request):
    latest_reservation_list = Reservation.objects.order_by('arrival')[:5]
    template = loader.get_template('bookings/index.html')
    context = {
            'latest_reservation_list': latest_reservation_list,
            }
    return HttpResponse(template.render(context, request))

def year_archive(request, year):
    year_entries = Reservation.objects.filter(arrival__year=year)
    entry_dicts = [entry.archive_dict() for entry in year_entries]
    context = {
            'year': year,
            'year_entries': entry_dicts,
            }
    return render(request, 'bookings/year_archive.html', context)

def month_archive(request, year, month):
    month_entries = Reservation.objects.month_archive(year, month)
    entry_dicts = [entry.archive_dict() for entry in month_entries]
    context = {
            'year': year,
            'month': month,
            'month_entries': entry_dicts,
            }
    return render(request, 'bookings/month_archive.html', context)

def day_archive(request, year, month, day):
    day_entries = Reservation.objects.day_archive(int(year), int(month), int(day))
    entry_dicts = [entry.archive_dict() for entry in day_entries]
    context = {
            'year': year,
            'month': month,
            'day': day,
            'day_entries': day_entries,
            }
    return render(request, 'bookings/day_archive.html', context)

