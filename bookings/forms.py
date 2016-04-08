from django import forms
from django.forms import ModelForm

from bookings.models import Reservation

### Search Form ###
class SearchDatesForm(forms.Form):
    check_in = forms.DateField(widget=forms.SelectDateWidget)
    check_out = forms.DateField(widget=forms.SelectDateWidget)
    guests = forms.IntegerField(required=True, min_value=1)
    
    def clean(self):
        print('\nclean method now startingi\n')
        cleaned_data = super(SearchDatesForm, self).clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        
        if check_in and check_out:
            print('hello')
            if check_in > check_out:
                raise forms.ValidationError(
                        "Check-in and Check-out dates are not possible."
                        )
### Reservation Step Through Form ###
class ReservationStepOne(ModelForm):
    class Meta:
        model = Reservation
        fields = ['member', 'arrival', 'departure']

    def __init__(self, *args, **kwargs):
        super(ReservationStepOne, self).__init__(*args, **kwargs)
        self.fields['member'].required = True
        self.fields['arrival'].required = True
        self.fields['departure'].required = True

    def clean(self):
        cleaned_data = super(ReservationStepOne, self).clean()
        return cleaned_data


