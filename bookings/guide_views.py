from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy

from bookings.models import Guide, Reservation, ReservationDetail

class GuideListView(ListView):
    model = Guide
    context_object_name = 'guide_list'

class GuideDetailView(DetailView):
    model = Guide
    context_object_name = 'guide'

    def get_context_data(self, *args, **kwargs):
        context = super(GuideDetailView, self).get_context_data(**kwargs)
        guide_reservations = Reservation.objects.filter(reservationdetail__guides=self.kwargs['pk']).order_by('arrival')
        context['reservations'] = guide_reservations
        return context

class GuideCreate(CreateView):
    model = Guide
    fields = ['first_name', 'last_name']
    template_name = 'bookings/guide_edit.html'

class GuideUpdate(UpdateView):
    model = Guide
    fields = ['first_name', 'last_name']
    template_name = 'bookings/guide_edit.html'

class GuideDelete(DeleteView):
    model = Guide
    template_name = 'bookings/guide_delete.html'
    success_url = reverse_lazy('guide_list')

class GuideReservation(TemplateView):
    template_name = 'bookings/guide_reservations.html'

    def get_context_data(self, **kwargs):
        context = super(GuideReservation, self).get_context_data(**kwargs)
        reservation_to_search = self.kwargs['reservation']
        guide_info = ReservationDetail.objects.filter(reservation=reservation_to_search)
        context['guide_list'] = guide_info
        context['current_reservation'] = ReservationDetail.objects.get(reservation=reservation_to_search)
        return context
