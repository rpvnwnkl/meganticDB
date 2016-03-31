from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
