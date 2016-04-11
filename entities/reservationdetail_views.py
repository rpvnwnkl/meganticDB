from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Reservation, ReservationDetail

class ReservationDetailListView(ListView):
    model = ReservationDetail
    context_object_name = 'resdetail_list'

class ReservationDetailDetailView(DetailView):
    model = ReservationDetail
    context_object_name = 'resdetail'

    def get_context_data(self, *args, **kwargs):
        context = super(ReservationDetailDetailView, self).get_context_data(**kwargs)
        reservationdetail = ReservationDetail.objects.get(pk=self.kwargs['pk'])
        reservation = reservationdetail.reservation
        context['reservation'] = reservation
        return context

class ReservationDetailCreate(CreateView):
    model = ReservationDetail
    fields = ['reservation', 'day', 'camps', 'guides']
    template_name = 'bookings/reservationdetail_edit.html'

class ReservationDetailUpdate(UpdateView):
    model = ReservationDetail
    fields = ['reservation', 'day', 'camps', 'guides']
    template_name = 'bookings/reservationdetail_edit.html'

class ReservationDetailDelete(DeleteView):
    model = ReservationDetail
    context_object_name = 'resdetail'
    template_name = 'bookings/reservationdetail_delete.html'
    success_url = reverse_lazy('resdetail_list')
