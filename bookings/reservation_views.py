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
from django.views.generic.edit import CreateView

from bookings.models import Reservation, ReservationDetail

from .forms import ReservationForm

class ReservationListView(ListView):
    model = Reservation
    template_name = 'bookings/reservation_list.html'
    context_object_name = 'reservation_list'

class ReservationCreate(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'bookings/reservation_edit.html'
    def get_initial(self):
        return {'member': self.kwargs['pk']}
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            #do other things
            reservation.save()
            return redirect('reservation_detail', pk=reservation.pk)
        else:
            return render(request, 'bookings/reservation_edit.html', {'form':form})

    def get_success_url(self):
        return reverse_lazy('reservation_detail', kwargs={'pk':self.object.pk})

def reservation_new(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            #reservation.created_on_date = timezone.now()
            reservation.save()
            return redirect('reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm
    return render(request, 'bookings/reservation_edit.html', {'form': form})

def reservation_edit(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save(commit=False)
            #reservation.created_on_date = timezone.now()
            reservation.save()
            return redirect('reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'bookings/reservation_edit.html', {'form': form})

def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.delete()
    return redirect('reservation_list')

class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'bookings/reservation_detail.html'
    context_object_name = 'reservation'
    def get_context_data(self, **kwargs):
        context = super(ReservationDetailView, self).get_context_data(**kwargs)
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

