
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import ArchiveIndexView

from bookings.models import Reservation, ReservationDetail

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

