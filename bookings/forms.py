from django.forms import ModelForm
from bookings.models import Reservation, Member, Camp, Guide
from django.contrib import messages

class ReservationForm(ModelForm):

    def is_valid(self):

        valid = super(ReservationForm, self).is_valid()
        # if it fails, we can quit now
        if not valid:
            print('not valid after super')
            return valid
        # add extra actions before validating
        return valid

    

    class Meta:
        model = Reservation
        fields = ['member', 'party_size', 'arrival', 'departure', 'first_meal', 'last_meal']


