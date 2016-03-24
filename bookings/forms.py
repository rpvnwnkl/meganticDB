from django.shortcuts import render
from django.forms import ModelForm
from bookings.models import Reservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['member', 'party_size', 'arrival', 'departure', 'first_meal', 'last_meal']
        #template_name = 'bookings/reservation_form.html'

def add_reservation(request):
    form = ReservationForm()
    return render(request, 'bookings/reservation_form.html', {'form': form})

