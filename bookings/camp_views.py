from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from bookings.models import Camp, Reservation, ReservationDetail

import datetime

class CampListView(ListView):
    model = Camp
    context_object_name = 'camp_list'

class CampDetailView(DetailView):
    model = Camp
    context_object_name = 'camp'

    def get_context_data(self, *args, **kwargs):
        context = super(CampDetailView, self).get_context_data(**kwargs)
        camp_reservations = Reservation.objects.filter(reservationdetail__camps=self.kwargs['pk']).order_by('arrival')
        context['reservations'] = camp_reservations
        return context

class CampCreate(CreateView):
    model = Camp
    fields = ['camp_name', 'sleeps']
    template_name = 'bookings/camp_edit.html'

class CampUpdate(UpdateView):
    model = Camp
    fields = ['camp_name', 'sleeps']
    template_name = 'bookings/camp_edit.html'

class CampDelete(DeleteView):
    model = Camp
    template_name = 'bookings/camp_delete.html'
    success_url = reverse_lazy('camp_list')

class CampMonthlySchedule(TemplateView):
    
    template_name = 'bookings/camp_schedule.html'

    def get_context_data(self, **kwargs):
        context = super(CampMonthlySchedule, self).get_context_data(**kwargs)
        camp_list, month_days = Camp.objects.get_vacancies(self.kwargs['year'], self.kwargs['month'])
        context['camp_list'] = camp_list
        print (camp_list)
        print (month_days)
        context['month_days'] = month_days
        context['current_month'] = month_days[0]
        context['previous_month'] = (month_days[0] - datetime.timedelta(days=1))
        context['next_month'] = (month_days[-1] + datetime.timedelta(days=1))
        return context

class CampReservation(TemplateView):
    template_name = 'bookings/camp_reservations.html'

    def get_context_data(self, **kwargs):
        context = super(CampReservation, self).get_context_data(**kwargs)
        reservation_to_search = self.kwargs['reservation']
        camp_info = ReservationDetail.objects.filter(reservation=reservation_to_search)
        context['reservation_list'] = camp_info
        context['current_reservation'] = ReservationDetail.objects.get(reservation=reservation_to_search)
        return context
