from django import forms
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.shortcuts import render
from django.forms.models import BaseModelFormSet

from .models import ReservationDetail

from .models import Reservation

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

class ReservationStepTwo(ModelForm):
    class Meta:
        model = ReservationDetail
        fields = ['num_guests', 'num_beds_required', 'num_guides_required', 'eating_breakfast', 'eating_lunch', 'eating_dinner']

def create_res_details(request, respk):
    ReservationDetailFormSet = modelformset_factory(ReservationDetail, fields=('num_guests', 'num_beds_required', 'num_guides_required', 'eating_breakfast', 'eating_lunch', 'eating_dinner'))
    if request.method == "POST":
        print(request.POST)
        formset = ReservationDetailFormSet(request.POST, request.FILES, queryset=ReservationDetail.objects.filter(reservation=respk))
        if formset.is_valid():
            formset.save()
    else:
        print(request.POST)
        formset = ReservationDetailFormSet(queryset=ReservationDetail.objects.filter(reservation=respk))
    return render(request, 'reservation/reservation_details.html', {'formset': formset})


#class NewReservationDetailFormSet(BaseModelFormSet):
    
class DailyDetailsForm(ModelForm):
    class Meta:
        model = ReservationDetail
        fields = ['camps', 'eating_breakfast', 'eating_lunch', 'eating_dinner', 'num_guides']

class ReservationUpdateForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['arrival', 'departure']

class BaseDetailsFormSet(BaseModelFormSet):
    def clean(self):
        # custom validation

        if any(self.errors):
            return

