from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from bookings.models import Reservation, ReservationDetail

#from .forms import ReservationForm

class ReservationListView(ListView):
    model = Reservation
    template_name = 'bookings/reservation_list.html'
    context_object_name = 'reservation_list'

class ReservationCreate(CreateView):
    model = Reservation
    #form_class = ReservationForm
    template_name = 'bookings/reservation_edit.html'
    fields =['member', 'party_size', 'arrival', 'departure', 'first_meal', 'last_meal']

    def get_initial(self):
        # this helps prepopulate the form based on presence of pk
        if 'pk' in self.kwargs:
            return {'member': self.kwargs['pk']}
        else:
            return

    def get_success_url(self):
        return reverse_lazy('reservation_detail', kwargs={'pk':self.object.pk})

class ReservationUpdate(UpdateView):
    model = Reservation
    template_name = 'bookings/reservation_edit.html'
    fields = ['member', 'party_size', 'arrival', 'departure', 'first_meal', 'last_meal']

class ReservationDelete(DeleteView):
    model = Reservation
    template_name = 'bookings/reservation_delete.html'
    success_url = reverse_lazy('reservation_list')

class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'bookings/reservation_detail.html'
    context_object_name = 'reservation'
    def get_context_data(self, **kwargs):
        context = super(ReservationDetailView, self).get_context_data(**kwargs)
        reservation_details = ReservationDetail.objects.filter(reservation=self.kwargs['pk'])
        context['reservation_details'] = reservation_details
        print(context)
        return context

class ReservationArchiveView(ArchiveIndexView):
    queryset = Reservation.objects.all()
    date_field = 'arrival'
    allow_future = True
    make_object_list = True

class ReservationYearArchiveView(YearArchiveView):
    queryset = Reservation.objects.all()
    date_field = 'arrival'
    make_object_list = True
    allow_future = True
    ordering = ["arrival",]


class ReservationMonthArchiveView(MonthArchiveView):
    queryset = ReservationDetail.objects.all()
    date_field = "day"
    allow_future = True
    month_format = "%m"
    template_name="bookings/reservation_archive_month.html"


class ReservationWeekArchiveView(WeekArchiveView):
    queryset = ReservationDetail.objects.all()
    date_field = 'day'
    week_format = "%W"
    allow_future = True
    template_name = "bookings/reservation_archive_week.html"

class ReservationDayArchiveView(DayArchiveView):
    queryset = ReservationDetail.objects.all()
    date_field = 'day'
    allow_future = True
    template_name = "bookings/reservation_archive_day.html"

