from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from bookings.models import Member, Reservation

class MemberListView(ListView):
    model = Member
    context_object_name = 'member_list'

class MemberDetailView(DetailView):
    model = Member
    context_object_name = 'member'

    def get_context_data(self, *args, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        mem_reservations = Reservation.objects.filter(member=self.kwargs['pk']).order_by('arrival')
        context['reservations'] = mem_reservations
        return context

class MemberCreate(CreateView):
    model = Member
    fields = ['first_name', 'last_name']
    template_name = 'bookings/member_edit.html'

class MemberUpdate(UpdateView):
    model = Member
    fields = ['first_name', 'last_name']
    template_name = 'bookings/member_edit.html'

class MemberDelete(DeleteView):
    model = Member
    template_name = 'bookings/member_delete.html'
    success_url = reverse_lazy('member_list')
