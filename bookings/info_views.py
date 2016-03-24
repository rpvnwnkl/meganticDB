from django.views.generic import ListView
from django.views.generic import ArchiveIndexView
from django.views.generic import YearArchiveView
from django.views.generic import MonthArchiveView

from bookings.models import Member
from bookings.models import Camp
from bookings.models import ReservationDetail

class MemberInfoView(ListView):
    model = Member
    context_object_name = 'members_info'

class CampInfoView(ListView):
    model = Camp
    context_object_name = 'camps_info'

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
