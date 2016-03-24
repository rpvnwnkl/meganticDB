from django.views.generic import ListView, DetailView
from django.views.generic import ArchiveIndexView
from django.views.generic import YearArchiveView
from django.views.generic import MonthArchiveView

from bookings.models import Member
from bookings.models import Camp
from bookings.models import Reservation
from bookings.models import ReservationDetail

import datetime

class MembersInfoView(ListView):
    model = Member
    context_object_name = 'members_info'

class CampsInfoView(ListView):
    model = Camp
    context_object_name = 'camps_info'

class ReservationInfoView(DetailView):
    model = Reservation
    template_name = 'bookings/reservation_info.html'
    context_object_name = 'reservation'

    def get_context_data(self, **kwargs):
        context = super(ReservationInfoView, self).get_context_data(**kwargs)
        # collect camp/guide info for each day of stay
        details = []
        resDetailInstances =  ReservationDetail.objects.filter(reservation=self.kwargs['pk'])
        for each_day in resDetailInstances:
            details.append({
                        'day':each_day.day,
                        'camps':each_day.camps.all(), 
                        'guides':each_day.guides.all(),
                        })
        context['details'] = details
        return context

class CampArchive(ArchiveIndexView):
    
    def get_queryset(self):
        self.camp = self.kwargs['camp']
        queryset = ReservationDetail.objects.filter(camps__camp_name=self.camp)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(CampArchive, self).get_context_data(**kwargs)
        context['camp'] = self.kwargs['camp']
        return context

    date_field = 'day'
    make_object_list = True
    allow_future = True
    template_name = 'bookings/camp_archive.html'


class CampYearArchive(YearArchiveView):
    
    def get_queryset(self):
        self.camp = self.kwargs['camp']
        queryset = ReservationDetail.objects.filter(camps__camp_name=self.camp)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(CampYearArchive, self).get_context_data(**kwargs)
        context['camp'] = self.kwargs['camp']
        return context

    date_field = 'day'
    make_object_list = True
    template_name = 'bookings/camp_year_archive.html'

class CampMonthArchive(MonthArchiveView):
    pass
