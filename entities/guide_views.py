from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy

from .models import Guide, GuideDetail, Reservation, ReservationDetail

class GuideListView(ListView):
    model = Guide
    context_object_name = 'guide_list'

class GuideDetailView(DetailView):
    model = Guide
    context_object_name = 'guide'

    def get_context_data(self, *args, **kwargs):
        context = super(GuideDetailView, self).get_context_data(**kwargs)
        #guide_reservations = Reservation.objects.filter(reservationdetail__guides=self.kwargs['pk']).order_by('arrival')
        #context['reservations'] = guide_reservations
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
        context['reservation_details'] = ReservationDetail.objects.filter(reservation=reservation_to_search)
        context['current_reservation'] = Reservation.objects.get(pk=reservation_to_search)
        print(context)
        return context



##################################
### Guide Detail Section #########
##################################

class GuideDetailReservation(TemplateView):
    model = GuideDetail
    context_object_name = 'guide_list'
    template_name = 'bookings/guide/guide_detail_reservations.html'
    
    def get_context_data(self, **kwargs):
        context = super(GuideDetailReservation, self).get_context_data(**kwargs)
        reservation_to_search = self.kwargs['pk']
        context['reservation_details'] = ReservationDetail.objects.filter(reservation=reservation_to_search)
        context['current_reservation'] = Reservation.objects.get(pk=reservation_to_search)
        print(context)
        return context

class GuideDetailUpdate(UpdateView):
    model = GuideDetail
    fields = ['reservation_detail', 'guide']
    template_name = 'bookings/guide/guide_detail_edit.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(GuideDetailUpdate, self).get_context_data(**kwargs)
        print(context)
        #context['pk'] = self.kwargs['pk']
        #print(context)
        return context

class GuideDetailCreate(CreateView):
    model = GuideDetail
    fields = ['reservation_detail', 'guide']
    template_name = 'bookings/guide/guide_detail_edit.html'

class GuideDetailDelete(DeleteView):
    model = GuideDetail
    template_name = 'bookings/guide/guide_detail_delete.html'
    success_url = reverse_lazy('reservation_list')
