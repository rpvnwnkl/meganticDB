from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from bookings.models import Camp, Reservation, ReservationDetail

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
